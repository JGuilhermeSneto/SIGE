from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from ..models.academico import (
    Disciplina, Turma, GradeHorario, AtividadeProfessor, 
    Questao, Alternativa, EntregaAtividade, RespostaAluno
)
from ..models.desempenho import Nota, NotaAtividade, Frequencia
from apps.usuarios.models.perfis import Professor, Aluno
from ..forms.academico import DisciplinaForm, AtividadeProfessorForm
from ..utils.academico import (
    _get_grade_horario_turma, _get_ocupados_por_professor,
    _calcular_detalhes_disciplina
)
from apps.comum.utils.constantes import NOMES_DIAS
from apps.usuarios.utils.perfis import (
    get_nome_exibicao, get_foto_perfil, redirect_user, is_super_ou_gestor
)

@login_required
def visualizar_disciplinas(request, disciplina_id):
    """Exibe detalhes de uma disciplina."""
    disciplina = get_object_or_404(Disciplina, id=disciplina_id)
    eh_professor_da_disc = (
        hasattr(request.user, "professor") and disciplina.professor == request.user.professor
    )
    if not (is_super_ou_gestor(request.user) or eh_professor_da_disc):
        messages.error(request, "Permissão negada.")
        return redirect("painel_usuarios")

    turma = disciplina.turma
    from apps.usuarios.models.perfis import Aluno
    alunos = Aluno.objects.filter(turma=turma).select_related("user").order_by("nome_completo")
    notas = Nota.objects.filter(disciplina=disciplina).select_related("aluno")
    notas_dict = {nota.aluno.id: nota for nota in notas}

    return render(request, "disciplina/visualizar_disciplinas.html", {
        "disciplina": disciplina, "turma": turma, "alunos": alunos, "notas_dict": notas_dict,
        "nome_exibicao": get_nome_exibicao(request.user), "foto_perfil_url": get_foto_perfil(request.user),
        "is_gestor_ou_super": is_super_ou_gestor(request.user),
    })

@login_required
@user_passes_test(is_super_ou_gestor)
def cadastrar_disciplina_para_turma(request, turma_id):
    """Vincula disciplina a turma."""
    turma = get_object_or_404(Turma, id=turma_id)
    if request.method == "POST":
        data = request.POST.copy()
        data["turma"] = turma.id
        form = DisciplinaForm(data)
        if form.is_valid():
            form.save()
            messages.success(request, "Disciplina cadastrada com sucesso!")
            return redirect("listar_disciplinas_turma", turma_id=turma.id)
        else:
            for field, errors in form.errors.items():
                for error in errors: messages.error(request, f"{field}: {error}")
    else:
        form = DisciplinaForm(initial={"turma": turma})

    professores = Professor.objects.all().select_related("user")
    return render(request, "disciplina/cadastrar_disciplina_turma.html", {
        "turma": turma, "professores": professores, "form": form,
        "nome_exibicao": get_nome_exibicao(request.user), "foto_perfil_url": get_foto_perfil(request.user),
    })

@login_required
@user_passes_test(is_super_ou_gestor)
def editar_disciplina(request, disciplina_id):
    """Edita disciplina."""
    disciplina = get_object_or_404(Disciplina, id=disciplina_id)
    turma = disciplina.turma
    if request.method == "POST":
        data = request.POST.copy()
        data["turma"] = turma.id
        form = DisciplinaForm(data, instance=disciplina)
        if form.is_valid():
            form.save()
            messages.success(request, "Disciplina atualizada com sucesso!")
            return redirect("listar_disciplinas_turma", turma_id=turma.id)
        else:
            for field, errors in form.errors.items():
                for error in errors: messages.error(request, f"{field}: {error}")
    else:
        form = DisciplinaForm(instance=disciplina)

    professores = Professor.objects.all().select_related("user")
    return render(request, "disciplina/cadastrar_disciplina_turma.html", {
        "disciplina": disciplina, "turma": turma, "professores": professores, "form": form,
        "nome_exibicao": get_nome_exibicao(request.user), "foto_perfil_url": get_foto_perfil(request.user),
    })

@login_required
@user_passes_test(is_super_ou_gestor)
def listar_disciplinas_turma(request, turma_id):
    """Lista disciplinas de uma turma."""
    turma = get_object_or_404(Turma, id=turma_id)
    disciplinas = Disciplina.objects.filter(turma=turma).select_related("professor__user")
    return render(request, "disciplina/listar_disciplinas_turma.html", {
        "turma": turma, "disciplinas": disciplinas, "nome_exibicao": get_nome_exibicao(request.user), "foto_perfil_url": get_foto_perfil(request.user),
    })

