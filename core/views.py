import calendar
from datetime import datetime
import unicodedata

from django.contrib import messages
from django.contrib.auth import (authenticate, login, logout,
                                 update_session_auth_hash)
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import (AlunoForm, DisciplinaForm, EditarPerfilForm, GestorForm,
                    LoginForm, NotaForm, ProfessorForm, TurmaForm)
from .models import Aluno, Disciplina, Gestor, GradeHorario, Nota, Professor, Turma


# ======================== HORÁRIOS ========================
HORARIOS = {
    "manha": [
        "07:00 às 07:45",
        "07:45 às 08:30",
        "08:50 às 09:35",
        "09:35 às 10:20",
        "10:30 às 11:15",
        "11:15 às 12:00",
    ],
    "tarde": [
        "13:00 às 13:45",
        "13:45 às 14:30",
        "14:50 às 15:35",
        "15:35 às 16:20",
        "16:30 às 17:15",
        "17:15 às 18:00",
    ],
    "noite": [
        "19:00 às 19:45",
        "19:45 às 20:30",
        "20:40 às 21:25",
        "21:25 às 22:00",
    ],
}


# ======================== HELPERS ========================
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
    elif hasattr(user, "professor"):
        return "painel_professor"
    elif hasattr(user, "aluno"):
        return "painel_aluno"
    elif hasattr(user, "gestor"):
        return "painel_super"
    return "login"


def gerar_calendario():
    hoje = datetime.today()
    cal = calendar.monthcalendar(hoje.year, hoje.month)
    celulas = []
    for semana in cal:
        for dia in semana:
            celulas.append(
                {
                    "numero": dia,
                    "vazio": dia == 0,
                    "hoje": dia == hoje.day,
                }
            )
    return celulas


# ======================== LOGIN / LOGOUT ========================
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


# ======================== PAINEL SUPER ========================
@login_required
@user_passes_test(is_super_ou_gestor)
def painel_super(request):
    ano_atual = datetime.now().year

    anos_disponiveis_qs = (
        Turma.objects.values_list("ano", flat=True).distinct().order_by("-ano")
    )
    anos_disponiveis = list(anos_disponiveis_qs)

    if not anos_disponiveis:
        anos_disponiveis = [ano_atual]

    ano_filtro = request.GET.get("ano")
    try:
        ano_filtro = int(ano_filtro) if ano_filtro else ano_atual
    except ValueError:
        ano_filtro = ano_atual

    if ano_filtro not in anos_disponiveis:
        anos_disponiveis.append(ano_filtro)
        anos_disponiveis.sort(reverse=True)

    turmas = Turma.objects.filter(ano=ano_filtro)

    total_turmas = turmas.count()
    total_alunos = Aluno.objects.filter(turma__in=turmas).distinct().count()
    total_professores = Professor.objects.filter(disciplina__turma__in=turmas).distinct().count()
    total_disciplinas = Disciplina.objects.filter(turma__in=turmas).distinct().count()
    foto_perfil_url = get_foto_perfil(request.user)

    return render(
        request,
        "superusuario/painel_super.html",
        {
            "usuario": request.user,
            "nome_exibicao": get_nome_exibicao(request.user),
            "total_professores": total_professores,
            "total_alunos": total_alunos,
            "total_turmas": total_turmas,
            "total_disciplinas": total_disciplinas,
            "foto_perfil_url": foto_perfil_url,
            "agora": datetime.now(),
            "calendario": gerar_calendario(),
            "anos_disponiveis": anos_disponiveis,
            "ano_filtro": ano_filtro,
        },
    )


# ========================== USUÁRIOS ==========================
@login_required
def usuarios(request):
    pode_ver_gestores = False

    if request.user.is_superuser:
        pode_ver_gestores = True
    elif hasattr(request.user, "gestor"):
        if request.user.gestor.cargo in ("diretor", "vice_diretor"):
            pode_ver_gestores = True

    return render(
        request, "core/usuarios.html", {"pode_ver_gestores": pode_ver_gestores}
    )


# ======================== PERFIL ========================
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


