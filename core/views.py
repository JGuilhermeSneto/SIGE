"""
Módulo de views da aplicação core do sistema SIGE.
"""

import calendar
from datetime import date, datetime

from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.timezone import now

from .forms import (
    AlunoForm,
    EditarPerfilForm,
    GestorForm,
    LoginForm,
    ProfessorForm,
)
from .models import (
    Aluno,
    Disciplina,
    Frequencia,
    Gestor,
    GradeHorario,
    Nota,
    Professor,
    Turma,
)


# =====================================================================
# Constantes
# =====================================================================

HORARIOS = {
    "manha": [
        "07:00 às 07:45", "07:45 às 08:30", "08:50 às 09:35",
        "09:35 às 10:20", "10:30 às 11:15", "11:15 às 12:00",
    ],
    "tarde": [
        "13:00 às 13:45", "13:45 às 14:30", "14:50 às 15:35",
        "15:35 às 16:20", "16:30 às 17:15", "17:15 às 18:00",
    ],
    "noite": [
        "19:00 às 19:45", "19:45 às 20:30", "20:40 às 21:25", "21:25 às 22:00",
    ],
}

DIAS_SEMANA = ["segunda", "terca", "quarta", "quinta", "sexta"]
NOMES_DIAS  = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]


# =====================================================================
# Funções Auxiliares
# =====================================================================


def is_superuser(user):
    return user.is_superuser


def is_super_ou_gestor(user):
    return user.is_superuser or hasattr(user, "gestor")


def get_foto_perfil(user):
    for tipo in ["professor", "aluno", "gestor", "superperfil"]:
        try:
            perfil = getattr(user, tipo, None)
            if perfil and getattr(perfil, "foto", None):
                return perfil.foto.url
        except (AttributeError, ValueError):
            pass
    return None


def get_nome_exibicao(user):
    for tipo in ["gestor", "professor", "aluno"]:
        perfil = getattr(user, tipo, None)
        if perfil and getattr(perfil, "nome_completo", None):
            return perfil.nome_completo
    nome = f"{user.first_name} {user.last_name}".strip()
    return nome if nome else user.email


def get_user_profile(user):
    for tipo in ["professor", "aluno", "gestor", "superperfil"]:
        perfil = getattr(user, tipo, None)
        if perfil:
            return perfil
    return None


def redirect_user(user):
    if user.is_superuser:
        return "painel_super"
    if hasattr(user, "professor"):
        return "painel_professor"
    if hasattr(user, "aluno"):
        return "painel_aluno"
    if hasattr(user, "gestor"):
        return "painel_super"
    return "login"


def gerar_calendario():
    hoje = datetime.today()
    cal = calendar.monthcalendar(hoje.year, hoje.month)
    celulas = []
    for semana in cal:
        for dia in semana:
            celulas.append({
                "numero": dia,
                "vazio": dia == 0,
                "hoje": dia == hoje.day,
            })
    return celulas


def _get_turno_key(turno):
    return turno.lower().replace("ã", "a").replace("á", "a")


def _get_anos_filtro(anos_disponiveis, ano_param, ano_atual):
    try:
        ano_filtro = int(ano_param) if ano_param else ano_atual
    except ValueError:
        ano_filtro = ano_atual
    if ano_filtro not in anos_disponiveis:
        anos_disponiveis = sorted(anos_disponiveis + [ano_filtro], reverse=True)
    return ano_filtro, anos_disponiveis


def _contar_notas_lancadas(nota):
    """
    FIX: model original tinha `valor`+`bimestre`; agora usa nota1–nota4.
    Conta quantas das quatro notas bimestrais foram lançadas (não nulas).
    """
    return sum(
        1 for campo in (nota.nota1, nota.nota2, nota.nota3, nota.nota4)
        if campo is not None
    )


def _calcular_detalhes_disciplina(disciplina, alunos_count):
    notas_disciplina = Nota.objects.filter(disciplina=disciplina)
    notas_lancadas = sum(_contar_notas_lancadas(n) for n in notas_disciplina)
    notas_possiveis = alunos_count * 4
    percentual = int(
        (notas_lancadas / notas_possiveis * 100) if notas_possiveis > 0 else 0
    )
    return {
        "disciplina": disciplina,
        "alunos_count": alunos_count,
        "notas_lancadas": notas_lancadas,
        "notas_possiveis": notas_possiveis,
        "percentual": percentual,
    }


def _formatar_grade(grade_obj, horarios):
    if not (horarios and grade_obj.dados):
        return None
    grade_formatada = {}
    for i, horario in enumerate(horarios):
        grade_formatada[horario] = {
            dia: (
                grade_obj.dados.get(dia, [])[i]
                if i < len(grade_obj.dados.get(dia, []))
                else ""
            )
            for dia in DIAS_SEMANA
        }
    return grade_formatada


def _get_grade_formatada(turma):
    try:
        grade_obj = GradeHorario.objects.get(turma=turma)
    except GradeHorario.DoesNotExist:
        return None
    turno_key = _get_turno_key(turma.turno)
    horarios = HORARIOS.get(turno_key, [])
    return _formatar_grade(grade_obj, horarios)


