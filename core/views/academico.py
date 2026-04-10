from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from ..models import Disciplina, Turma, Professor, Nota, GradeHorario
from ..forms import DisciplinaForm
from ..utils import (
    get_nome_exibicao, get_foto_perfil, NOMES_DIAS,
    _get_grade_horario_turma, _get_ocupados_por_professor,
    _calcular_detalhes_disciplina, is_super_ou_gestor
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
    from ..models import Aluno
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
    from ..utils import HORARIOS, DIAS_SEMANA
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
    from ..utils import _get_ano_filtro_professor
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