# ========================== PROFESSORES ==========================
@login_required
@user_passes_test(lambda u: u.is_superuser or hasattr(u, "gestor"))
def listar_professores(request):
    query = request.GET.get("q", "")

    if query:
        professores = Professor.objects.filter(nome_completo__icontains=query)
    else:
        professores = Professor.objects.all()

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
        else:
            for campo, erros in form.errors.items():
                for erro in erros:
                    messages.error(request, erro)
    else:
        form = ProfessorForm(request=request)

    return render(request, "professor/cadastrar_professor.html", {"form": form})


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
        else:
            for campo, erros in form.errors.items():
                for erro in erros:
                    messages.error(request, erro)
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
    messages.success(request, "Professor removido.")
    return redirect("listar_professores")


# ========================== GESTOR ==========================
@login_required
@user_passes_test(lambda u: u.is_superuser)
def cadastrar_gestor(request):
    if request.method == "POST":
        form = GestorForm(request.POST, request.FILES, request=request)
        if form.is_valid():
            gestor = form.save()
            messages.success(
                request,
                f"{gestor.get_cargo_display()} {gestor.nome_completo} cadastrado com sucesso!",
            )
            return redirect("listar_gestores")
        else:
            for campo, erros in form.errors.items():
                for erro in erros:
                    messages.error(request, erro)
    else:
        form = GestorForm(request=request)

    return render(request, "gestor/cadastrar_gestor.html", {"form": form})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def listar_gestores(request):
    gestores = Gestor.objects.select_related("user").all()
    return render(request, "gestor/listar_gestores.html", {"gestores": gestores})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def excluir_gestor(request, gestor_id):
    gestor = get_object_or_404(Gestor, id=gestor_id)
    gestor.user.delete()
    messages.success(request, "Gestor excluído com sucesso.")
    return redirect("listar_gestores")


@login_required
@user_passes_test(lambda u: u.is_superuser)
def editar_gestor(request, gestor_id):
    gestor = get_object_or_404(Gestor, id=gestor_id)
    user = gestor.user

    if request.method == "POST":
        form = GestorForm(request.POST, request.FILES, instance=gestor, request=request)
        if form.is_valid():
            form.save()
            nova_senha = form.cleaned_data.get("senha")
            if nova_senha:
                user.set_password(nova_senha)
                user.save()
            messages.success(request, "Gestor atualizado com sucesso!")
            return redirect("listar_gestores")
        else:
            messages.error(request, "Corrija os erros abaixo.")
    else:
        form = GestorForm(instance=gestor, initial={"email": user.email})

    return render(
        request, "gestor/cadastrar_gestor.html", {"form": form, "gestor": gestor}
    )


# ========================== ALUNO ==========================
@login_required
@user_passes_test(lambda u: u.is_superuser or hasattr(u, "gestor"))
def listar_alunos(request):
    query = request.GET.get("q", "")

    if query:
        alunos = Aluno.objects.filter(nome_completo__icontains=query)
    else:
        alunos = Aluno.objects.all()

    return render(
        request, "aluno/listar_alunos.html", {"alunos": alunos, "query": query}
    )


@login_required
@user_passes_test(lambda u: u.is_superuser or hasattr(u, "gestor"))
def cadastrar_aluno(request):
    if request.method == "POST":
        form = AlunoForm(request.POST, request.FILES, request=request)
        if form.is_valid():
            aluno = form.save()
            messages.success(
                request, f"Aluno(a) {aluno.nome_completo} cadastrado(a) com sucesso!"
            )
            return redirect("listar_alunos")
        else:
            for campo, erros in form.errors.items():
                for erro in erros:
                    messages.error(request, erro)
    else:
        form = AlunoForm(request=request)

    return render(request, "aluno/cadastrar_aluno.html", {"form": form})


@login_required
@user_passes_test(lambda u: u.is_superuser or hasattr(u, "gestor"))
def editar_aluno(request, aluno_id):
    aluno = get_object_or_404(Aluno, id=aluno_id)

    if request.method == "POST":
        form = AlunoForm(request.POST, request.FILES, instance=aluno, request=request)
        if form.is_valid():
            aluno = form.save()
            messages.success(
                request, f"Aluno(a) {aluno.nome_completo} atualizado(a) com sucesso!"
            )
            return redirect("listar_alunos")
        else:
            for campo, erros in form.errors.items():
                for erro in erros:
                    messages.error(request, erro)
    else:
        form = AlunoForm(instance=aluno, request=request)

    return render(
        request, "aluno/cadastrar_aluno.html", {"form": form, "aluno": aluno}
    )