@login_required
def disciplinas_turma(request, turma_id):
    """Visão de disciplinas de uma turma."""
    user, turma = request.user, get_object_or_404(Turma, id=turma_id)
    if hasattr(user, "professor"):
        qs = Disciplina.objects.filter(turma=turma, professor=user.professor)
    elif is_super_ou_gestor(user):
        qs = Disciplina.objects.filter(turma=turma)
    else: return redirect("login")

    detalhes = [_calcular_detalhes_disciplina(d, turma) for d in qs.order_by("nome")]
    return render(request, "professor/disciplinas_turma.html", {
        "turma": turma, "disciplinas_detalhadas": detalhes, "nome_exibicao": get_nome_exibicao(user), "foto_perfil_url": get_foto_perfil(user),
    })

@login_required
def visualizar_grade_professor(request, turma_id):
    """Grade horária para o professor."""
    if not hasattr(request.user, "professor"): return redirect("login")
    turma = get_object_or_404(Turma, id=turma_id)
    discs = Disciplina.objects.filter(turma=turma, professor=request.user.professor)
    return render(request, "professor/visualizar_grade_professor.html", {
        "turma": turma, "grade_horario": _get_grade_horario_turma(turma), "nomes_dias": NOMES_DIAS, "disciplinas_professor": discs,
        "nome_exibicao": get_nome_exibicao(request.user), "foto_perfil_url": get_foto_perfil(request.user),
    })

@login_required
@user_passes_test(is_super_ou_gestor)
def grade_horaria(request, turma_id):
    """Gerencia grade horária."""
    turma = get_object_or_404(Turma, id=turma_id)
    from ..utils.constantes import HORARIOS, DIAS_SEMANA
    turno_key = turma.turno.lower().replace("ã", "a").replace("á", "a")
    horarios_turno = HORARIOS.get(turno_key, [])

    if request.method == "POST":
        GradeHorario.objects.filter(turma=turma).delete()
        for dia in DIAS_SEMANA:
            for idx, h_label in enumerate(horarios_turno):
                disc_id = request.POST.get(f"grade-{dia}-{idx}")
                if disc_id:
                    GradeHorario.objects.create(turma=turma, disciplina_id=disc_id, dia=dia, horario=h_label)
        messages.success(request, "Grade atualizada!")
        return redirect("grade_horaria", turma_id=turma.id)

    disciplinas = Disciplina.objects.filter(turma=turma).select_related("professor")
    grade_db = GradeHorario.objects.filter(turma=turma)
    grade_dict = {f"{g.dia}_{g.horario}": g.disciplina_id for g in grade_db}

    prof_ocupados = {}
    for d in disciplinas:
        if d.professor:
            prof_ocupados[d.id] = _get_ocupados_por_professor(d.professor.id, turma.ano, turma.id)

    return render(request, "turma/grade_horaria.html", {
        "turma": turma, "disciplinas": disciplinas, "horarios": horarios_turno, "dias_semana": DIAS_SEMANA, "grade_dict": grade_dict, "prof_ocupados": prof_ocupados,
        "nome_exibicao": get_nome_exibicao(request.user), "foto_perfil_url": get_foto_perfil(request.user),
    })

@login_required
def disciplinas_professor(request):
    """Lista as turmas do professor."""
    if not hasattr(request.user, "professor"): return redirect("login")
    professor = request.user.professor
    from ..utils.filtros import _get_ano_filtro_professor
    anos_disponiveis = list(Turma.objects.filter(disciplinas__professor=professor).values_list("ano", flat=True).distinct().order_by("-ano")) or [timezone.now().year]
    ano_filtro, anos_disponiveis = _get_ano_filtro_professor(request, anos_disponiveis, timezone.now().year)

    from ..models import Aluno
    turmas = Turma.objects.filter(disciplinas__professor=professor, ano=ano_filtro).distinct().order_by("nome")
    turmas_detalhadas = [{
        "turma": t, "disciplinas_count": Disciplina.objects.filter(turma=t, professor=professor).count(), "alunos_count": Aluno.objects.filter(turma=t).count(), "turno_display": t.get_turno_display(),
    } for t in turmas]

    return render(request, "professor/disciplinas_professor.html", {
        "turmas_detalhadas": turmas_detalhadas, "nome_exibicao": get_nome_exibicao(request.user), "foto_perfil_url": get_foto_perfil(request.user), "anos_disponiveis": anos_disponiveis, "ano_filtro": ano_filtro,
    })