def _calcular_situacao_aluno(disciplinas_com_notas, total_lancadas, total_possiveis):
    if total_lancadas != total_possiveis or total_possiveis == 0:
        return "--", ""

    tem_reprovacao = False
    tem_recuperacao = False
    todas_aprovadas = True

    for item in disciplinas_com_notas:
        nota = item["nota"]
        if not nota or nota.media is None:
            todas_aprovadas = False
            continue
        if nota.media < 4:
            tem_reprovacao = True
            todas_aprovadas = False
        elif nota.media < 6:
            tem_recuperacao = True
            todas_aprovadas = False

    if tem_reprovacao:
        return "Reprovado", "reprovado"
    if tem_recuperacao:
        return "Recuperação", "recuperacao"
    if todas_aprovadas:
        return "Aprovado", "aprovado"
    return "--", ""


def _get_ocupados_por_professor(turma):
    ocupados = {}
    outras_grades = GradeHorario.objects.exclude(turma=turma)
    for grade in outras_grades:
        for dia in DIAS_SEMANA:
            for idx, nome_disc in enumerate(grade.dados.get(dia, [])):
                if not nome_disc:
                    continue
                try:
                    disc = Disciplina.objects.get(nome=nome_disc, turma=grade.turma)
                except Disciplina.DoesNotExist:
                    continue
                ocupados.setdefault(disc.professor_id, set()).add((dia, idx))
    return ocupados


def _is_gestor_ou_super(user):
    return user.is_superuser or hasattr(user, "gestor")


# =====================================================================
# Views — Autenticação
# =====================================================================


def login_view(request):
    if request.user.is_authenticated:
        return redirect(redirect_user(request.user))

    form = LoginForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect(redirect_user(user))

    return render(request, "auth/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")


# =====================================================================
# Views — Painel Principal
# =====================================================================


@login_required
@user_passes_test(is_super_ou_gestor)
def painel_super(request):
    ano_atual = datetime.now().year
    anos_disponiveis = list(
        Turma.objects.values_list("ano", flat=True).distinct().order_by("-ano")
    ) or [ano_atual]

    ano_filtro, anos_disponiveis = _get_anos_filtro(
        anos_disponiveis, request.GET.get("ano"), ano_atual
    )
    turmas = Turma.objects.filter(ano=ano_filtro)

    return render(
        request,
        "superusuario/painel_super.html",
        {
            "usuario": request.user,
            "nome_exibicao": get_nome_exibicao(request.user),
            "total_professores": (
                Professor.objects.filter(disciplinas__turma__in=turmas).distinct().count()
            ),
            "total_alunos": Aluno.objects.filter(turma__in=turmas).distinct().count(),
            "total_turmas": turmas.count(),
            "total_disciplinas": (
                Disciplina.objects.filter(turma__in=turmas).distinct().count()
            ),
            "foto_perfil_url": get_foto_perfil(request.user),
            "agora": datetime.now(),
            "calendario": gerar_calendario(),
            "anos_disponiveis": anos_disponiveis,
            "ano_filtro": ano_filtro,
        },
    )


# =====================================================================
# Views — Usuários
# =====================================================================


@login_required
def usuarios(request):
    pode_ver_gestores = request.user.is_superuser or (
        hasattr(request.user, "gestor")
        and request.user.gestor.cargo in ("diretor", "vice_diretor")
    )
    return render(
        request,
        "core/usuarios.html",
        {"pode_ver_gestores": pode_ver_gestores},
    )


# =====================================================================
# Views — Perfil do Usuário
# =====================================================================


@login_required
def editar_perfil(request):
    user = request.user
    perfil = get_user_profile(user)
    form = EditarPerfilForm(request.POST or None, instance=user)

    if request.method == "POST" and form.is_valid():
        user = form.save(commit=False)
        nova_senha = form.cleaned_data.get("nova_senha")
        if nova_senha:
            user.set_password(nova_senha)
            update_session_auth_hash(request, user)
        user.save()

        foto = request.FILES.get("foto")
        if perfil and foto:
            perfil.foto = foto
            perfil.save()

        messages.success(request, "Perfil atualizado com sucesso!")
        return redirect(redirect_user(user))

    if request.method == "POST":
        messages.error(request, "Corrija os erros abaixo.")

    foto_atual = None
    if perfil and getattr(perfil, "foto", None):
        foto_atual = perfil.foto.url

    return render(
        request,
        "core/editar_perfil.html",
        {
            "form": form,
            "perfil": perfil,
            "foto_atual": foto_atual,
            "foto_perfil_url": get_foto_perfil(user),
        },
    )


@login_required
def remover_foto_perfil(request):
    perfil = get_user_profile(request.user)
    if not perfil:
        messages.error(request, "Nenhum perfil associado ao usuário.")
        return redirect("editar_perfil")

    if getattr(perfil, "foto", None):
        perfil.foto.delete(save=False)
        perfil.foto = None
        perfil.save()

    messages.success(request, "Foto removida com sucesso!")
    return redirect("editar_perfil")


# =====================================================================
# Views — Professores
# =====================================================================


@login_required
@user_passes_test(lambda u: u.is_superuser or hasattr(u, "gestor"))
def listar_professores(request):
    query = request.GET.get("q", "")
    professores = (
        Professor.objects.filter(nome_completo__icontains=query)
        if query
        else Professor.objects.all()
    )
    return render(
        request,
        "professor/listar_professores.html",
        {"professores": professores, "query": query},
    )