@login_required
@user_passes_test(lambda u: u.is_superuser or hasattr(u, "gestor"))
def excluir_aluno(request, aluno_id):
    aluno = get_object_or_404(Aluno, id=aluno_id)
    aluno.user.delete()
    messages.success(request, "Aluno removido.")
    return redirect("listar_alunos")


# ========================== TURMAS ==========================
@login_required
@user_passes_test(lambda u: u.is_superuser or hasattr(u, "gestor"))
def listar_turmas(request):
    ano_atual = timezone.localtime(timezone.now()).year
    query = request.GET.get("q", "").strip()

    anos_disponiveis_qs = (
        Turma.objects.values_list("ano", flat=True).distinct().order_by("-ano")
    )
    anos_disponiveis = list(anos_disponiveis_qs)

    if not anos_disponiveis:
        anos_disponiveis = [ano_atual]

    ano_filtro = request.GET.get("ano")
    try:
        ano_filtro = int(ano_filtro) if ano_filtro else ano_atual
    except ValueError:
        ano_filtro = ano_atual

    if ano_filtro not in anos_disponiveis:
        anos_disponiveis.append(ano_filtro)
        anos_disponiveis.sort(reverse=True)

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
                erro = "O ano letivo deve ser entre 2010 e o próximo ano."
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

    return render(request, "turma/cadastrar_turma.html", {"turma": turma, "erro": erro, "anos": anos})


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


# ========================== DISCIPLINAS ==========================
@login_required
def visualizar_disciplinas(request, disciplina_id):
    disciplina = get_object_or_404(Disciplina, id=disciplina_id)

    if not (
        request.user.is_superuser
        or hasattr(request.user, "gestor")
        or (
            hasattr(request.user, "professor")
            and disciplina.professor == request.user.professor
        )
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
        },
    )


@login_required
@user_passes_test(lambda u: u.is_superuser or hasattr(u, "gestor"))
def editar_disciplina(request, disciplina_id):
    disciplina = get_object_or_404(Disciplina, id=disciplina_id)
    professores = Professor.objects.filter(user__is_superuser=False)  # ✅ definido aqui

    if request.method == "POST":
        disciplina.nome = request.POST["nome"]
        disciplina.professor = get_object_or_404(
            Professor, id=request.POST["professor"]
        )
        disciplina.save()
        messages.success(request, "Disciplina atualizada com sucesso!")
        return redirect("disciplinas_turma", turma_id=disciplina.turma.id)  # ✅ nome correto

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
    return redirect("disciplinas_turma", turma_id=turma_id)  # ✅ nome correto


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
                return redirect("disciplinas_turma", turma_id=turma.id)  # ✅ nome correto

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
        disciplinas = Disciplina.objects.filter(turma=turma, professor=user.professor).order_by("nome")
    else:
        disciplinas = Disciplina.objects.filter(turma=turma).order_by("nome")

    if not disciplinas.exists():
        messages.error(request, "Nenhuma disciplina encontrada nesta turma.")
        if hasattr(user, "professor"):
            return redirect("disciplinas_professor")
        return redirect("listar_turmas")

    alunos_count = Aluno.objects.filter(turma=turma).count()
    disciplinas_detalhadas = []

    for disciplina in disciplinas:
        notas_disciplina = Nota.objects.filter(disciplina=disciplina)
        notas_lancadas_disc = 0

        for nota in notas_disciplina:
            if nota.nota1 is not None:
                notas_lancadas_disc += 1
            if nota.nota2 is not None:
                notas_lancadas_disc += 1
            if nota.nota3 is not None:
                notas_lancadas_disc += 1
            if nota.nota4 is not None:
                notas_lancadas_disc += 1

        notas_possiveis_disc = alunos_count * 4

        disciplinas_detalhadas.append(
            {
                "disciplina": disciplina,
                "alunos_count": alunos_count,
                "notas_lancadas": notas_lancadas_disc,
                "notas_possiveis": notas_possiveis_disc,
                "percentual": int(
                    (notas_lancadas_disc / notas_possiveis_disc * 100)
                    if notas_possiveis_disc > 0
                    else 0
                ),
            }
        )

    return render(
        request,
        "professor/disciplinas_turma.html",
        {
            "turma": turma,
            "disciplinas_detalhadas": disciplinas_detalhadas,
            "foto_perfil_url": foto_perfil_url,
        },
    )


