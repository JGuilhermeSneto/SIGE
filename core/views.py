import calendar
from datetime import datetime, timezone

from django.contrib import messages
from django.contrib.auth import (authenticate, login, logout,
                                 update_session_auth_hash)
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (AlunoForm, DisciplinaForm, EditarPerfilForm, GestorForm,
                    LoginForm, NotaForm, ProfessorForm, TurmaForm)
from .models import Aluno, Disciplina, Gestor, Nota, Professor, Turma


# ======================== LOGIN / LOGOUT ========================
def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect("painel_super")
        elif hasattr(request.user, "professor"):
            return redirect("painel_professor")
        elif hasattr(request.user, "aluno"):
            return redirect("painel_aluno")
        elif hasattr(request.user, "gestor"):
            return redirect("painel_super")

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_superuser:
                return redirect("painel_super")
            elif hasattr(user, "professor"):
                return redirect("painel_professor")
            elif hasattr(user, "aluno"):
                return redirect("painel_aluno")
            elif hasattr(user, "gestor"):
                return redirect("painel_super")
    else:
        form = LoginForm()

    return render(
        request, "auth/login.html", {"form": form}
    )  # ✅ Primeira função corrigida!!


def logout_view(request):
    logout(request)
    return redirect("login")


# ======================== CALENDÁRIO ========================
def gerar_calendario():
    hoje = datetime.today()  # pega a data atual

    # gera uma matriz com os dias do mês (semanas)
    cal = calendar.monthcalendar(hoje.year, hoje.month)

    for semana in cal:
        for dia in semana:
            celulas.append( # type: ignore
                {  # type: ignore
                    "numero": dia,
                    "vazio": dia == 0,
                    "hoje": dia == hoje.day,
                }
            )

    return celulas  # type: ignore


# ========================== SUPERUSUÁRIO ========================
def is_superuser(user):
    return user.is_superuser


def is_super_ou_gestor(user):
    return user.is_superuser or hasattr(user, "gestor")


def get_foto_perfil(user):
    # lista de possíveis perfis do usuário
    for tipo in ["professor", "aluno", "gestor", "superperfil"]:

        perfil = getattr(user, tipo, None)  # tenta acessar o perfil

        # verifica se existe perfil e se possui foto
        if perfil and getattr(perfil, "foto", None):
            return perfil.foto.url  # retorna URL da foto

    return None  # retorna vazio caso não tenha foto


def get_nome_exibicao(user):
    # percorre tipos de perfil
    for tipo in ["gestor", "professor", "aluno"]:

        perfil = getattr(user, tipo, None)  # pega perfil

        # verifica se existe e possui nome completo
        if perfil and getattr(perfil, "nome_completo", None):
            return perfil.nome_completo  # retorna nome

    # monta nome com first_name e last_name
    nome = f"{user.first_name} {user.last_name}".strip()

    # se existir nome retorna, senão retorna email
    return nome if nome else user.email


# ======================== AUTENTICAÇÃO ========================


def login_view(request):
    # verifica se usuário já está autenticado
    if request.user.is_authenticated:
        return redirect(redirect_user(request.user))  # type: ignore # redireciona

    form = LoginForm(request.POST or None)  # cria formulário

    # se for envio POST e formulário válido
    if request.method == "POST" and form.is_valid():

        user = form.get_user()  # obtém usuário autenticado
        login(request, user)  # realiza login

        return redirect(redirect_user(user))  # type: ignore # redireciona

    # renderiza página de login
    return render(request, "auth/login.html", {"form": form})


def logout_view(request):
    logout(request)  # encerra sessão do usuário
    return redirect("login")  # redireciona para login


# ======================== PAINEL SUPER ========================