@login_required
@user_passes_test(lambda u: u.is_superuser or hasattr(u, "gestor"))
def cadastrar_professor(request):
    if request.method == "POST":
        form = ProfessorForm(request.POST, request.FILES, request=request)
        if form.is_valid():
            professor = form.save()
            messages.success(
                request,
                f"Professor(a) {professor.nome_completo} cadastrado(a) com sucesso!",
            )
            return redirect("listar_professores")

        # FIX: exibe os erros field by field para facilitar diagnóstico
        for field, erros in form.errors.items():
            label = form.fields[field].label if field in form.fields else field
            for erro in erros:
                messages.error(request, f"{label}: {erro}")
    else:
        form = ProfessorForm(request=request)

    return render(
        request,
        "professor/cadastrar_professor.html",
        {"form": form, "professor": None},
    )


@login_required
@user_passes_test(lambda u: u.is_superuser or hasattr(u, "gestor"))
def editar_professor(request, professor_id):
    professor = get_object_or_404(Professor, id=professor_id)

    if request.method == "POST":
        form = ProfessorForm(
            request.POST, request.FILES, instance=professor, request=request
        )
        if form.is_valid():
            form.save()
            messages.success(
                request,
                f"Professor(a) {professor.nome_completo} atualizado(a) com sucesso!",
            )
            return redirect("listar_professores")

        for field, erros in form.errors.items():
            label = form.fields[field].label if field in form.fields else field
            for erro in erros:
                messages.error(request, f"{label}: {erro}")
    else:
        form = ProfessorForm(instance=professor, request=request)

    return render(
        request,
        "professor/cadastrar_professor.html",
        {"form": form, "professor": professor},
    )


@login_required
@user_passes_test(lambda u: u.is_superuser or hasattr(u, "gestor"))
def excluir_professor(request, professor_id):
    professor = get_object_or_404(Professor, id=professor_id)
    professor.user.delete()
    messages.success(request, "Professor removido com sucesso.")
    return redirect("listar_professores")


# =====================================================================
# Views — Gestores
# =====================================================================


@login_required
@user_passes_test(lambda u: u.is_superuser)
def cadastrar_editar_gestor(request, gestor_id=None):
    gestor = get_object_or_404(Gestor, id=gestor_id) if gestor_id else None

    if request.method == "POST":
        form = GestorForm(
            request.POST, request.FILES, instance=gestor, request=request
        )
        if form.is_valid():
            gestor = form.save()
            acao = "atualizado" if gestor_id else "cadastrado"
            messages.success(
                request,
                f"{gestor.get_cargo_display()} {gestor.nome_completo} {acao} com sucesso!",
            )
            return redirect("listar_gestores")

        # FIX: exibe erros com label legível
        for field, erros in form.errors.items():
            label = form.fields[field].label if field in form.fields else field
            for erro in erros:
                messages.error(request, f"{label}: {erro}")
    else:
        initial = {"email": gestor.user.email} if gestor and gestor.user else {}
        form = GestorForm(instance=gestor, initial=initial, request=request)

    return render(
        request,
        "gestor/cadastrar_gestor.html",
        {"form": form, "gestor": gestor},
    )


@login_required
@user_passes_test(lambda u: u.is_superuser)
def listar_gestores(request):
    query = request.GET.get("q", "")
    gestores = Gestor.objects.select_related("user").all()
    if query:
        gestores = gestores.filter(nome_completo__icontains=query)
    return render(
        request,
        "gestor/listar_gestores.html",
        {"gestores": gestores, "query": query},
    )


@login_required
@user_passes_test(lambda u: u.is_superuser)
def excluir_gestor(request, gestor_id):
    gestor = get_object_or_404(Gestor, id=gestor_id)
    if gestor.user:
        gestor.user.delete()
    else:
        gestor.delete()
    messages.success(request, "Gestor excluído com sucesso.")
    return redirect("listar_gestores")


# =====================================================================
# Views — Alunos
# =====================================================================


@login_required
@user_passes_test(lambda u: u.is_superuser or hasattr(u, "gestor"))
def listar_alunos(request):
    query = request.GET.get("q", "")
    alunos = (
        Aluno.objects.filter(nome_completo__icontains=query)
        if query
        else Aluno.objects.all()
    )
    return render(
        request,
        "aluno/listar_alunos.html",
        {"alunos": alunos, "query": query},
    )


@login_required
@user_passes_test(lambda u: u.is_superuser or hasattr(u, "gestor"))
def cadastrar_aluno(request):
    if request.method == "POST":
        form = AlunoForm(request.POST, request.FILES, request=request)
        if form.is_valid():
            aluno = form.save()
            messages.success(
                request,
                f"Aluno(a) {aluno.nome_completo} cadastrado(a) com sucesso!",
            )
            return redirect("listar_alunos")

        for field, erros in form.errors.items():
            label = form.fields[field].label if field in form.fields else field
            for erro in erros:
                messages.error(request, f"{label}: {erro}")
    else:
        form = AlunoForm(request=request)

    return render(request, "aluno/cadastrar_aluno.html", {"form": form, "aluno": None})