@login_required
@user_passes_test(is_super_ou_gestor)
def excluir_disciplina(request, disciplina_id):
    """Remove uma disciplina da grade da turma."""
    disciplina = get_object_or_404(Disciplina, id=disciplina_id)
    turma_id   = disciplina.turma.id
    nome_disc  = disciplina.nome
    disciplina.delete()
    messages.success(request, f"Disciplina '{nome_disc}' excluída com sucesso!")
    return redirect("listar_disciplinas_turma", turma_id=turma_id)

@login_required
def listar_atividades(request, disciplina_id):
    """Lista as atividades/provas cadastradas pelo professor para a disciplina."""
    disciplina = get_object_or_404(Disciplina, id=disciplina_id)
    
    eh_professor = hasattr(request.user, "professor") and disciplina.professor == request.user.professor
    if not (is_super_ou_gestor(request.user) or eh_professor):
        messages.error(request, "Acesso negado.")
        return redirect("painel_usuarios")
        
    atividades = disciplina.atividades.all()
    
    return render(request, "professor/listar_atividades.html", {
        "disciplina": disciplina,
        "turma": disciplina.turma,
        "atividades": atividades,
        "is_professor": eh_professor,
        "nome_exibicao": get_nome_exibicao(request.user),
        "foto_perfil_url": get_foto_perfil(request.user),
    })

@login_required
def cadastrar_atividade(request, disciplina_id):
    """Permite ao professor cadastrar nova prova ou trabalho."""
    disciplina = get_object_or_404(Disciplina, id=disciplina_id)
    
    if not (hasattr(request.user, "professor") and disciplina.professor == request.user.professor):
        messages.error(request, "Somente o professor da disciplina pode cadastrar atividades.")
        return redirect("listar_atividades", disciplina_id=disciplina.id)

    if request.method == "POST":
        form = AtividadeProfessorForm(request.POST)
        if form.is_valid():
            atividade = form.save(commit=False)
            atividade.disciplina = disciplina
            atividade.save()
            messages.success(request, f"{atividade.get_tipo_display()} cadastrada com sucesso!")
            return redirect("listar_atividades", disciplina_id=disciplina.id)
        else:
            for field, errors in form.errors.items():
                for error in errors: messages.error(request, f"{field}: {error}")
    else:
        form = AtividadeProfessorForm()

    return render(request, "professor/cadastrar_atividade.html", {
        "disciplina": disciplina,
        "turma": disciplina.turma,
        "form": form,
        "nome_exibicao": get_nome_exibicao(request.user),
        "foto_perfil_url": get_foto_perfil(request.user),
    })


@login_required
def lancar_notas_atividade(request, disciplina_id, atividade_id):
    """Lançamento de notas em massa para uma atividade específica."""
    disciplina = get_object_or_404(Disciplina, id=disciplina_id)
    atividade = get_object_or_404(AtividadeProfessor, id=atividade_id, disciplina=disciplina)
    
    eh_professor = hasattr(request.user, "professor") and disciplina.professor == request.user.professor
    if not (is_super_ou_gestor(request.user) or eh_professor):
        messages.error(request, "Acesso negado.")
        return redirect("listar_atividades", disciplina_id=disciplina.id)

    from apps.usuarios.models.perfis import Aluno
    from ..models.desempenho import NotaAtividade
    from ..models.academico import EntregaAtividade
    alunos = Aluno.objects.filter(turma=disciplina.turma).order_by("nome_completo")
    
    if request.method == "POST":
        for aluno in alunos:
            valor = request.POST.get(f"nota_{aluno.id}")
            obs = request.POST.get(f"obs_{aluno.id}", "")
            
            if valor:
                try:
                    valor_decimal = float(valor.replace(",", "."))
                    NotaAtividade.objects.update_or_create(
                        aluno=aluno,
                        atividade=atividade,
                        defaults={"valor": valor_decimal, "observacao": obs}
                    )
                except ValueError:
                    messages.error(request, f"Valor inválido para o aluno {aluno.nome_completo}")
        
        messages.success(request, "Notas salvas com sucesso!")
        return redirect("lancar_notas_atividade", disciplina_id=disciplina.id, atividade_id=atividade.id)

    notas_atuais = NotaAtividade.objects.filter(atividade=atividade)
    notas_dict = {n.aluno_id: n for n in notas_atuais}

    # Busca entregas dos alunos para o professor baixar
    entregas = EntregaAtividade.objects.filter(atividade=atividade)
    entregas_dict = {e.aluno_id: e for e in entregas}

    return render(request, "professor/lancar_notas_atividade.html", {
        "disciplina": disciplina,
        "atividade": atividade,
        "alunos": alunos,
        "notas_dict": notas_dict,
        "entregas_dict": entregas_dict,
        "nome_exibicao": get_nome_exibicao(request.user),
        "foto_perfil_url": get_foto_perfil(request.user),
    })