@login_required  # exige usuário logado
@user_passes_test(is_super_ou_gestor)  # exige permissão
def painel_super(request):

    ano_atual = datetime.now().year  # pega ano atual

    # FILTRO DE ANO
    anos_disponiveis_qs = (
        Turma.objects.values_list("ano", flat=True).distinct().order_by("-ano")
    )
    anos_disponiveis = list(anos_disponiveis_qs)

    if not anos_disponiveis:
        anos_disponiveis = [ano_atual]  # usa ano atual

    ano_filtro = request.GET.get("ano")
    try:
        # tenta converter para inteiro
        ano_filtro = int(ano_filtro) if ano_filtro else ano_atual
    except ValueError:
        ano_filtro = ano_atual  # fallback

    # garante que o ano existe na lista
    if ano_filtro not in anos_disponiveis:
        anos_disponiveis.append(ano_filtro)
        anos_disponiveis.sort(reverse=True)

    turmas = Turma.objects.filter(ano=ano_filtro)  # filtra turmas

    total_turmas = turmas_ano_filtrado.count()  # type: ignore
    total_alunos = Aluno.objects.filter(turma__in=turmas_ano_filtrado).distinct().count()  # type: ignore
    total_professores = Professor.objects.filter(disciplina__turma__in=turmas_ano_filtrado).distinct().count()  # type: ignore
    total_disciplinas = Disciplina.objects.filter(turma__in=turmas_ano_filtrado).distinct().count()  # type: ignore

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
            "foto_perfil_url": foto_perfil_url,  # type: ignore
            "agora": datetime.now(),
            "calendario": gerar_calendario(),
            "anos_disponiveis": anos_disponiveis,
            "ano_filtro": ano_filtro,
        },
    )


# ========================== USUÁRIOS ==========================


@login_required
def usuarios(request):

    user = request.user  # pega usuário atual

    if request.user.is_superuser:
        pode_ver_gestores = True
    elif hasattr(request.user, "gestor"):
        if request.user.gestor.cargo in ("diretor", "vice_diretor"):
            pode_ver_gestores = True

    return render(
        request, "core/usuarios.html", {"pode_ver_gestores": pode_ver_gestores}  # ✅
    )


from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


@login_required
def editar_perfil(request):

    user = request.user  # usuário atual
    perfil = get_user_profile(user)  # type: ignore # pega perfil

    form = EditarPerfilForm(request.POST or None, instance=user)  # cria form

    if request.method == "POST" and form.is_valid():

        user = form.save(commit=False)  # salva sem commit

        nova_senha = form.cleaned_data.get("nova_senha")  # pega senha

        if nova_senha:
            user.set_password(nova_senha)  # define nova senha
            update_session_auth_hash(request, user)  # mantém sessão

        user.save()  # salva usuário

        foto = request.FILES.get("foto")  # pega arquivo enviado

        if perfil and foto:
            perfil.foto = foto  # atualiza foto
            perfil.save()  # salva perfil

        messages.success(request, "Perfil atualizado com sucesso!")

        return redirect(redirect_user(user))  # type: ignore

    if request.method == "POST":
        messages.error(request, "Corrija os erros abaixo.")

    foto_atual = None  # inicia variável

    # verifica se existe foto
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


def get_foto_perfil(user):
    # Professor
    if hasattr(user, "professor") and user.professor and user.professor.foto:
        return user.professor.foto.url

    # Aluno
    if hasattr(user, "aluno") and user.aluno and user.aluno.foto:
        return user.aluno.foto.url

    # Gestor
    if hasattr(user, "gestor") and user.gestor and user.gestor.foto:
        return user.gestor.foto.url

    # Superusuário
    if hasattr(user, "superperfil") and user.superperfil and user.superperfil.foto:
        return user.superperfil.foto.url

    return None  # ✅✅ refatorado


@login_required
def remover_foto_perfil(request):

    perfil = get_user_profile(request.user)  # type: ignore # pega perfil

    if not perfil:
        messages.error(request, "Nenhum perfil associado ao usuário.")
        return redirect("editar_perfil")

    # verifica se existe foto
    if getattr(perfil, "foto", None):
        perfil.foto.delete(save=False)  # remove arquivo
        perfil.foto = None  # limpa campo
        perfil.save()  # salva

    messages.success(request, "Foto removida com sucesso!")
    return redirect("editar_perfil")