@login_required
@user_passes_test(lambda u: u.is_superuser or hasattr(u, "gestor"))
def editar_aluno(request, aluno_id):
    aluno = get_object_or_404(Aluno, id=aluno_id)

    if request.method == "POST":
        form = AlunoForm(
            request.POST, request.FILES, instance=aluno, request=request
        )
        if form.is_valid():
            aluno = form.save()
            messages.success(
                request,
                f"Aluno(a) {aluno.nome_completo} atualizado(a) com sucesso!",
            )
            return redirect("listar_alunos")

        for field, erros in form.errors.items():
            label = form.fields[field].label if field in form.fields else field
            for erro in erros:
                messages.error(request, f"{label}: {erro}")
    else:
        form = AlunoForm(instance=aluno, request=request)

    return render(
        request,
        "aluno/cadastrar_aluno.html",
        {"form": form, "aluno": aluno},
    )


@login_required
@user_passes_test(lambda u: u.is_superuser or hasattr(u, "gestor"))
def excluir_aluno(request, aluno_id):
    aluno = get_object_or_404(Aluno, id=aluno_id)
    aluno.user.delete()
    messages.success(request, "Aluno removido com sucesso.")
    return redirect("listar_alunos")


# =====================================================================
# Views — Turmas
# =====================================================================


@login_required
@user_passes_test(lambda u: u.is_superuser or hasattr(u, "gestor"))
def listar_turmas(request):
    ano_atual = timezone.localtime(timezone.now()).year
    query = request.GET.get("q", "").strip()
    anos_disponiveis = list(
        Turma.objects.values_list("ano", flat=True).distinct().order_by("-ano")
    ) or [ano_atual]

    ano_filtro, anos_disponiveis = _get_anos_filtro(
        anos_disponiveis, request.GET.get("ano"), ano_atual
    )

    turmas = Turma.objects.filter(ano=ano_filtro)
    if query:
        turmas = turmas.filter(nome__icontains=query)

    return render(
        request,
        "turma/listar_turmas.html",
        {
            "turmas": turmas,
            "query": query,
            "ano_filtro": ano_filtro,
            "anos_disponiveis": anos_disponiveis,
        },
    )


@login_required
@user_passes_test(lambda u: u.is_superuser or hasattr(u, "gestor"))
def cadastrar_turma(request):
    erro = None
    ano_atual = datetime.now().year
    anos = list(range(2010, ano_atual + 2))

    if request.method == "POST":
        nome = request.POST.get("nome")
        turno = request.POST.get("turno")
        ano = request.POST.get("ano")
        try:
            ano = int(ano)
        except (TypeError, ValueError):
            erro = "Ano letivo inválido."
        else:
            if ano < 2010 or ano > ano_atual + 1:
                erro = "O ano letivo deve estar entre 2010 e o próximo ano."
            elif Turma.objects.filter(nome=nome, ano=ano).exists():
                erro = "Essa turma já existe neste ano."
            else:
                Turma.objects.create(nome=nome, turno=turno, ano=ano)
                return redirect("listar_turmas")

    return render(request, "turma/cadastrar_turma.html", {"erro": erro, "anos": anos})


@login_required
@user_passes_test(lambda u: u.is_superuser or hasattr(u, "gestor"))
def editar_turma(request, turma_id):
    turma = get_object_or_404(Turma, id=turma_id)
    erro = None
    ano_atual = datetime.now().year
    anos = list(range(2010, ano_atual + 2))

    if request.method == "POST":
        nome = request.POST.get("nome")
        turno = request.POST.get("turno")
        ano = request.POST.get("ano")

        if Turma.objects.filter(nome=nome, ano=ano).exclude(id=turma.id).exists():
            erro = "Já existe outra turma com esse nome neste ano."
        else:
            turma.nome = nome
            turma.turno = turno
            turma.ano = ano
            turma.save()
            messages.success(request, "Turma atualizada com sucesso!")
            return redirect("listar_turmas")

    return render(
        request,
        "turma/cadastrar_turma.html",
        {"turma": turma, "erro": erro, "anos": anos},
    )


@login_required
@user_passes_test(
    lambda u: u.is_superuser
    or (hasattr(u, "gestor") and u.gestor.cargo != "secretario")
)
def excluir_turma(request, turma_id):
    turma = get_object_or_404(Turma, id=turma_id)
    turma.delete()
    messages.success(request, "Turma excluída com sucesso!")
    return redirect("listar_turmas")


# =====================================================================
# Views — Disciplinas
# =====================================================================


@login_required
def visualizar_disciplinas(request, disciplina_id):
    disciplina = get_object_or_404(Disciplina, id=disciplina_id)
    eh_professor_da_disc = (
        hasattr(request.user, "professor")
        and disciplina.professor == request.user.professor
    )

    if not (
        request.user.is_superuser
        or hasattr(request.user, "gestor")
        or eh_professor_da_disc
    ):
        messages.error(request, "Você não tem permissão para visualizar esta disciplina.")
        return redirect("login")

    turma = disciplina.turma
    alunos = Aluno.objects.filter(turma=turma).order_by("nome_completo")
    notas = Nota.objects.filter(disciplina=disciplina)
    notas_dict = {nota.aluno.id: nota for nota in notas}

    return render(
        request,
        "disciplina/visualizar_disciplinas.html",
        {
            "disciplina": disciplina,
            "turma": turma,
            "alunos": alunos,
            "notas": notas,
            "notas_dict": notas_dict,
            "is_gestor_ou_super": _is_gestor_ou_super(request.user),
        },
    )