@login_required
def listar_atividades_aluno(request):
    """Lista as atividades da turma do aluno, separadas por tipo."""
    if not hasattr(request.user, "aluno"):
        messages.error(request, "Acesso exclusivo para alunos.")
        return redirect("painel_aluno")
    
    aluno = request.user.aluno
    atividades = AtividadeProfessor.objects.filter(disciplina__turma=aluno.turma).select_related("disciplina")
    
    # Coleta as entregas do aluno para estas atividades
    from ..models.academico import EntregaAtividade
    from ..models.desempenho import NotaAtividade
    entregas = EntregaAtividade.objects.filter(aluno=aluno)
    entregas_dict = {e.atividade_id: e for e in entregas}
    
    # Coleta as notas se existirem
    notas = NotaAtividade.objects.filter(aluno=aluno)
    notas_dict = {n.atividade_id: n for n in notas}
    
    # Agrupa por tipo para atender a solicitação do usuário
    return render(request, "aluno/atividades_aluno.html", {
        "trabalhos": atividades.filter(tipo="TRABALHO").order_by("data"),
        "atividades": atividades.filter(tipo="ATIVIDADE").order_by("data"),
        "provas": atividades.filter(tipo="PROVA").order_by("data"),
        "entregas_dict": entregas_dict,
        "notas_dict": notas_dict,
        "nome_exibicao": get_nome_exibicao(request.user),
        "foto_perfil_url": get_foto_perfil(request.user),
    })

from ..services.atividade_servico import AtividadeServico
from ..selectors.atividade_seletores import AtividadeSeletores

@login_required
def entregar_atividade(request, atividade_id):
    """Permite ao aluno realizar a entrega de um arquivo e/ou responder o quiz via Camada de Serviço."""
    if not hasattr(request.user, "aluno"):
        return redirect("painel_aluno")
        
    aluno = request.user.aluno
    atividade = get_object_or_404(AtividadeProfessor, id=atividade_id, disciplina__turma=aluno.turma)
    
    hoje = timezone.now()
    prazo_expirado = atividade.prazo_final and hoje > atividade.prazo_final
    
    entrega, _ = EntregaAtividade.objects.get_or_create(aluno=aluno, atividade=atividade)

    if request.method == "POST":
        try:
            AtividadeServico.processar_entrega_aluno(aluno, atividade.id, request.POST, request.FILES)
            messages.success(request, "Entrega salva com sucesso!")
            return redirect("listar_atividades_aluno")
        except ValueError as e:
            messages.error(request, str(e))
            return redirect("listar_atividades_aluno")

    respostas_atuais = {r.questao_id: r for r in entrega.respostas.all()}
    questoes = atividade.questoes.all().prefetch_related("alternativas")

    return render(request, "aluno/entregar_atividade.html", {
        "atividade": atividade,
        "entrega": entrega,
        "questoes": questoes,
        "respostas_atuais": respostas_atuais,
        "prazo_expirado": prazo_expirado,
        "exibir_gabarito": prazo_expirado,
        "nome_exibicao": get_nome_exibicao(request.user),
        "foto_perfil_url": get_foto_perfil(request.user),
    })

@login_required
def gerenciar_questoes(request, disciplina_id, atividade_id):
    """Permite ao professor gerenciar o banco de questões usando AtividadeServico."""
    disciplina = get_object_or_404(Disciplina, id=disciplina_id)
    atividade = get_object_or_404(AtividadeProfessor, id=atividade_id, disciplina=disciplina)
    
    if not (hasattr(request.user, "professor") and disciplina.professor == request.user.professor):
        messages.error(request, "Acesso negado.")
        return redirect("listar_atividades", disciplina_id=disciplina.id)

    if request.method == "POST":
        AtividadeServico.salvar_banco_questoes(atividade, request.POST)
        messages.success(request, "Questões salvas com sucesso!")
        return redirect("gerenciar_questoes", disciplina_id=disciplina.id, atividade_id=atividade.id)

    questoes = atividade.questoes.all().prefetch_related("alternativas")
    
    return render(request, "professor/gerenciar_questoes.html", {
        "disciplina": disciplina,
        "atividade": atividade,
        "questoes": questoes,
        "nome_exibicao": get_nome_exibicao(request.user),
        "foto_perfil_url": get_foto_perfil(request.user),
    })

