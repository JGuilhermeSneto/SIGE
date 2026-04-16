from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models.ficha_medica import FichaMedica, RegistroVacina
from .forms import FichaMedicaForm, RegistroVacinaForm
from apps.usuarios.models.perfis import Aluno
from apps.usuarios.utils.perfis import is_super_ou_gestor, get_nome_exibicao, get_foto_perfil

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