@login_required
@user_passes_test(lambda u: u.is_superuser or hasattr(u, "gestor"))
def editar_disciplina(request, disciplina_id):
    disciplina = get_object_or_404(Disciplina, id=disciplina_id)
    professores = Professor.objects.filter(user__is_superuser=False)

    if request.method == "POST":
        disciplina.nome = request.POST["nome"]
        disciplina.professor = get_object_or_404(Professor, id=request.POST["professor"])
        disciplina.save()
        messages.success(request, "Disciplina atualizada com sucesso!")
        return redirect("disciplinas_turma", turma_id=disciplina.turma.id)

    return render(
        request,
        "disciplina/cadastrar_disciplina_turma.html",
        {
            "disciplina": disciplina,
            "turma": disciplina.turma,
            "professores": professores,
        },
    )


@login_required
@user_passes_test(lambda u: u.is_superuser or hasattr(u, "gestor"))
def excluir_disciplina(request, disciplina_id):
    disciplina = get_object_or_404(Disciplina, id=disciplina_id)
    turma_id = disciplina.turma.id
    disciplina.delete()
    messages.success(request, "Disciplina excluída com sucesso!")
    return redirect("disciplinas_turma", turma_id=turma_id)


@login_required
@user_passes_test(lambda u: u.is_superuser or hasattr(u, "gestor"))
def cadastrar_disciplina_para_turma(request, turma_id):
    turma = get_object_or_404(Turma, id=turma_id)

    if request.method == "POST":
        nome = request.POST.get("nome")
        professor_id = request.POST.get("professor")

        if not nome or not professor_id:
            messages.error(request, "Preencha todos os campos.")
        else:
            professor = get_object_or_404(Professor, id=professor_id)
            if Disciplina.objects.filter(nome=nome, turma=turma).exists():
                messages.error(request, "Essa disciplina já existe nesta turma.")
            else:
                Disciplina.objects.create(nome=nome, professor=professor, turma=turma)
                messages.success(request, "Disciplina cadastrada com sucesso!")
                return redirect("disciplinas_turma", turma_id=turma.id)

    professores = Professor.objects.filter(user__is_superuser=False)
    return render(
        request,
        "disciplina/cadastrar_disciplina_turma.html",
        {"turma": turma, "professores": professores},
    )


@login_required
@user_passes_test(lambda u: u.is_superuser or hasattr(u, "gestor"))
def listar_disciplinas_turma(request, turma_id):
    turma = get_object_or_404(Turma, id=turma_id)
    query = request.GET.get("q", "")
    disciplinas = Disciplina.objects.filter(turma=turma)
    if query:
        disciplinas = disciplinas.filter(nome__icontains=query)
    return render(
        request,
        "disciplina/listar_disciplinas_turma.html",
        {"turma": turma, "disciplinas": disciplinas, "query": query},
    )


@login_required
def disciplinas_turma(request, turma_id):
    user = request.user
    turma = get_object_or_404(Turma, id=turma_id)
    foto_perfil_url = get_foto_perfil(user)

    if not (user.is_superuser or hasattr(user, "gestor") or hasattr(user, "professor")):
        return redirect("login")

    if hasattr(user, "professor"):
        disciplinas = Disciplina.objects.filter(
            turma=turma, professor=user.professor
        ).order_by("nome")
    else:
        disciplinas = Disciplina.objects.filter(turma=turma).order_by("nome")

    if not disciplinas.exists():
        messages.error(request, "Nenhuma disciplina encontrada nesta turma.")
        return redirect(
            "disciplinas_professor" if hasattr(user, "professor") else "listar_turmas"
        )

    alunos_count = Aluno.objects.filter(turma=turma).count()
    disciplinas_detalhadas = [
        _calcular_detalhes_disciplina(d, alunos_count) for d in disciplinas
    ]

    return render(
        request,
        "professor/disciplinas_turma.html",
        {
            "turma": turma,
            "disciplinas_detalhadas": disciplinas_detalhadas,
            "foto_perfil_url": foto_perfil_url,
            "is_gestor_ou_super": _is_gestor_ou_super(user),
        },
    )


# =====================================================================
# Views — Painel do Professor
# =====================================================================


def _get_ano_filtro_professor(request, anos_disponiveis, ano_atual):
    ano_param = request.GET.get("ano")
    if ano_param:
        try:
            ano_filtro = int(ano_param)
            request.session["ano_filtro_professor"] = ano_filtro
        except ValueError:
            ano_filtro = request.session.get("ano_filtro_professor", ano_atual)
    else:
        ano_filtro = request.session.get("ano_filtro_professor", ano_atual)
    if ano_filtro not in anos_disponiveis:
        anos_disponiveis = sorted(anos_disponiveis + [ano_filtro], reverse=True)
    return ano_filtro, anos_disponiveis