def get_nome_exibicao(user):
    if hasattr(user, "gestor") and user.gestor:
        return user.gestor.nome_completo

    if hasattr(user, "professor") and user.professor:
        return user.professor.nome_completo

    if hasattr(user, "aluno") and user.aluno:
        return user.aluno.nome_completo

    nome = f"{user.first_name} {user.last_name}".strip()
    if nome:
        return nome

    return user.email


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
            professor = form.save()  # salva professor

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


# ========================== EDITAR PROFESSOR ==========================
@login_required
@user_passes_test(lambda u: u.is_superuser or hasattr(u, "gestor"))
def editar_professor(request, professor_id):
    # busca o professor pelo id ou retorna erro 404 se não existir
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


# ========================== EXCLUIR PROFESSOR ==========================
@login_required
@user_passes_test(lambda u: u.is_superuser or hasattr(u, "gestor"))
def excluir_professor(request, professor_id):

    # busca professor ou retorna erro 404
    professor = get_object_or_404(Professor, id=professor_id)
    professor.user.delete()
    professor.delete()
    messages.success(request, "Professor removido.")
    return redirect("listar_professores")


##✅✅ refatorado

# ========================== GESTOR ==========================


@login_required  # exige login
@user_passes_test(lambda u: u.is_superuser)  # apenas superusuário pode acessar
def cadastrar_gestor(request):
    if request.method == "POST":
        form = GestorForm(request.POST, request.FILES, request=request)

        if form.is_valid():
            gestor = form.save()  # 🔥 Faz tudo automaticamente

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


##✅✅ refatorado

# ==== GESTOR (Painel da Gestão Escolar) ====


@login_required
@user_passes_test(lambda u: u.is_superuser)
def listar_gestores(request):
    gestores = Gestor.objects.select_related("user").all()
    return render(request, "gestor/listar_gestores.html", {"gestores": gestores})


# ========================== EXCLUIR GESTOR ==========================
@login_required
@user_passes_test(lambda u: u.is_superuser)
def excluir_gestor(request, gestor_id):
    gestor = get_object_or_404(Gestor, id=gestor_id)
    gestor.user.delete()
    gestor.delete()
    messages.success(request, "Gestor excluído com sucesso.")
    return redirect("listar_gestores")


# ========================== EDITAR GESTOR ==========================
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
    )  ##✅✅ refatorado


# ========================== ALUNO =========================
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


# ========================== CADASTRAR ALUNO ==========================
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


# ========================== EDITAR ALUNO ==========================
@login_required
@user_passes_test(lambda u: u.is_superuser or hasattr(u, "gestor"))
def editar_aluno(request, aluno_id):

    # busca aluno pelo id ou retorna erro 404
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
    )  ##✅✅ refatorado


@login_required
@user_passes_test(lambda u: u.is_superuser or hasattr(u, "gestor"))
def excluir_aluno(request, aluno_id):

    # busca aluno pelo id ou retorna erro 404
    aluno = get_object_or_404(Aluno, id=aluno_id)
    aluno.user.delete()
    aluno.delete()
    messages.success(request, "Aluno removido.")
    return redirect("listar_alunos")


# ========================== DISCIPLINAS, TURMAS E NOTAS ==========================
# (mantém as lógicas originais do seu código, já estavam certas)


# Disciplinas


@login_required
def visualizar_disciplinas(request, disciplina_id):

    # busca disciplina pelo id ou retorna erro 404
    disciplina = get_object_or_404(Disciplina, id=disciplina_id)

    # Permite acesso se for:
    # - superusuário
    # - gestor
    # - professor da disciplina
    if not (
        request.user.is_superuser
        or hasattr(request.user, "gestor")
        or (
            hasattr(request.user, "professor")
            and disciplina.professor == request.user.professor
        )
    ):
        messages.error(
            request, "Você não tem permissão para visualizar esta disciplina."
        )
        return redirect("login")

    turma = disciplina.turma
    alunos = Aluno.objects.filter(turma=turma).order_by("nome_completo")
    notas = Nota.objects.filter(disciplina=disciplina)
    notas_dict = {
        nota.aluno.id: nota for nota in Nota.objects.filter(disciplina=disciplina)
    }

    context = {
        "disciplina": disciplina,
        "turma": turma,
        "alunos": alunos,
        "notas": notas,
        "notas_dict": notas_dict,
    }

    return render(request, "core/visualizar_disciplinas.html", context)