@login_required
def corrigir_entrega(request, disciplina_id, atividade_id, entrega_id):
    """View de correção utilizando Seletores e Serviços para escalabilidade."""
    disciplina = get_object_or_404(Disciplina, id=disciplina_id)
    entrega = AtividadeSeletores.buscar_entrega_detalhada(entrega_id)
    atividade = entrega.atividade
    
    if not (hasattr(request.user, "professor") and disciplina.professor == request.user.professor):
        messages.error(request, "Acesso negado.")
        return redirect("lancar_notas_atividade", disciplina_id=disciplina.id, atividade_id=atividade.id)

    respostas = {r.questao_id: r for r in entrega.respostas.all()}

    if request.method == "POST":
        AtividadeServico.finalizar_correcao(entrega, request.POST)
        messages.success(request, f"Correção de {entrega.aluno.nome_completo} salva com sucesso!")
        return redirect("lancar_notas_atividade", disciplina_id=disciplina.id, atividade_id=atividade.id)

    return render(request, "professor/corrigir_entrega.html", {
        "disciplina": disciplina,
        "atividade": atividade,
        "entrega": entrega,
        "questoes": atividade.questoes.all(),
        "respostas": respostas,
        "nome_exibicao": get_nome_exibicao(request.user),
        "foto_perfil_url": get_foto_perfil(request.user),
    })

@login_required
@user_passes_test(is_super_ou_gestor)
def listar_turmas(request):
    """Lista turmas."""
    ano_atual = timezone.localtime(timezone.now()).year
    query = request.GET.get("q", "").strip()
    from apps.academico.utils.filtros import _get_anos_filtro
    anos_disponiveis = list(Turma.objects.values_list("ano", flat=True).distinct().order_by("-ano")) or [ano_atual]
    ano_filtro, anos_disponiveis = _get_anos_filtro(anos_disponiveis, request.GET.get("ano"), ano_atual)
    turmas = Turma.objects.filter(ano=ano_filtro)
    if query: turmas = turmas.filter(nome__icontains=query)
    return render(request, "turma/listar_turmas.html", {
        "turmas": turmas, "query": query, "ano_filtro": ano_filtro, "anos_disponiveis": anos_disponiveis, 
        "nome_exibicao": get_nome_exibicao(request.user), "foto_perfil_url": get_foto_perfil(request.user),
    })

@login_required
@user_passes_test(is_super_ou_gestor)
def cadastrar_turma(request):
    """Cria turma."""
    from datetime import datetime
    from ..forms.academico import TurmaForm
    ano_atual = datetime.now().year
    anos = list(range(2010, ano_atual + 2))
    
    if request.method == "POST":
        form = TurmaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Turma cadastrada com sucesso!")
            return redirect("listar_turmas")
    else:
        form = TurmaForm(initial={"ano": ano_atual})

    return render(request, "turma/cadastrar_turma.html", {
        "form": form,
        "anos": anos,
        "nome_exibicao": get_nome_exibicao(request.user),
        "foto_perfil_url": get_foto_perfil(request.user),
    })

@login_required
@user_passes_test(is_super_ou_gestor)
def editar_turma(request, turma_id):
    """Edita turma."""
    from datetime import datetime
    from ..forms.academico import TurmaForm
    turma = get_object_or_404(Turma, id=turma_id)
    ano_atual = datetime.now().year
    anos = list(range(2010, ano_atual + 2))

    if request.method == "POST":
        form = TurmaForm(request.POST, instance=turma)
        if form.is_valid():
            form.save()
            messages.success(request, "Turma atualizada com sucesso!")
            return redirect("listar_turmas")
    else:
        form = TurmaForm(instance=turma)

    return render(request, "turma/cadastrar_turma.html", {
        "turma": turma,
        "form": form,
        "anos": anos,
        "nome_exibicao": get_nome_exibicao(request.user),
        "foto_perfil_url": get_foto_perfil(request.user),
    })

@login_required
@user_passes_test(is_super_ou_gestor)
def excluir_turma(request, turma_id):
    """Remove turma."""
    turma = get_object_or_404(Turma, id=turma_id)
    nome = turma.nome
    turma.delete()
    messages.success(request, f"Turma {nome} removida.")
    return redirect("listar_turmas")