def _acumular_notas_professor(disciplinas_filtradas):
    total_notas_possiveis = 0
    total_notas_lancadas = 0
    alunos_ids = set()
    disciplinas_detalhadas = []

    for disciplina in disciplinas_filtradas:
        alunos_count = Aluno.objects.filter(turma=disciplina.turma).count()
        alunos_ids.update(
            Aluno.objects.filter(turma=disciplina.turma).values_list("id", flat=True)
        )
        notas_disciplina = Nota.objects.filter(disciplina=disciplina)
        total_notas_possiveis += alunos_count * 4
        notas_lancadas_disc = sum(_contar_notas_lancadas(n) for n in notas_disciplina)
        total_notas_lancadas += notas_lancadas_disc
        notas_possiveis_disc = alunos_count * 4
        disciplinas_detalhadas.append({
            "disciplina": disciplina,
            "alunos_count": alunos_count,
            "notas_lancadas": notas_lancadas_disc,
            "notas_possiveis": notas_possiveis_disc,
            "percentual": int(
                (notas_lancadas_disc / notas_possiveis_disc * 100)
                if notas_possiveis_disc > 0 else 0
            ),
        })

    return total_notas_possiveis, total_notas_lancadas, len(alunos_ids), disciplinas_detalhadas


@login_required
def painel_professor(request):
    if not hasattr(request.user, "professor"):
        return redirect("login")

    professor = request.user.professor
    ano_atual = datetime.now().year
    disciplinas = Disciplina.objects.filter(professor=professor).select_related("turma")
    anos_disponiveis = list(
        Turma.objects.filter(disciplinas__professor=professor)
        .values_list("ano", flat=True)
        .distinct()
        .order_by("-ano")
    ) or [ano_atual]

    ano_filtro, anos_disponiveis = _get_ano_filtro_professor(
        request, anos_disponiveis, ano_atual
    )
    disciplinas_filtradas = disciplinas.filter(turma__ano=ano_filtro)
    (
        total_notas_possiveis,
        total_notas_lancadas,
        total_alunos,
        disciplinas_detalhadas,
    ) = _acumular_notas_professor(disciplinas_filtradas)

    return render(
        request,
        "professor/painel_professor.html",
        {
            "professor": professor,
            "nome_exibicao": professor.nome_completo,
            "total_disciplinas": disciplinas_filtradas.count(),
            "total_turmas": disciplinas_filtradas.values("turma").distinct().count(),
            "total_alunos": total_alunos,
            "total_notas_lancadas": total_notas_lancadas,
            "total_notas_possiveis": total_notas_possiveis,
            "disciplinas_detalhadas": disciplinas_detalhadas,
            "foto_perfil_url": get_foto_perfil(request.user),
            "agora": datetime.now(),
            "calendario": gerar_calendario(),
            "anos_disponiveis": anos_disponiveis,
            "ano_filtro": ano_filtro,
        },
    )


@login_required
def disciplinas_professor(request):
    if not hasattr(request.user, "professor"):
        return redirect("login")

    professor = request.user.professor
    foto_perfil_url = get_foto_perfil(request.user)
    ano_atual = datetime.now().year
    turmas_ids = (
        Disciplina.objects.filter(professor=professor)
        .values_list("turma_id", flat=True)
        .distinct()
    )
    anos_disponiveis = list(
        Turma.objects.filter(id__in=turmas_ids)
        .values_list("ano", flat=True)
        .distinct()
        .order_by("-ano")
    ) or [ano_atual]

    ano_filtro, anos_disponiveis = _get_ano_filtro_professor(
        request, anos_disponiveis, ano_atual
    )
    turmas = Turma.objects.filter(id__in=turmas_ids, ano=ano_filtro).order_by("nome")
    query = request.GET.get("q", "")
    if query:
        turmas = turmas.filter(nome__icontains=query)

    turmas_detalhadas = [
        {
            "turma": turma,
            "disciplinas_count": Disciplina.objects.filter(
                turma=turma, professor=professor
            ).count(),
            "alunos_count": Aluno.objects.filter(turma=turma).count(),
            "turno_display": turma.get_turno_display(),
        }
        for turma in turmas
    ]

    return render(
        request,
        "professor/disciplinas_professor.html",
        {
            "turmas_detalhadas": turmas_detalhadas,
            "foto_perfil_url": foto_perfil_url,
            "query": query,
            "anos_disponiveis": anos_disponiveis,
            "ano_filtro": ano_filtro,
        },
    )


@login_required
def visualizar_grade_professor(request, turma_id):
    if not hasattr(request.user, "professor"):
        return redirect("login")

    professor = request.user.professor
    turma = get_object_or_404(Turma, id=turma_id)
    disciplinas_prof = Disciplina.objects.filter(turma=turma, professor=professor)

    if not disciplinas_prof.exists():
        messages.error(request, "Você não leciona nenhuma disciplina nesta turma.")
        return redirect("disciplinas_professor")

    return render(
        request,
        "professor/visualizar_grade_professor.html",
        {
            "turma": turma,
            "grade_horario": _get_grade_formatada(turma),
            "disciplinas_professor": disciplinas_prof,
        },
    )


# =====================================================================
# Views — Lançamento de Notas
# =====================================================================