@login_required
@user_passes_test(lambda u: u.is_superuser or hasattr(u, "gestor"))
def editar_disciplina(request, disciplina_id):

    disciplina = get_object_or_404(Disciplina, id=disciplina_id)

    if request.method == "POST":
        disciplina.nome = request.POST["nome"]
        disciplina.professor = get_object_or_404(
            Professor, id=request.POST["professor"]
        )
        disciplina.save()

        return redirect("listar_disciplinas_turma", turma_id=disciplina.turma.id)

    # ========================== RENDER ==========================

    return render(
        request,
        "core/cadastrar_disciplina_turma.html",
        {
            "disciplina": disciplina,
            "turma": disciplina.turma,
            "professores": professores,  # type: ignore
        },
    )


##✅✅ refatorado


@login_required
@user_passes_test(lambda u: u.is_superuser or hasattr(u, "gestor"))
def excluir_disciplina(request, disciplina_id):

    # busca disciplina ou retorna erro 404
    disciplina = get_object_or_404(Disciplina, id=disciplina_id)

    turma_id = disciplina.turma.id  # salva id da turma antes de deletar

    disciplina.delete()  # remove disciplina do banco

    # mensagem de sucesso
    messages.success(request, "Disciplina excluída com sucesso!")

    # redireciona para lista de disciplinas da turma
    return redirect("listar_disciplinas_turma", turma_id=turma_id)


# ========================== LISTAR TURMAS ==========================
@login_required
@user_passes_test(lambda u: u.is_superuser or hasattr(u, "gestor"))
def listar_turmas(request):

    # pega ano atual considerando timezone do Django
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
        # tenta converter para inteiro
        ano_filtro = int(ano_filtro) if ano_filtro else ano_atual
    except ValueError:
        ano_filtro = ano_atual  # fallback se valor inválido

    # garante que o ano selecionado está na lista
    if ano_filtro not in anos_disponiveis:
        anos_disponiveis.append(ano_filtro)
        anos_disponiveis.sort(reverse=True)

    # ========================== CONSULTA ==========================

    # filtra turmas pelo ano selecionado
    turmas = Turma.objects.filter(ano=ano_filtro)

    # aplica filtro de busca por nome
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


from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .models import Turma


@login_required
@user_passes_test(lambda u: u.is_superuser or hasattr(u, "gestor"))
def cadastrar_turma(request):

    erro = None

    ano_atual = datetime.now().year

    # cria lista de anos permitidos (2010 até próximo ano)
    anos = list(range(2010, ano_atual + 2))

    # ========================== PROCESSAMENTO POST ==========================

    if request.method == "POST":
        nome = request.POST.get("nome")
        turno = request.POST.get("turno")
        ano = request.POST.get("ano")

        # =========== VALIDAÇÕES ===========
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

    return render(request, "core/cadastrar_turma.html", {"erro": erro, "anos": anos})


@login_required
@user_passes_test(lambda u: u.is_superuser or hasattr(u, "gestor"))
def editar_turma(request, turma_id):

    # busca turma ou retorna erro 404
    turma = get_object_or_404(Turma, id=turma_id)

    erro = None  # variável de erro

    # pega ano atual
    ano_atual = datetime.now().year

    # lista de anos (mantém padrão do cadastro)
    anos = list(range(2010, ano_atual + 2))

    # ========================== PROCESSAMENTO POST ==========================

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

    return render(request, "turma/cadastrar_turma.html", {"turma": turma, "erro": erro})


@login_required
@user_passes_test(
    lambda u: u.is_superuser
    or (hasattr(u, "gestor") and u.gestor.cargo != "secretario")
)
def excluir_turma(request, turma_id):

    # busca turma pelo id ou retorna erro 404
    turma = get_object_or_404(Turma, id=turma_id)

    turma.delete()  # remove turma do banco

    # mensagem de sucesso
    messages.success(request, "Turma excluída com sucesso!")

    return redirect("listar_turmas")


