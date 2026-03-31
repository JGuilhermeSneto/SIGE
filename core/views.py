"""Views do módulo core do sistema SIGE."""

import calendar
from datetime import datetime

from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import AlunoForm, EditarPerfilForm, GestorForm, LoginForm, ProfessorForm
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

DIAS_SEMANA = ["segunda", "terca", "quarta", "quinta", "sexta"]
NOMES_DIAS = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]


# ======================== HELPERS ========================
def is_superuser(user):
    """Verifica se o usuário é superusuário."""
    return user.is_superuser


def is_super_ou_gestor(user):
    """Verifica se o usuário é superusuário ou gestor."""
    return user.is_superuser or hasattr(user, "gestor")


def get_foto_perfil(user):
    """Retorna a URL da foto de perfil do usuário, se existir."""
    for tipo in ["professor", "aluno", "gestor", "superperfil"]:
        try:
            perfil = getattr(user, tipo, None)
            if perfil and getattr(perfil, "foto", None):
                return perfil.foto.url
        except (AttributeError, ValueError):
            pass
    return None


def get_nome_exibicao(user):
    """Retorna o nome de exibição do usuário conforme seu perfil."""
    for tipo in ["gestor", "professor", "aluno"]:
        perfil = getattr(user, tipo, None)
        if perfil and getattr(perfil, "nome_completo", None):
            return perfil.nome_completo
    nome = f"{user.first_name} {user.last_name}".strip()
    return nome if nome else user.email


def get_user_profile(user):
    """Retorna o perfil associado ao usuário (professor, aluno, gestor etc)."""
    for tipo in ["professor", "aluno", "gestor", "superperfil"]:
        perfil = getattr(user, tipo, None)
        if perfil:
            return perfil
    return None


def redirect_user(user):
    """Retorna o nome da URL de redirecionamento conforme o tipo de usuário."""
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
    """Gera as células do calendário do mês atual."""
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


def _get_turno_key(turno):
    """Normaliza o turno para chave do dicionário HORARIOS."""
    return turno.lower().replace("ã", "a").replace("á", "a")


def _get_anos_filtro(anos_disponiveis, ano_param, ano_atual):
    """Resolve e valida o ano de filtro, retornando (ano_filtro, anos_atualizados)."""
    try:
        ano_filtro = int(ano_param) if ano_param else ano_atual
    except ValueError:
        ano_filtro = ano_atual

    if ano_filtro not in anos_disponiveis:
        anos_disponiveis = sorted(anos_disponiveis + [ano_filtro], reverse=True)

    return ano_filtro, anos_disponiveis


def _contar_notas_lancadas(nota):
    """Conta quantas notas bimestrais foram lançadas em um objeto Nota."""
    return sum(
        1
        for campo in (nota.nota1, nota.nota2, nota.nota3, nota.nota4)
        if campo is not None
    )


def _calcular_detalhes_disciplina(disciplina, alunos_count):
    """Retorna dict com detalhes de notas lançadas para uma disciplina."""
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
    """Converte os dados brutos de GradeHorario em dict indexado por horário."""
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
    """Busca e formata a grade horária de uma turma. Retorna None se não existir."""
    try:
        grade_obj = GradeHorario.objects.get(turma=turma)
    except GradeHorario.DoesNotExist:
        return None
    turno_key = _get_turno_key(turma.turno)
    horarios = HORARIOS.get(turno_key, [])
    return _formatar_grade(grade_obj, horarios)


def _calcular_situacao_aluno(disciplinas_com_notas, total_lancadas, total_possiveis):
    """Determina situação geral do aluno (Aprovado/Reprovado/Recuperação/--)."""
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
    """Retorna dict {prof_id: set((dia, idx))} com slots já ocupados em outras turmas."""
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


def _build_grade_rows(grade, horarios, disciplinas_da_turma, ocupados):
    """Monta a lista de linhas da grade para renderização."""
    rows = []
    for i, horario in enumerate(horarios):
        cols = []
        for dia in DIAS_SEMANA:
            lista = grade.dados.get(dia, [])
            valor = lista[i] if isinstance(lista, list) and i < len(lista) else ""
            disponiveis = [
                d
                for d in disciplinas_da_turma
                if (d.professor_id not in ocupados)
                or (dia, i) not in ocupados[d.professor_id]
            ]
            cols.append({"dia": dia, "valor": valor, "disciplinas": disponiveis})
        rows.append({"index": i, "horario": horario, "cols": cols})
    return rows