@login_required
@user_passes_test(
    lambda u: u.is_superuser or hasattr(u, "gestor") or hasattr(u, "professor")
)
def lancar_nota(request, disciplina_id):
    """
    FIX: model Nota agora tem nota1–nota4 em uma única linha por (aluno, disciplina).
    get_or_create sem bimestre — consistente com o novo modelo.
    """
    disciplina = get_object_or_404(Disciplina, id=disciplina_id)
    alunos = Aluno.objects.filter(turma_id=disciplina.turma_id).order_by("nome_completo")

    if request.method == "POST":
        for aluno in alunos:
            nota_obj, _ = Nota.objects.get_or_create(
                aluno_id=aluno.pk, disciplina_id=disciplina.id
            )
            for i in range(1, 5):
                campo = f"nota{i}_{aluno.pk}"
                valor = request.POST.get(campo, "").strip()
                if valor == "":
                    continue
                try:
                    valor_float = float(valor.replace(",", "."))
                    if valor_float < 0 or valor_float > 10:
                        raise ValueError("Nota fora do intervalo 0–10.")
                except ValueError as e:
                    messages.error(
                        request,
                        f'Nota inválida: "{valor}" para {aluno.nome_completo} (B{i}). {e}',
                    )
                    continue
                setattr(nota_obj, f"nota{i}", valor_float)
            nota_obj.save()

        messages.success(request, "Notas salvas com sucesso!")
        return redirect("lancar_nota", disciplina_id=disciplina.id)

    notas_dict = {
        n.aluno_id: n for n in Nota.objects.filter(disciplina_id=disciplina.id)
    }

    return render(
        request,
        "professor/lancar_nota.html",
        {
            "disciplina": disciplina,
            "alunos": alunos,
            "notas_dict": notas_dict,
            "is_gestor_ou_super": _is_gestor_ou_super(request.user),
        },
    )


# =====================================================================
# Views — Painel do Aluno
# =====================================================================


def _coletar_notas_aluno(aluno, disciplinas):
    disciplinas_com_notas = []
    soma_medias = 0
    total_com_media = 0
    total_lancadas = 0

    for disciplina in disciplinas:
        nota = Nota.objects.filter(aluno=aluno, disciplina=disciplina).first()
        if nota:
            total_lancadas += _contar_notas_lancadas(nota)

        freq_qs = Frequencia.objects.filter(aluno=aluno, disciplina=disciplina)
        total_aulas = freq_qs.count()
        presencas = freq_qs.filter(presente=True).count()
        faltas = total_aulas - presencas
        percentual_faltas = (
            round((faltas / total_aulas * 100), 1) if total_aulas > 0 else 0
        )

        disciplinas_com_notas.append({
            "disciplina": disciplina,
            "nota": nota,
            "total_aulas": total_aulas,
            "presencas": presencas,
            "faltas": faltas,
            "percentual_faltas": percentual_faltas,
        })

        # FIX: nota.media agora é uma @property no model corrigido
        if nota and nota.media is not None:
            soma_medias += nota.media
            total_com_media += 1

    media_geral = soma_medias / total_com_media if total_com_media > 0 else None
    return disciplinas_com_notas, media_geral, total_lancadas


@login_required
def painel_aluno(request):
    if not hasattr(request.user, "aluno"):
        return redirect("login")

    aluno = request.user.aluno
    disciplinas = Disciplina.objects.filter(turma=aluno.turma)
    total_possiveis = disciplinas.count() * 4
    disciplinas_com_notas, media_geral, total_lancadas = _coletar_notas_aluno(
        aluno, disciplinas
    )
    situacao_geral, situacao_classe = _calcular_situacao_aluno(
        disciplinas_com_notas, total_lancadas, total_possiveis
    )

    return render(
        request,
        "aluno/painel_aluno.html",
        {
            "aluno": aluno,
            "disciplinas_com_notas": disciplinas_com_notas,
            "media_geral": media_geral,
            "total_notas_lancadas": total_lancadas,
            "total_notas_possiveis": total_possiveis,
            "situacao_geral": situacao_geral,
            "situacao_classe": situacao_classe,
            "grade_horario": _get_grade_formatada(aluno.turma),
            "calendario": gerar_calendario(),
            "agora": datetime.now(),
        },
    )


# =====================================================================
# Views — Grade Horária
# =====================================================================


@login_required
def grade_horaria(request, turma_id):
    turma = get_object_or_404(Turma, id=turma_id)
    turno_key = _get_turno_key(turma.turno)
    horarios = HORARIOS.get(turno_key, []) or []
    grade_qs = GradeHorario.objects.filter(turma=turma).select_related(
        "disciplina", "professor"
    )
    disciplinas_da_turma = Disciplina.objects.filter(turma=turma)
    ocupados = _get_ocupados_por_professor(turma)

    if request.method == "POST":
        GradeHorario.objects.filter(turma=turma).delete()
        for dia in DIAS_SEMANA:
            for i, horario_inicio in enumerate(horarios):
                disciplina_id = request.POST.get(f"{dia}_{i}")
                if disciplina_id:
                    try:
                        disciplina = Disciplina.objects.get(id=disciplina_id)
                    except Disciplina.DoesNotExist:
                        continue
                    GradeHorario.objects.create(
                        turma=turma,
                        disciplina=disciplina,
                        professor=getattr(disciplina, "professor", None),
                        dia_semana=dia,
                        horario_inicio=horario_inicio,
                        horario_fim=horario_inicio,
                    )
        messages.success(request, "Grade atualizada com sucesso!")
        return redirect("grade_horaria", turma_id=turma.id)

    grade_dict = {dia: {} for dia in DIAS_SEMANA}
    for h in grade_qs:
        grade_dict[h.dia_semana][h.horario_inicio] = h

    rows = []
    for horario in horarios:
        row = {"horario": horario, "dias": []}
        for dia in DIAS_SEMANA:
            item = grade_dict[dia].get(horario)
            row["dias"].append({
                "disciplina": item.disciplina if item else None,
                "id": item.disciplina.id if item and item.disciplina else "",
            })
        rows.append(row)

    return render(
        request,
        "core/grade_horaria.html",
        {
            "turma": turma,
            "nomes_dias": NOMES_DIAS,
            "rows": rows,
            "disciplinas": disciplinas_da_turma,
            "is_gestor_ou_super": _is_gestor_ou_super(request.user),
        },
    )