##✅✅ refatorado

# ========================== PAINEL PROFESSOR ==========================


@login_required  # exige login
def painel_professor(request):
    """Tela principal do professor com estatísticas e visão geral"""
    if not hasattr(request.user, "professor"):
        return redirect("login")

    professor = request.user.professor
    foto_perfil_url = get_foto_perfil(request.user)

    # Buscar todas as disciplinas do professor
    disciplinas = Disciplina.objects.filter(professor=professor).select_related("turma")

    # Anos disponíveis baseados nas turmas onde o professor leciona
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

    # Filtro de ano
    ano_filtro = request.GET.get("ano")

    if ano_filtro:
        try:
            ano_filtro = int(ano_filtro)
            request.session["ano_filtro_professor"] = ano_filtro
        except ValueError:
            ano_filtro = request.session.get("ano_filtro_professor", ano_atual)
    else:
        # Se não veio no GET, tenta pegar da sessão
        ano_filtro = request.session.get("ano_filtro_professor", ano_atual)

    if ano_filtro not in anos_disponiveis:
        anos_disponiveis.append(ano_filtro)
        anos_disponiveis.sort(reverse=True)

    # Filtrar disciplinas por ano
    disciplinas_filtradas = disciplinas.filter(turma__ano=ano_filtro)

    # ESTATÍSTICAS
    total_disciplinas = disciplinas_filtradas.count()
    total_turmas = disciplinas_filtradas.values("turma").distinct().count()

    # Total de alunos (sem duplicatas)
    alunos_ids = set()
    for disciplina in disciplinas_filtradas:
        alunos_turma = Aluno.objects.filter(turma=disciplina.turma).values_list(
            "id", flat=True
        )
        alunos_ids.update(alunos_turma)
    total_alunos = len(alunos_ids)

    # Notas lançadas vs pendentes
    total_notas_possiveis = 0
    total_notas_lancadas = 0

    for disciplina in disciplinas_filtradas:
        alunos_disciplina = Aluno.objects.filter(turma=disciplina.turma)
        total_notas_possiveis += alunos_disciplina.count() * 4

        notas = Nota.objects.filter(disciplina=disciplina)

        # percorre notas para contar campos preenchidos
        for nota in notas:
            if nota.nota1 is not None:
                total_notas_lancadas += 1
            if nota.nota2 is not None:
                total_notas_lancadas += 1
            if nota.nota3 is not None:
                total_notas_lancadas += 1
            if nota.nota4 is not None:
                total_notas_lancadas += 1

    # Lista de disciplinas com informações detalhadas
    disciplinas_detalhadas = []
    for disciplina in disciplinas_filtradas:

        # quantidade de alunos da turma
        alunos_count = Aluno.objects.filter(turma=disciplina.turma).count()

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
        "core/painel_professor.html",
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


##✅ refatorado


@login_required  # exige que o usuário esteja autenticado
def disciplinas_professor(request):
    """Lista todas as turmas onde o professor leciona com filtro de ano"""
    if not hasattr(request.user, "professor"):
        return redirect("login")

    professor = request.user.professor
    foto_perfil_url = get_foto_perfil(request.user)

    # Busca turmas onde o professor tem disciplinas
    turmas_ids = (
        Disciplina.objects.filter(professor=professor)
        .values_list("turma_id", flat=True)
        .distinct()
    )

    # Anos disponíveis
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

    # 🔥 LÓGICA DO FILTRO COM SESSÃO
    ano_filtro = request.GET.get("ano")

    if ano_filtro:
        try:
            ano_filtro = int(ano_filtro)
            request.session["ano_filtro_professor"] = ano_filtro
        except ValueError:
            ano_filtro = request.session.get("ano_filtro_professor", ano_atual)
    else:
        # Se não veio no GET, tenta pegar da sessão
        ano_filtro = request.session.get("ano_filtro_professor", ano_atual)

    if ano_filtro not in anos_disponiveis:
        anos_disponiveis.append(ano_filtro)
        anos_disponiveis.sort(reverse=True)

    # Filtrar turmas por ano
    turmas = Turma.objects.filter(id__in=turmas_ids, ano=ano_filtro).order_by("nome")

    # Filtro de busca
    query = request.GET.get("q", "")
    if query:
        turmas = turmas.filter(nome__icontains=query)

    # Informações detalhadas de cada turma
    turmas_detalhadas = []
    for turma in turmas:
        disciplinas_turma = Disciplina.objects.filter(turma=turma, professor=professor)

        alunos_count = Aluno.objects.filter(turma=turma).count()

        turmas_detalhadas.append(
            {
                "turma": turma,
                "disciplinas_count": disciplinas_turma.count(),
                "alunos_count": alunos_count,
                "turno_display": turma.get_turno_display(),
            }
        )

    return render(
        request,
        "core/disciplinas_professor.html",
        {
            "turmas_detalhadas": turmas_detalhadas,
            "foto_perfil_url": foto_perfil_url,
            "query": query,
            "anos_disponiveis": anos_disponiveis,
            "ano_filtro": ano_filtro,
        },
    )