def _is_gestor_ou_super(user):
    """Atalho para verificar se o usuário é superusuário ou gestor."""
    return user.is_superuser or hasattr(user, "gestor")


# ======================== LOGIN / LOGOUT ========================
def login_view(request):
    """Processa o login do usuário."""
    if request.user.is_authenticated:
        return redirect(redirect_user(request.user))

    form = LoginForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect(redirect_user(user))

    return render(request, "auth/login.html", {"form": form})


def logout_view(request):
    """Realiza o logout do usuário."""
    logout(request)
    return redirect("login")


# ======================== PAINEL SUPER ========================
@login_required
@user_passes_test(is_super_ou_gestor)
def painel_super(request):
    """Exibe o painel principal do superusuário/gestor."""
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
                Professor.objects.filter(disciplina__turma__in=turmas)
                .distinct()
                .count()
            ),
            "total_alunos": (Aluno.objects.filter(turma__in=turmas).distinct().count()),
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


# ========================== USUÁRIOS ==========================
@login_required
def usuarios(request):
    """Lista os usuários do sistema."""
    pode_ver_gestores = request.user.is_superuser or (
        hasattr(request.user, "gestor")
        and request.user.gestor.cargo in ("diretor", "vice_diretor")
    )
    return render(
        request, "core/usuarios.html", {"pode_ver_gestores": pode_ver_gestores}
    )


# ======================== PERFIL ========================
@login_required
def editar_perfil(request):
    """Permite ao usuário editar seu perfil."""
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
    """Remove a foto de perfil do usuário."""
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
    """Lista todos os professores cadastrados."""
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
    """Cadastra um novo professor."""
    if request.method == "POST":
        form = ProfessorForm(request.POST, request.FILES, request=request)
        if form.is_valid():
            professor = form.save()
            messages.success(
                request,
                f"Professor(a) {professor.nome_completo} cadastrado(a) com sucesso!",
            )
            return redirect("listar_professores")
        for _, erros in form.errors.items():
            for erro in erros:
                messages.error(request, erro)
    else:
        form = ProfessorForm(request=request)

    return render(request, "professor/cadastrar_professor.html", {"form": form})


@login_required
@user_passes_test(lambda u: u.is_superuser or hasattr(u, "gestor"))
def editar_professor(request, professor_id):
    """Edita os dados de um professor."""
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
        for _, erros in form.errors.items():
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
    """Exclui um professor do sistema."""
    professor = get_object_or_404(Professor, id=professor_id)
    professor.user.delete()
    messages.success(request, "Professor removido.")
    return redirect("listar_professores")


# ========================== GESTOR ==========================
@login_required
@user_passes_test(lambda u: u.is_superuser)
def cadastrar_gestor(request):
    """Cadastra um novo gestor."""
    if request.method == "POST":
        form = GestorForm(request.POST, request.FILES, request=request)
        if form.is_valid():
            gestor = form.save()
            messages.success(
                request,
                f"{gestor.get_cargo_display()} {gestor.nome_completo} cadastrado com sucesso!",
            )
            return redirect("listar_gestores")
        for _, erros in form.errors.items():
            for erro in erros:
                messages.error(request, erro)
    else:
        form = GestorForm(request=request)

    return render(request, "gestor/cadastrar_gestor.html", {"form": form})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def listar_gestores(request):
    """Lista todos os gestores cadastrados."""
    gestores = Gestor.objects.select_related("user").all()
    return render(request, "gestor/listar_gestores.html", {"gestores": gestores})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def excluir_gestor(request, gestor_id):
    """Exclui um gestor do sistema."""
    gestor = get_object_or_404(Gestor, id=gestor_id)
    gestor.user.delete()
    messages.success(request, "Gestor excluído com sucesso.")
    return redirect("listar_gestores")


