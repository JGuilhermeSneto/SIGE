from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models.ficha_medica import FichaMedica, RegistroVacina, AtestadoMedico
from .forms import FichaMedicaForm, RegistroVacinaForm, AtestadoForm, AtestadoAnaliseForm
from django.utils import timezone
from apps.usuarios.models.perfis import Aluno, Professor
from apps.usuarios.utils.perfis import is_super_ou_gestor, get_nome_exibicao, get_foto_perfil
from datetime import timedelta

@login_required
def visualizar_saude_aluno(request, aluno_id):
    """Exibe a ficha médica de um aluno. Acessível por Gestores e Professores."""
    aluno = get_object_or_404(Aluno, id=aluno_id)
    
    # Validação de permissão: Gestor, Professor do Aluno ou o próprio Aluno
    eh_gestor = is_super_ou_gestor(request.user)
    eh_professor = False
    if hasattr(request.user, 'professor') and hasattr(aluno, 'turma') and aluno.turma:
        eh_professor = aluno.turma.disciplinas.filter(professor=request.user.professor).exists()
    eh_proprio_aluno = hasattr(request.user, 'aluno') and request.user.aluno.id == aluno.id
    
    if not (eh_gestor or eh_professor or eh_proprio_aluno):
        messages.error(request, "Você não tem permissão para ver dados de saúde deste aluno.")
        return redirect('painel_usuarios')

    ficha, created = FichaMedica.objects.get_or_create(aluno=aluno)
    
    return render(request, 'saude/detalhe_saude.html', {
        'aluno': aluno,
        'ficha': ficha,
        'is_gestor': eh_gestor,
        'nome_exibicao': get_nome_exibicao(request.user),
        'foto_perfil_url': get_foto_perfil(request.user),
    })

@login_required
@user_passes_test(is_super_ou_gestor)
def editar_ficha_medica(request, aluno_id):
    """Permite ao gestor editar a ficha médica e vacinas."""
    aluno = get_object_or_404(Aluno, id=aluno_id)
    ficha, _ = FichaMedica.objects.get_or_create(aluno=aluno)
    
    if request.method == "POST":
        form = FichaMedicaForm(request.POST, instance=ficha)
        if form.is_valid():
            form.save()
            messages.success(request, f"Ficha médica de {aluno.nome_completo} atualizada!")
            return redirect('visualizar_saude_aluno', aluno_id=aluno.id)
    else:
        form = FichaMedicaForm(instance=ficha)
        
    return render(request, 'saude/form_saude.html', {
        'aluno': aluno,
        'form': form,
        'nome_exibicao': get_nome_exibicao(request.user),
        'foto_perfil_url': get_foto_perfil(request.user),
    })

@login_required
@user_passes_test(is_super_ou_gestor)
def adicionar_vacina(request, ficha_id):
    ficha = get_object_or_404(FichaMedica, id=ficha_id)
    if request.method == "POST":
        form = RegistroVacinaForm(request.POST)
        if form.is_valid():
            vacina = form.save(commit=False)
            vacina.ficha = ficha
            vacina.save()
            messages.success(request, "Vacina registrada!")
    return redirect('visualizar_saude_aluno', aluno_id=ficha.aluno.id)

# --- VISTAS DE ATESTADO MÉDICO ---

@login_required
def listar_atestados_aluno(request):
    """Lista os atestados enviados pelo usuário logado (Aluno, Professor ou Gestor)."""
    atestados = AtestadoMedico.objects.filter(usuario=request.user)
    return render(request, 'saude/meus_atestados.html', {
        'atestados': atestados,
        'nome_exibicao': get_nome_exibicao(request.user),
        'foto_perfil_url': get_foto_perfil(request.user),
    })

@login_required
def enviar_atestado(request):
    """Permite ao usuário (Aluno/Professor/Gestor) fazer o upload de um novo atestado."""
    if request.method == "POST":
        form = AtestadoForm(request.POST, request.FILES)
        if form.is_valid():
            atestado = form.save(commit=False)
            atestado.usuario = request.user
            atestado.save()
            messages.success(request, "Atestado enviado com sucesso! Aguarde a análise da gestão.")
            return redirect('listar_atestados_aluno')
    else:
        form = AtestadoForm()

    return render(request, 'saude/enviar_atestado.html', {
        'form': form,
        'nome_exibicao': get_nome_exibicao(request.user),
        'foto_perfil_url': get_foto_perfil(request.user),
    })