# ======================== PAINEL PROFESSOR ========================
@login_required
def painel_professor(request):
    if not hasattr(request.user, "professor"):
        return redirect("login")

    professor = request.user.professor
    foto_perfil_url = get_foto_perfil(request.user)
    disciplinas = Disciplina.objects.filter(professor=professor).select_related("turma")

    anos_disponiveis_qs = (
        Turma.objects.filter(disciplina__professor=professor)
        .values_list("ano", flat=True)
        .distinct()
        .order_by("-ano")
    )
    anos_disponiveis = list(anos_disponiveis_qs)
    ano_atual = datetime.now().year

    if not anos_disponiveis:
        anos_disponiveis = [ano_atual]

    ano_filtro = request.GET.get("ano")
    if ano_filtro:
        try:
            ano_filtro = int(ano_filtro)
            request.session["ano_filtro_professor"] = ano_filtro
        except ValueError:
            ano_filtro = request.session.get("ano_filtro_professor", ano_atual)
    else:
        ano_filtro = request.session.get("ano_filtro_professor", ano_atual)

    if ano_filtro not in anos_disponiveis:
        anos_disponiveis.append(ano_filtro)
        anos_disponiveis.sort(reverse=True)

    disciplinas_filtradas = disciplinas.filter(turma__ano=ano_filtro)
    total_disciplinas = disciplinas_filtradas.count()
    total_turmas = disciplinas_filtradas.values("turma").distinct().count()

    alunos_ids = set()
    for disciplina in disciplinas_filtradas:
        alunos_turma = Aluno.objects.filter(turma=disciplina.turma).values_list("id", flat=True)
        alunos_ids.update(alunos_turma)
    total_alunos = len(alunos_ids)

    total_notas_possiveis = 0
    total_notas_lancadas = 0

    disciplinas_detalhadas = []
    for disciplina in disciplinas_filtradas:
        alunos_count = Aluno.objects.filter(turma=disciplina.turma).count()
        notas_disciplina = Nota.objects.filter(disciplina=disciplina)
        total_notas_possiveis += alunos_count * 4

        notas_lancadas_disc = 0
        for nota in notas_disciplina:
            if nota.nota1 is not None:
                notas_lancadas_disc += 1
                total_notas_lancadas += 1
            if nota.nota2 is not None:
                notas_lancadas_disc += 1
                total_notas_lancadas += 1
            if nota.nota3 is not None:
                notas_lancadas_disc += 1
                total_notas_lancadas += 1
            if nota.nota4 is not None:
                notas_lancadas_disc += 1
                total_notas_lancadas += 1

        notas_possiveis_disc = alunos_count * 4
        disciplinas_detalhadas.append(
            {
                "disciplina": disciplina,
                "alunos_count": alunos_count,
                "notas_lancadas": notas_lancadas_disc,
                "notas_possiveis": notas_possiveis_disc,
                "percentual": int(
                    (notas_lancadas_disc / notas_possiveis_disc * 100)
                    if notas_possiveis_disc > 0
                    else 0
                ),
            }
        )

    return render(
        request,
        "professor/painel_professor.html",
        {
            "professor": professor,
            "nome_exibicao": professor.nome_completo,
            "total_disciplinas": total_disciplinas,
            "total_turmas": total_turmas,
            "total_alunos": total_alunos,
            "total_notas_lancadas": total_notas_lancadas,
            "total_notas_possiveis": total_notas_possiveis,
            "disciplinas_detalhadas": disciplinas_detalhadas,
            "foto_perfil_url": foto_perfil_url,
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

    turmas_ids = (
        Disciplina.objects.filter(professor=professor)
        .values_list("turma_id", flat=True)
        .distinct()
    )

    anos_disponiveis_qs = (
        Turma.objects.filter(id__in=turmas_ids)
        .values_list("ano", flat=True)
        .distinct()
        .order_by("-ano")
    )
    anos_disponiveis = list(anos_disponiveis_qs)
    ano_atual = datetime.now().year

    if not anos_disponiveis:
        anos_disponiveis = [ano_atual]

    ano_filtro = request.GET.get("ano")
    if ano_filtro:
        try:
            ano_filtro = int(ano_filtro)
            request.session["ano_filtro_professor"] = ano_filtro
        except ValueError:
            ano_filtro = request.session.get("ano_filtro_professor", ano_atual)
    else:
        ano_filtro = request.session.get("ano_filtro_professor", ano_atual)

    if ano_filtro not in anos_disponiveis:
        anos_disponiveis.append(ano_filtro)
        anos_disponiveis.sort(reverse=True)

    turmas = Turma.objects.filter(id__in=turmas_ids, ano=ano_filtro).order_by("nome")

    query = request.GET.get("q", "")
    if query:
        turmas = turmas.filter(nome__icontains=query)

    turmas_detalhadas = []
    for turma in turmas:
        disciplinas_da_turma = Disciplina.objects.filter(turma=turma, professor=professor)
        alunos_count = Aluno.objects.filter(turma=turma).count()
        turmas_detalhadas.append(
            {
                "turma": turma,
                "disciplinas_count": disciplinas_da_turma.count(),
                "alunos_count": alunos_count,
                "turno_display": turma.get_turno_display(),
            }
        )

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

    turno_key = turma.turno.lower().replace("ã", "a").replace("á", "a")
    horarios = HORARIOS.get(turno_key, [])
    grade_formatada = None

    try:
        grade_obj = GradeHorario.objects.get(turma=turma)

        if horarios and grade_obj.dados:
            grade_formatada = {}
            for i, horario in enumerate(horarios):
                grade_formatada[horario] = {
                    dia: (
                        grade_obj.dados.get(dia, [])[i]
                        if i < len(grade_obj.dados.get(dia, []))
                        else ""
                    )
                    for dia in ["segunda", "terca", "quarta", "quinta", "sexta"]
                }

    except GradeHorario.DoesNotExist:
        grade_formatada = None

    return render(
        request,
        "professor/visualizar_grade_professor.html",
        {
            "turma": turma,
            "grade_horario": grade_formatada,
            "disciplinas_professor": disciplinas_prof,
        },
    )


# ======================== LANÇAR NOTA ========================
@login_required
@user_passes_test(
    lambda u: u.is_superuser or hasattr(u, "gestor") or hasattr(u, "professor")
)
def lancar_nota(request, disciplina_id):
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
                except ValueError:
                    messages.error(
                        request,
                        f'Nota inválida: "{valor}" para {aluno.nome_completo} (B{i}).',
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
        },
    )


# ======================== PAINEL ALUNO ========================
@login_required
def painel_aluno(request):
    if not hasattr(request.user, "aluno"):
        return redirect("login")

    aluno = request.user.aluno
    disciplinas = Disciplina.objects.filter(turma=aluno.turma)

    disciplinas_com_notas = []
    soma_medias = 0
    total_disciplinas_com_media = 0
    total_notas_lancadas = 0
    total_notas_possiveis = disciplinas.count() * 4

    tem_reprovacao = False
    tem_recuperacao = False
    todas_aprovadas = True

    for disciplina in disciplinas:
        nota = Nota.objects.filter(aluno=aluno, disciplina=disciplina).first()

        if nota:
            if nota.nota1 is not None:
                total_notas_lancadas += 1
            if nota.nota2 is not None:
                total_notas_lancadas += 1
            if nota.nota3 is not None:
                total_notas_lancadas += 1
            if nota.nota4 is not None:
                total_notas_lancadas += 1

        disciplinas_com_notas.append({"disciplina": disciplina, "nota": nota})

        if nota and nota.media:
            soma_medias += nota.media
            total_disciplinas_com_media += 1

            if nota.media < 4:
                tem_reprovacao = True
                todas_aprovadas = False
            elif nota.media < 6:
                tem_recuperacao = True
                todas_aprovadas = False
        else:
            todas_aprovadas = False

    media_geral = (
        soma_medias / total_disciplinas_com_media
        if total_disciplinas_com_media > 0
        else None
    )

    if total_notas_lancadas == total_notas_possiveis and total_notas_possiveis > 0:
        if tem_reprovacao:
            situacao_geral = "Reprovado"
            situacao_classe = "reprovado"
        elif tem_recuperacao:
            situacao_geral = "Recuperação"
            situacao_classe = "recuperacao"
        elif todas_aprovadas:
            situacao_geral = "Aprovado"
            situacao_classe = "aprovado"
        else:
            situacao_geral = "--"
            situacao_classe = ""
    else:
        situacao_geral = "--"
        situacao_classe = ""

    grade_formatada = None
    try:
        grade_obj = GradeHorario.objects.get(turma=aluno.turma)
        turno_key = aluno.turma.turno.lower().replace("ã", "a").replace("á", "a")
        horarios = HORARIOS.get(turno_key, [])

        if horarios and grade_obj.dados:
            grade_formatada = {}
            for i, horario in enumerate(horarios):
                grade_formatada[horario] = {
                    dia: (
                        grade_obj.dados.get(dia, [])[i]
                        if i < len(grade_obj.dados.get(dia, []))
                        else ""
                    )
                    for dia in ["segunda", "terca", "quarta", "quinta", "sexta"]
                }

    except GradeHorario.DoesNotExist:
        grade_formatada = None

    calendario = gerar_calendario()
    agora = datetime.now()

    return render(
        request,
        "aluno/painel_aluno.html",
        {
            "aluno": aluno,
            "disciplinas_com_notas": disciplinas_com_notas,
            "media_geral": media_geral,
            "total_notas_lancadas": total_notas_lancadas,
            "total_notas_possiveis": total_notas_possiveis,
            "situacao_geral": situacao_geral,
            "situacao_classe": situacao_classe,
            "grade_horario": grade_formatada,
            "calendario": calendario,
            "agora": agora,
        },
    )


# ======================== GRADE HORÁRIA ========================
@login_required
def grade_horaria(request, turma_id):
    turma = get_object_or_404(Turma, id=turma_id)
    grade, criado = GradeHorario.objects.get_or_create(turma=turma)

    dias = ["segunda", "terca", "quarta", "quinta", "sexta"]
    nomes_dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]

    turno_key = turma.turno.lower().replace("ã", "a").replace("á", "a")
    horarios = HORARIOS.get(turno_key, [])

    if not horarios:
        messages.error(request, "Turno inválido nesta turma.")
        horarios = [""]

    if not grade.dados:
        grade.dados = {dia: [""] * len(horarios) for dia in dias}
        grade.save()

    disciplinas_da_turma = Disciplina.objects.filter(turma=turma)

    ocupados = {}
    outras_grades = GradeHorario.objects.exclude(turma=turma)

    for g in outras_grades:
        for dia in dias:
            lista = g.dados.get(dia, [])
            for idx, nome_disciplina in enumerate(lista):
                if not nome_disciplina:
                    continue
                try:
                    disc = Disciplina.objects.get(nome=nome_disciplina, turma=g.turma)
                except Disciplina.DoesNotExist:
                    continue
                prof_id = disc.professor_id
                if prof_id not in ocupados:
                    ocupados[prof_id] = set()
                ocupados[prof_id].add((dia, idx))

    if request.method == "POST":
        new_data = {dia: [] for dia in dias}
        for i in range(len(horarios)):
            for dia in dias:
                campo = f"{dia}_{i}"
                valor = request.POST.get(campo, "")
                new_data[dia].append(valor)

        grade.dados = new_data
        grade.save()
        messages.success(request, "Grade horária atualizada com sucesso!")
        return redirect("grade_horaria", turma_id=turma.id)

    rows = []
    for i, horario in enumerate(horarios):
        row = {"index": i, "horario": horario, "cols": []}

        for dia in dias:
            lista = grade.dados.get(dia, [])
            valor = lista[i] if isinstance(lista, list) and i < len(lista) else ""

            disciplinas_disponiveis = []
            for d in disciplinas_da_turma:
                prof_id = d.professor_id
                if prof_id in ocupados and (dia, i) in ocupados[prof_id]:
                    continue
                disciplinas_disponiveis.append(d)

            row["cols"].append(
                {
                    "dia": dia,
                    "valor": valor,
                    "disciplinas": disciplinas_disponiveis,
                }
            )

        rows.append(row)

    return render(
        request,
        "core/grade_horaria.html",
        {
            "turma": turma,
            "nomes_dias": nomes_dias,
            "rows": rows,
            "disciplinas": disciplinas_da_turma,
        },
    )