@login_required
@user_passes_test(lambda u: u.is_superuser)
def editar_gestor(request, gestor_id):
    """Edita os dados de um gestor."""
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
    """Lista todos os alunos cadastrados."""
    query = request.GET.get("q", "")
    alunos = (
        Aluno.objects.filter(nome_completo__icontains=query)
        if query
        else Aluno.objects.all()
    )
    return render(
        request, "aluno/listar_alunos.html", {"alunos": alunos, "query": query}
    )


@login_required
@user_passes_test(lambda u: u.is_superuser or hasattr(u, "gestor"))
def cadastrar_aluno(request):
    """Cadastra um novo aluno."""
    if request.method == "POST":
        form = AlunoForm(request.POST, request.FILES, request=request)
        if form.is_valid():
            aluno = form.save()
            messages.success(
                request, f"Aluno(a) {aluno.nome_completo} cadastrado(a) com sucesso!"
            )
            return redirect("listar_alunos")
        for _, erros in form.errors.items():
            for erro in erros:
                messages.error(request, erro)
    else:
        form = AlunoForm(request=request)

    return render(request, "aluno/cadastrar_aluno.html", {"form": form})


@login_required
@user_passes_test(lambda u: u.is_superuser or hasattr(u, "gestor"))
def editar_aluno(request, aluno_id):
    """Edita os dados de um aluno."""
    aluno = get_object_or_404(Aluno, id=aluno_id)

    if request.method == "POST":
        form = AlunoForm(request.POST, request.FILES, instance=aluno, request=request)
        if form.is_valid():
            aluno = form.save()
            messages.success(
                request, f"Aluno(a) {aluno.nome_completo} atualizado(a) com sucesso!"
            )
            return redirect("listar_alunos")
        for _, erros in form.errors.items():
            for erro in erros:
                messages.error(request, erro)
    else:
        form = AlunoForm(instance=aluno, request=request)

    return render(request, "aluno/cadastrar_aluno.html", {"form": form, "aluno": aluno})


@login_required
@user_passes_test(lambda u: u.is_superuser or hasattr(u, "gestor"))
def excluir_aluno(request, aluno_id):
    """Exclui um aluno do sistema."""
    aluno = get_object_or_404(Aluno, id=aluno_id)
    aluno.user.delete()
    messages.success(request, "Aluno removido.")
    return redirect("listar_alunos")


# ========================== TURMAS ==========================
@login_required
@user_passes_test(lambda u: u.is_superuser or hasattr(u, "gestor"))
def listar_turmas(request):
    """Lista todas as turmas cadastradas."""
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
    """Cadastra uma nova turma."""
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
    """Edita os dados de uma turma."""
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
    """Exclui uma turma do sistema."""
    turma = get_object_or_404(Turma, id=turma_id)
    turma.delete()
    messages.success(request, "Turma excluída com sucesso!")
    return redirect("listar_turmas")


# ========================== DISCIPLINAS ==========================
@login_required
def visualizar_disciplinas(request, disciplina_id):
    """Exibe os detalhes de uma disciplina com notas dos alunos."""
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
        messages.error(
            request, "Você não tem permissão para visualizar esta disciplina."
        )
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
            "is_gestor_ou_super": _is_gestor_ou_super(request.user),  # ✅ CORRIGIDO
        },
    )


@login_required
@user_passes_test(lambda u: u.is_superuser or hasattr(u, "gestor"))
def editar_disciplina(request, disciplina_id):
    """Edita os dados de uma disciplina."""
    disciplina = get_object_or_404(Disciplina, id=disciplina_id)
    professores = Professor.objects.filter(user__is_superuser=False)

    if request.method == "POST":
        disciplina.nome = request.POST["nome"]
        disciplina.professor = get_object_or_404(
            Professor, id=request.POST["professor"]
        )
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
    """Exclui uma disciplina do sistema."""
    disciplina = get_object_or_404(Disciplina, id=disciplina_id)
    turma_id = disciplina.turma.id
    disciplina.delete()
    messages.success(request, "Disciplina excluída com sucesso!")
    return redirect("disciplinas_turma", turma_id=turma_id)