@login_required
@user_passes_test(is_super_ou_gestor)
def gestao_atestados(request):
    """Painel do gestor para listar todos os atestados."""
    status_filtro = request.GET.get('status', 'PENDENTE')
    atestados = AtestadoMedico.objects.filter(status=status_filtro).select_related('usuario')
    
    return render(request, 'saude/gestao_atestados.html', {
        'atestados': atestados,
        'status_atual': status_filtro,
        'nome_exibicao': get_nome_exibicao(request.user),
        'foto_perfil_url': get_foto_perfil(request.user),
    })

@login_required
@user_passes_test(is_super_ou_gestor)
def revisar_atestado(request, atestado_id):
    """View para o gestor aprovar ou rejeitar um atestado."""
    atestado = get_object_or_404(AtestadoMedico, id=atestado_id)
    
    if request.method == "POST":
        form = AtestadoAnaliseForm(request.POST, instance=atestado)
        if form.is_valid():
            atestado = form.save(commit=False)
            atestado.data_analise = timezone.now()
            atestado.analisado_por = request.user.gestor if hasattr(request.user, 'gestor') else None
            atestado.save()
            
            # Se aprovado, processa automações
            if atestado.status == 'APROVADO':
                # --- LÓGICA PARA ALUNOS ---
                if hasattr(atestado.usuario, 'aluno'):
                    aluno = atestado.usuario.aluno
                    from apps.academico.models.desempenho import Frequencia
                    faltas = Frequencia.objects.filter(
                        aluno=aluno,
                        data__range=[atestado.data_inicio, atestado.data_fim],
                        presente=False
                    )
                    total_justificadas = faltas.count()
                    faltas.update(justificada=True, atestado=atestado)
                    messages.success(request, f"Atestado aprovado! {total_justificadas} faltas do aluno {aluno.nome_completo} foram justificadas.")
                
                # --- LÓGICA PARA PROFESSORES ---
                elif hasattr(atestado.usuario, 'professor'):
                    professor = atestado.usuario.professor
                    from apps.academico.models.academico import GradeHorario, PlanejamentoAula
                    
                    # Mapeamento para buscar sessões na grade
                    WEEKDAY_MAP = {0: 'segunda', 1: 'terca', 2: 'quarta', 3: 'quinta', 4: 'sexta'}
                    
                    # Grades do professor
                    grades = GradeHorario.objects.filter(disciplina__professor=professor)
                    
                    total_suspendas = 0
                    current_date = atestado.data_inicio
                    while current_date <= atestado.data_fim:
                        weekday_str = WEEKDAY_MAP.get(current_date.weekday())
                        if weekday_str:
                            sessoes_dia = grades.filter(dia=weekday_str)
                            for sessao in sessoes_dia:
                                PlanejamentoAula.objects.update_or_create(
                                    disciplina=sessao.disciplina,
                                    turma=sessao.turma,
                                    data_aula=current_date,
                                    horario_aula=sessao.horario,
                                    defaults={
                                        'professor': professor,
                                        'status': 'SUSPENSA',
                                        'conteudo': f"Aula suspensa: Professor em licença médica (Atestado #{atestado.id})",
                                        'concluido': True
                                    }
                                )
                                total_suspendas += 1
                        current_date += timedelta(days=1)
                    
                    messages.success(request, f"Atestado aprovado! {total_suspendas} sessões de aula do professor {professor.nome_completo} foram marcadas como suspensas.")
                
                else:
                    messages.success(request, "Atestado aprovado com sucesso.")
            else:
                messages.warning(request, "Atestado rejeitado.")
                
            return redirect('gestao_atestados')
    else:
        form = AtestadoAnaliseForm(instance=atestado)

    return render(request, 'saude/revisar_atestado.html', {
        'atestado': atestado,
        'form': form,
        'nome_exibicao': get_nome_exibicao(request.user),
        'foto_perfil_url': get_foto_perfil(request.user),
    })