# =====================================================================
# Views — Frequência
# =====================================================================


@login_required
def lancar_chamada(request, disciplina_id):
    """FIX: campo correto é `observacao`, não `justificativa` (que não existe no model)."""
    disciplina = get_object_or_404(Disciplina, id=disciplina_id)

    if not (request.user.is_superuser or hasattr(request.user, "gestor")):
        if disciplina.professor.user != request.user:
            messages.error(request, "Você não tem permissão para acessar esta chamada.")
            return redirect("disciplinas_professor")

    data_str = request.GET.get("data") or request.POST.get("data")
    try:
        data_selecionada = date.fromisoformat(data_str) if data_str else date.today()
    except ValueError:
        data_selecionada = date.today()

    alunos = disciplina.turma.alunos.order_by("nome_completo")
    frequencias_existentes = {
        f.aluno_id: f
        for f in Frequencia.objects.filter(disciplina=disciplina, data=data_selecionada)
    }

    if request.method == "POST":
        for aluno in alunos:
            presente = str(aluno.id) in request.POST.getlist("presentes")
            # FIX: campo correto é `observacao` (não `justificativa`)
            observacao = request.POST.get(f"observacao_{aluno.id}", "").strip()
            if presente:
                observacao = ""

            Frequencia.objects.update_or_create(
                aluno=aluno,
                disciplina=disciplina,
                data=data_selecionada,
                defaults={
                    "presente": presente,
                    "observacao": observacao,   # FIX: era "justificativa"
                },
            )

        messages.success(
            request,
            f"Chamada do dia {data_selecionada.strftime('%d/%m/%Y')} salva com sucesso.",
        )
        return redirect("lancar_chamada", disciplina_id=disciplina_id)

    return render(
        request,
        "frequencia/lancar_chamada.html",
        {
            "disciplina": disciplina,
            "alunos": alunos,
            "data_selecionada": data_selecionada,
            "frequencias_existentes": frequencias_existentes,
        },
    )


@login_required
def historico_frequencia(request, disciplina_id):
    disciplina = get_object_or_404(Disciplina, id=disciplina_id)

    if not (request.user.is_superuser or hasattr(request.user, "gestor")):
        if disciplina.professor.user != request.user:
            messages.error(request, "Você não tem permissão para acessar este histórico.")
            return redirect("disciplinas_professor")

    datas = (
        Frequencia.objects.filter(disciplina=disciplina)
        .values_list("data", flat=True)
        .distinct()
        .order_by("-data")
    )

    resumo_por_data = []
    for data in datas:
        registros = Frequencia.objects.filter(disciplina=disciplina, data=data)
        total = registros.count()
        presencas = registros.filter(presente=True).count()
        faltas = total - presencas
        resumo_por_data.append({
            "data": data,
            "total": total,
            "presencas": presencas,
            "faltas": faltas,
        })

    return render(
        request,
        "frequencia/historico_frequencia.html",
        {"disciplina": disciplina, "resumo_por_data": resumo_por_data},
    )


@login_required
def frequencia_aluno(request):
    if not hasattr(request.user, "aluno"):
        messages.error(request, "Apenas alunos podem acessar a frequência.")
        return redirect("painel_super")

    aluno = request.user.aluno
    frequencias = (
        Frequencia.objects.filter(aluno=aluno)
        .values("disciplina__nome")
        .annotate(
            total_aulas=Count("id"),
            presencas=Count("id", filter=Q(presente=True)),
            faltas=Count("id", filter=Q(presente=False)),
        )
        .order_by("disciplina__nome")
    )

    return render(
        request,
        "frequencia/frequencia_aluno.html",
        {"aluno": aluno, "frequencias": frequencias},
    )


# =====================================================================
# Views — Painel Administrativo de Usuários
# =====================================================================


def painel_usuarios(request):
    """
    FIX: removidas referências aos campos `ativo` e `data_criacao` que não
    existem nos models Aluno, Professor e Gestor. Substituído por contagens simples.
    """
    context = {
        "total_usuarios":   User.objects.count(),
        "total_alunos":     Aluno.objects.count(),
        "total_professores": Professor.objects.count(),
        "total_gestores":   Gestor.objects.count(),
    }
    return render(request, "usuarios/usuarios.html", context)