@login_required
@user_passes_test(lambda u: u.is_superuser or hasattr(u, "gestor"))
def cadastrar_disciplina_para_turma(request, turma_id):
    """Cadastra uma nova disciplina vinculada a uma turma."""
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
    """Lista as disciplinas de uma turma específica."""
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
    """Exibe as disciplinas de uma turma para professor ou gestor."""
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
            "is_gestor_ou_super": _is_gestor_ou_super(user),  # ✅ CORRIGIDO
        },
    )


# ======================== PAINEL PROFESSOR ========================
def _get_ano_filtro_professor(request, anos_disponiveis, ano_atual):
    """Resolve o ano de filtro para o painel do professor, usando sessão como fallback."""
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
    """Calcula totais e detalhes de notas para as disciplinas de um professor."""
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

    return (
        total_notas_possiveis,
        total_notas_lancadas,
        len(alunos_ids),
        disciplinas_detalhadas,
    )


@login_required
def painel_professor(request):
    """Exibe o painel principal do professor."""
    if not hasattr(request.user, "professor"):
        return redirect("login")

    professor = request.user.professor
    ano_atual = datetime.now().year
    disciplinas = Disciplina.objects.filter(professor=professor).select_related("turma")

    anos_disponiveis = list(
        Turma.objects.filter(disciplina__professor=professor)
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
    """Lista as disciplinas do professor logado."""
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
    """Exibe a grade horária de uma turma para o professor."""
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


# ======================== LANÇAR NOTA ========================
@login_required
@user_passes_test(
    lambda u: u.is_superuser or hasattr(u, "gestor") or hasattr(u, "professor")
)
def lancar_nota(request, disciplina_id):
    """Lança notas dos alunos em uma disciplina."""
    disciplina = get_object_or_404(Disciplina, id=disciplina_id)
    alunos = Aluno.objects.filter(turma_id=disciplina.turma_id).order_by(
        "nome_completo"
    )

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
            "is_gestor_ou_super": _is_gestor_ou_super(request.user),  # ✅ CORRIGIDO
        },
    )


# ======================== PAINEL ALUNO ========================
def _coletar_notas_aluno(aluno, disciplinas):
    """Coleta disciplinas com notas e totais para o painel do aluno."""
    disciplinas_com_notas = []
    soma_medias = 0
    total_com_media = 0
    total_lancadas = 0

    for disciplina in disciplinas:
        nota = Nota.objects.filter(aluno=aluno, disciplina=disciplina).first()
        if nota:
            total_lancadas += _contar_notas_lancadas(nota)
        disciplinas_com_notas.append({"disciplina": disciplina, "nota": nota})
        if nota and nota.media is not None:
            soma_medias += nota.media
            total_com_media += 1

    media_geral = soma_medias / total_com_media if total_com_media > 0 else None
    return disciplinas_com_notas, media_geral, total_lancadas


@login_required
def painel_aluno(request):
    """Exibe o painel do aluno com notas e grade horária."""
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


# ======================== GRADE HORÁRIA ========================
@login_required
def grade_horaria(request, turma_id):
    """Exibe e permite editar a grade horária de uma turma."""
    turma = get_object_or_404(Turma, id=turma_id)
    grade, _ = GradeHorario.objects.get_or_create(turma=turma)

    turno_key = _get_turno_key(turma.turno)
    horarios = HORARIOS.get(turno_key, []) or [""]

    if not grade.dados:
        grade.dados = {dia: [""] * len(horarios) for dia in DIAS_SEMANA}
        grade.save()

    disciplinas_da_turma = Disciplina.objects.filter(turma=turma)
    ocupados = _get_ocupados_por_professor(turma)

    if request.method == "POST":
        grade.dados = {
            dia: [request.POST.get(f"{dia}_{i}", "") for i in range(len(horarios))]
            for dia in DIAS_SEMANA
        }
        grade.save()
        messages.success(request, "Grade horária atualizada com sucesso!")
        return redirect("grade_horaria", turma_id=turma.id)

    rows = _build_grade_rows(grade, horarios, disciplinas_da_turma, ocupados)

    return render(
        request,
        "core/grade_horaria.html",
        {
            "turma": turma,
            "nomes_dias": NOMES_DIAS,
            "rows": rows,
            "disciplinas": disciplinas_da_turma,
            "is_gestor_ou_super": _is_gestor_ou_super(request.user),  # ✅ CORRIGIDO
        },
    )