##✅✅ refatorado


# ==================== 3. DISCIPLINAS DE UMA TURMA ESPECÍFICA ====================
@login_required
def disciplinas_turma(request, turma_id):
    """
    Mostra as disciplinas de uma turma específica.
    Permite acesso para professor, gestor ou superusuário.
    """

    if not hasattr(request.user, "professor"):
        return redirect("login")

    professor = request.user.professor
    turma = get_object_or_404(Turma, id=turma_id)
    foto_perfil_url = get_foto_perfil(request.user)

    disciplinas = Disciplina.objects.filter(turma=turma, professor=professor).order_by(
        "nome"
    )

    if not disciplinas.exists():
        messages.error(request, "Você não leciona nenhuma disciplina nesta turma.")
        return redirect("disciplinas_professor")  # corrigido

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

        notas_possiveis_disc = alunos_count * 4  # type: ignore

        disciplinas_detalhadas.append(
            {
                "disciplina": disciplina,
                "alunos_count": alunos_count,  # type: ignore
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


###✅✅ refatorado


@login_required
def visualizar_grade_professor(request, turma_id):
    """Visualização da grade horária para o professor (somente leitura)"""
    if not hasattr(request.user, "professor"):
        return redirect("login")

    professor = request.user.professor
    turma = get_object_or_404(Turma, id=turma_id)

    # Verifica se o professor leciona nesta turma
    disciplinas_prof = Disciplina.objects.filter(turma=turma, professor=professor)

    if not disciplinas_prof.exists():
        messages.error(request, "Você não leciona nenhuma disciplina nesta turma.")
        return redirect("disciplinas_professor")

    # Pegar horários do turno
    turno_key = turma.turno.lower().replace("ã", "a").replace("á", "a")

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

    horarios = HORARIOS.get(turno_key, [])
    grade_formatada = None

    try:
        # tenta buscar grade da turma
        grade_obj = GradeHorario.objects.get(turma=turma)

        if horarios and grade_obj.dados:
            grade_formatada = {}

            for i, horario in enumerate(horarios):
                segunda = (
                    grade_obj.dados.get("segunda", [])[i]
                    if i < len(grade_obj.dados.get("segunda", []))
                    else ""
                )
                terca = (
                    grade_obj.dados.get("terca", [])[i]
                    if i < len(grade_obj.dados.get("terca", []))
                    else ""
                )
                quarta = (
                    grade_obj.dados.get("quarta", [])[i]
                    if i < len(grade_obj.dados.get("quarta", []))
                    else ""
                )
                quinta = (
                    grade_obj.dados.get("quinta", [])[i]
                    if i < len(grade_obj.dados.get("quinta", []))
                    else ""
                )
                sexta = (
                    grade_obj.dados.get("sexta", [])[i]
                    if i < len(grade_obj.dados.get("sexta", []))
                    else ""
                )

                grade_formatada[horario] = {
                    "segunda": segunda,
                    "terca": terca,
                    "quarta": quarta,
                    "quinta": quinta,
                    "sexta": sexta,
                }

    except GradeHorario.DoesNotExist:
        grade_formatada = None

    return render(
        request,
        "core/visualizar_grade_professor.html",
        {
            "turma": turma,
            "grade_horario": grade_formatada,
            "disciplinas_professor": disciplinas_prof,
        },
    )


##✅✅


@login_required
@user_passes_test(
    lambda u: u.is_superuser or hasattr(u, "gestor") or hasattr(u, "professor")
)
def lancar_nota(request, disciplina_id):
    disciplina = get_object_or_404(Disciplina, id=disciplina_id)

    # FORÇA queryset de MODEL (sem values)
    alunos = Aluno.objects.filter(turma_id=disciplina.turma_id).order_by(
        "nome_completo"
    )

    # DEBUG no terminal (pra provar que tem id)
    if alunos.exists():
        a0 = alunos.first()
        print(
            "DEBUG ALUNO:",
            type(a0),
            "id=",
            a0.id,
            "pk=",
            a0.pk,
            "nome=",
            a0.nome_completo,
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
        "core/lancar_nota.html",
        {
            "disciplina": disciplina,
            "alunos": alunos,
            "notas_dict": notas_dict,
        },
    )


import calendar
from datetime import datetime

# Horários por turno
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

    # LÓGICA DA SITUAÇÃO GERAL
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

    # SITUAÇÃO GERAL
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
            situacao_geral = "=="
            situacao_classe = ""
    else:
        situacao_geral = "=="
        situacao_classe = ""

    # ========================================
    # GRADE HORÁRIA = FORMATADA PARA O ALUNO
    # ========================================
    grade_formatada = None

    try:
        grade_obj = GradeHorario.objects.get(turma=aluno.turma)

        # Pegar horários do turno correto
        turno_key = aluno.turma.turno.lower().replace("ã", "a").replace("á", "a")
        horarios = HORARIOS.get(turno_key, [])

        if horarios and grade_obj.dados:
            grade_formatada = {}

            # Para cada horário, pegar as disciplinas de cada dia
            for i, horario in enumerate(horarios):
                segunda = (
                    grade_obj.dados.get("segunda", [])[i]
                    if i < len(grade_obj.dados.get("segunda", []))
                    else ""
                )
                terca = (
                    grade_obj.dados.get("terca", [])[i]
                    if i < len(grade_obj.dados.get("terca", []))
                    else ""
                )
                quarta = (
                    grade_obj.dados.get("quarta", [])[i]
                    if i < len(grade_obj.dados.get("quarta", []))
                    else ""
                )
                quinta = (
                    grade_obj.dados.get("quinta", [])[i]
                    if i < len(grade_obj.dados.get("quinta", []))
                    else ""
                )
                sexta = (
                    grade_obj.dados.get("sexta", [])[i]
                    if i < len(grade_obj.dados.get("sexta", []))
                    else ""
                )

                grade_formatada[horario] = {
                    "segunda": segunda,
                    "terca": terca,
                    "quarta": quarta,
                    "quinta": quinta,
                    "sexta": sexta,
                }

    except GradeHorario.DoesNotExist:
        grade_formatada = None

    calendario = gerar_calendario()
    agora = datetime.now()

    return render(
        request,
        "core/painel_aluno.html",
        {
            "aluno": aluno,
            "disciplinas_com_notas": disciplinas_com_notas,
            "media_geral": media_geral,
            "total_notas_lancadas": total_notas_lancadas,
            "total_notas_possiveis": total_notas_possiveis,
            "situacao_geral": situacao_geral,
            "situacao_classe": situacao_classe,
            "grade_horario": grade_formatada,  # ← agora formatada corretamente
            "calendario": calendario,
            "agora": agora,
        },
    )


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
                return redirect("listar_disciplinas_turma", turma_id=turma.id)

    professores = Professor.objects.filter(user__is_superuser=False)

    return render(
        request,
        "core/cadastrar_disciplina_turma.html",
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
        "core/listar_disciplinas_turma.html",
        {"turma": turma, "disciplinas": disciplinas, "query": query},
    )


# helper para pegar foto do usuário de forma segura
def get_foto_perfil(user):
    # Professor
    try:
        if hasattr(user, "professor") and user.professor.foto:
            return user.professor.foto.url
    except (AttributeError, ValueError):
        pass

    # Aluno
    try:
        if hasattr(user, "aluno") and user.aluno.foto:
            return user.aluno.foto.url
    except (AttributeError, ValueError):
        pass

    # Gestor
    try:
        if hasattr(user, "gestor") and user.gestor.foto:
            return user.gestor.foto.url
    except (AttributeError, ValueError):
        pass

    return None


from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import GradeHorario

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


@login_required
def grade_horaria(request, turma_id):

    # busca turma
    turma = get_object_or_404(Turma, id=turma_id)

    # busca ou cria grade
    grade, criado = GradeHorario.objects.get_or_create(turma=turma)

    # dias da semana (chave interna)
    dias = ["segunda", "terca", "quarta", "quinta", "sexta"]

    # nomes formatados para template
    nomes_dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]

    turno_key = turma.turno.lower().replace("ã", "a").replace("á", "a")

    horarios = HORARIOS.get(turno_key, [])

    # valida turno
    if not horarios:
        messages.error(request, "Turno inválido nesta turma.")
        horarios = [""]

    # inicializa estrutura da grade se estiver vazia
    if not grade.dados:
        grade.dados = {dia: [""] * len(horarios) for dia in dias}
        grade.save()

    # disciplinas da turma
    disciplinas_turma = Disciplina.objects.filter(turma=turma)

    # =============================================================
    # 1) MAPEAR OCUPAÇÃO DOS PROFESSORES
    # =============================================================
    ocupados = {}  # {professor_id: {(dia, index)} }

    outras_grades = GradeHorario.objects.exclude(turma=turma)

    for g in outras_grades:
        for dia in dias:

            lista = g.dados.get(dia, [])

            for idx, nome_disciplina in enumerate(lista):

                if not nome_disciplina:
                    continue

                try:
                    # busca disciplina pelo nome e turma
                    disc = Disciplina.objects.get(
                        nome=nome_disciplina,
                        turma=g.turma,
                    )
                except Disciplina.DoesNotExist:
                    continue

                prof_id = disc.professor_id

                # inicializa conjunto
                if prof_id not in ocupados:
                    ocupados[prof_id] = set()

                # marca ocupação
                ocupados[prof_id].add((dia, idx))

    # =============================================================
    # 2) SALVAR GRADE (POST)
    # =============================================================

    if request.method == "POST":

        new_data = {dia: [] for dia in dias}

        # percorre horários
        for i in range(len(horarios)):
            for dia in dias:

                campo = f"{dia}_{i}"
                valor = request.POST.get(campo, "")

                new_data[dia].append(valor)

        # salva nova grade
        grade.dados = new_data
        grade.save()

        messages.success(request, "Grade horária atualizada com sucesso!")

        return redirect("grade_horaria", turma_id=turma.id)

    # =============================================================
    # 3) MONTAR TABELA PARA TEMPLATE
    # =============================================================

    rows = []

    for i, horario in enumerate(horarios):

        row = {
            "index": i,
            "horario": horario,
            "cols": [],
        }

        for dia in dias:

            lista = grade.dados.get(dia, [])

            # valor atual da célula
            valor = lista[i] if isinstance(lista, list) and i < len(lista) else ""

            # ================= FILTRO DE DISPONIBILIDADE =================

            disciplinas_disponiveis = []

            for d in disciplinas_turma:

                prof_id = d.professor_id

                # verifica se professor está ocupado
                if prof_id in ocupados and (dia, i) in ocupados[prof_id]:
                    continue

                disciplinas_disponiveis.append(d)

            row["cols"].append(
                {
                    "dia": dia,
                    "valor": valor,
                    "disciplinas": disciplinas_disponiveis,  # ← envia disciplinas filtradas para este horário/dia
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
            "disciplinas": disciplinas_turma,  # ainda enviado para o loop externo
        },
    )
