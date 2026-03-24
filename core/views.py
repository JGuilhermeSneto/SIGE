# ======================== IMPORTS ========================

import calendar  # importa módulo para trabalhar com calendários
from datetime import (  # importa classe para manipular datas e horários
    datetime,
    timezone,
)


from django.contrib import messages  # sistema de mensagens para o usuário
from django.contrib.auth import logout  # funções de autenticação
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import (  # controle de acesso
    login_required,
    user_passes_test,
)
from django.shortcuts import (  # atalhos para redirecionar e renderizar páginas
    get_object_or_404,
    redirect,
    render,
)

from .forms import EditarPerfilForm  # formulários do sistema
from .forms import AlunoForm, GestorForm, LoginForm, ProfessorForm
from .models import Gestor  # modelos do banco de dados
from .models import Aluno, Disciplina, GradeHorario, Nota, Professor, Turma
from django.utils import timezone 
agora = timezone.localtime()
# ======================== FUNÇÕES AUXILIARES ========================


def get_user_profile(user):
    # verifica se o usuário possui perfil de professor
    if hasattr(user, "professor"):
        return user.professor  # retorna o objeto professor

    # verifica se o usuário possui perfil de aluno
    if hasattr(user, "aluno"):
        return user.aluno  # retorna o objeto aluno

    # verifica se o usuário possui perfil de gestor
    if hasattr(user, "gestor"):
        return user.gestor  # retorna o objeto gestor

    return None  # caso não tenha nenhum perfil


def redirect_user(user):
    # se for superusuário ou gestor
    if user.is_superuser or hasattr(user, "gestor"):
        return "painel_super"  # redireciona para painel admin

    # se for professor
    if hasattr(user, "professor"):
        return "painel_professor"  # redireciona para painel professor

    # se for aluno
    if hasattr(user, "aluno"):
        return "painel_aluno"  # redireciona para painel aluno

    return "login"  # padrão caso não encaixe em nenhum caso


def gerar_calendario():
    hoje = datetime.today()  # pega a data atual

    # gera uma matriz com os dias do mês (semanas)
    cal = calendar.monthcalendar(hoje.year, hoje.month)

    # percorre semanas e dias transformando em lista de dicionários
    return [
        {
            "numero": dia,  # número do dia
            "vazio": dia == 0,  # verifica se é espaço vazio
            "hoje": dia == hoje.day,  # verifica se é o dia atual
        }
        for semana in cal  # percorre cada semana
        for dia in semana  # percorre cada dia da semana
    ]


def is_super_ou_gestor(user):
    # retorna verdadeiro se for superusuário ou gestor
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
        return redirect(redirect_user(request.user))  # redireciona

    form = LoginForm(request.POST or None)  # cria formulário

    # se for envio POST e formulário válido
    if request.method == "POST" and form.is_valid():

        user = form.get_user()  # obtém usuário autenticado
        login(request, user)  # realiza login

        return redirect(redirect_user(user))  # redireciona

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

    # busca anos únicos no banco
    anos_disponiveis = list(
        Turma.objects.values_list("ano", flat=True)  # pega apenas campo ano
        .distinct()  # remove duplicados
        .order_by("-ano")  # ordena decrescente
    )

    # se não houver anos
    if not anos_disponiveis:
        anos_disponiveis = [ano_atual]  # usa ano atual

    ano_filtro = request.GET.get("ano")  # pega valor da URL

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

    total_turmas = turmas.count()  # conta turmas

    # conta alunos distintos
    total_alunos = Aluno.objects.filter(turma__in=turmas).distinct().count()

    # conta professores distintos
    total_professores = (
        Professor.objects.filter(disciplina__turma__in=turmas).distinct().count()
    )

    # conta disciplinas distintas
    total_disciplinas = Disciplina.objects.filter(turma__in=turmas).distinct().count()

    # renderiza página
    return render(
        request,
        "superusuario/painel_super.html",
        {
            "usuario": request.user,
            "total_professores": total_professores,
            "total_alunos": total_alunos,
            "total_turmas": total_turmas,
            "total_disciplinas": total_disciplinas,
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

    # define se pode ver gestores
    pode_ver_gestores = user.is_superuser or (
        hasattr(user, "gestor") and user.gestor.cargo in ("diretor", "vice_diretor")
    )

    return render(
        request,
        "core/usuarios.html",
        {"pode_ver_gestores": pode_ver_gestores},
    )


# ========================== PERFIL ==========================


@login_required
def editar_perfil(request):

    user = request.user  # usuário atual
    perfil = get_user_profile(user)  # pega perfil

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

        return redirect(redirect_user(user))

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


# ========================== FOTO ==========================


@login_required
def remover_foto_perfil(request):

    perfil = get_user_profile(request.user)  # pega perfil

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


# ========================== PROFESSORES ==========================


@login_required
@user_passes_test(is_super_ou_gestor)
def listar_professores(request):

    query = request.GET.get("q", "").strip()  # pega busca

    professores = Professor.objects.all()  # busca todos

    if query:
        professores = professores.filter(nome_completo__icontains=query)

    return render(
        request,
        "professor/listar_professores.html",
        {"professores": professores, "query": query},
    )


@login_required
@user_passes_test(is_super_ou_gestor)
def cadastrar_professor(request):

    form = ProfessorForm(
        request.POST or None,
        request.FILES or None,
        request=request,
    )

    if request.method == "POST" and form.is_valid():

        professor = form.save()  # salva professor

        messages.success(
            request,
            f"Professor(a) {professor.nome_completo} cadastrado(a) com sucesso!",
        )

        return redirect("listar_professores")

    if request.method == "POST":
        for erros in form.errors.values():
            for erro in erros:
                messages.error(request, erro)

    return render(
        request,
        "professor/cadastrar_professor.html",
        {"form": form},
    )


# ========================== EDITAR PROFESSOR ==========================


@login_required  # exige que o usuário esteja autenticado
@user_passes_test(lambda u: u.is_superuser or hasattr(u, "gestor"))  # exige permissão
def editar_professor(request, professor_id):
    # busca o professor pelo id ou retorna erro 404 se não existir
    professor = get_object_or_404(Professor, id=professor_id)

    # cria o formulário com dados ou vazio
    form = ProfessorForm(
        request.POST or None,  # dados do formulário (POST) ou None
        request.FILES or None,  # arquivos enviados ou None
        instance=professor,  # define que é edição (não criação)
        request=request,  # passa request para o form
    )

    # se for envio POST e formulário válido
    if request.method == "POST" and form.is_valid():

        form.save()  # salva alterações no professor

        # mensagem de sucesso
        messages.success(
            request,
            f"Professor(a) {professor.nome_completo} atualizado(a) com sucesso!",
        )

        return redirect("listar_professores")  # redireciona para listagem

    # se for POST e tiver erro, exibe mensagens
    if request.method == "POST":
        for erros in form.errors.values():  # percorre erros por campo
            for erro in erros:  # percorre cada erro
                messages.error(request, erro)  # mostra erro na tela

    # renderiza a mesma tela de cadastro (reutilização de template)
    return render(
        request,
        "professor/cadastrar_professor.html",
        {
            "form": form,  # envia formulário
            "professor": professor,  # envia objeto professor
        },
    )


# ========================== EXCLUIR PROFESSOR ==========================


@login_required  # exige login
@user_passes_test(lambda u: u.is_superuser or hasattr(u, "gestor"))  # exige permissão
def excluir_professor(request, professor_id):

    # busca professor ou retorna erro 404
    professor = get_object_or_404(Professor, id=professor_id)

    # remove usuário associado (caso exista)
    if hasattr(professor, "user") and professor.user:
        professor.user.delete()  # exclui usuário do sistema

    professor.delete()  # exclui o professor do banco

    # mensagem de sucesso
    messages.success(request, "Professor removido.")

    return redirect("listar_professores")  # volta para listagem


# ========================== GESTOR ==========================


@login_required  # exige login
@user_passes_test(lambda u: u.is_superuser)  # apenas superusuário pode acessar
def cadastrar_gestor(request):

    # cria formulário com ou sem dados
    form = GestorForm(
        request.POST or None,  # dados enviados ou None
        request.FILES or None,  # arquivos enviados ou None
        request=request,  # passa request para o form
    )

    # se for envio POST e válido
    if request.method == "POST" and form.is_valid():

        gestor = form.save()  # salva gestor (inclui criação de usuário)

        # mensagem de sucesso com cargo formatado
        messages.success(
            request,
            f"{gestor.get_cargo_display()} {gestor.nome_completo} cadastrado com sucesso!",
        )

        return redirect("listar_gestores")  # redireciona

    # se houver erro no formulário
    if request.method == "POST":
        for erros in form.errors.values():  # percorre erros
            for erro in erros:
                messages.error(request, erro)  # mostra erro

    # renderiza página de cadastro
    return render(
        request,
        "gestor/cadastrar_gestor.html",
        {
            "form": form,  # envia formulário
        },
    )


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


# ========================== LISTAR ALUNOS ==========================


@login_required  # exige que o usuário esteja logado
@user_passes_test(lambda u: u.is_superuser or hasattr(u, "gestor"))  # exige permissão
def listar_alunos(request):

    query = request.GET.get("q", "").strip()  # pega valor da busca e remove espaços

    alunos = Aluno.objects.all()  # busca todos os alunos

    # se houver texto na busca
    if query:
        alunos = alunos.filter(nome_completo__icontains=query)  # filtra pelo nome

    # renderiza página com lista de alunos
    return render(
        request,
        "aluno/listar_alunos.html",
        {
            "alunos": alunos,  # lista de alunos
            "query": query,  # valor digitado na busca
        },
    )


# ========================== CADASTRAR ALUNO ==========================


@login_required  # exige login
@user_passes_test(lambda u: u.is_superuser or hasattr(u, "gestor"))  # exige permissão
def cadastrar_aluno(request):

    # cria formulário com dados enviados ou vazio
    form = AlunoForm(
        request.POST or None,  # dados do formulário ou None
        request.FILES or None,  # arquivos enviados ou None
        request=request,  # passa request para o form
    )

    # se for envio POST e válido
    if request.method == "POST" and form.is_valid():

        aluno = form.save()  # salva aluno no banco

        # mensagem de sucesso
        messages.success(
            request,
            f"Aluno(a) {aluno.nome_completo} cadastrado(a) com sucesso!",
        )

        return redirect("listar_alunos")  # redireciona

    # se houver erro no formulário
    if request.method == "POST":
        for erros in form.errors.values():  # percorre erros por campo
            for erro in erros:  # percorre cada erro
                messages.error(request, erro)  # exibe erro

    # renderiza página de cadastro
    return render(
        request,
        "aluno/cadastrar_aluno.html",
        {
            "form": form,  # envia formulário
        },
    )


# ========================== EDITAR ALUNO ==========================


@login_required  # exige login
@user_passes_test(lambda u: u.is_superuser or hasattr(u, "gestor"))  # exige permissão
def editar_aluno(request, aluno_id):

    # busca aluno pelo id ou retorna erro 404
    aluno = get_object_or_404(Aluno, id=aluno_id)

    # cria formulário com dados ou vazio
    form = AlunoForm(
        request.POST or None,  # dados enviados ou None
        request.FILES or None,  # arquivos enviados ou None
        instance=aluno,  # define edição
        request=request,  # passa request para o form
    )

    # se for envio POST e válido
    if request.method == "POST" and form.is_valid():

        aluno = form.save()  # salva alterações

        # mensagem de sucesso
        messages.success(
            request,
            f"Aluno(a) {aluno.nome_completo} atualizado(a) com sucesso!",
        )

        return redirect("listar_alunos")  # redireciona

    # se houver erro no formulário
    if request.method == "POST":
        for erros in form.errors.values():  # percorre erros
            for erro in erros:
                messages.error(request, erro)  # exibe erro

    # renderiza mesma tela de cadastro (reutilização)
    return render(
        request,
        "aluno/cadastrar_aluno.html",
        {
            "form": form,  # formulário
            "aluno": aluno,  # objeto aluno
        },
    )


# ========================== EXCLUIR ALUNO ==========================


@login_required  # exige que o usuário esteja autenticado
@user_passes_test(lambda u: u.is_superuser or hasattr(u, "gestor"))  # exige permissão
def excluir_aluno(request, aluno_id):

    # busca aluno pelo id ou retorna erro 404
    aluno = get_object_or_404(Aluno, id=aluno_id)

    # verifica se existe usuário associado antes de deletar
    if hasattr(aluno, "user") and aluno.user:
        aluno.user.delete()  # remove usuário vinculado

    aluno.delete()  # remove aluno do banco

    # mensagem de sucesso
    messages.success(request, "Aluno removido com sucesso.")

    return redirect("listar_alunos")  # redireciona para lista


# ========================== VISUALIZAR DISCIPLINA ==========================


@login_required  # exige login
def visualizar_disciplinas(request, disciplina_id):

    # busca disciplina pelo id ou retorna erro 404
    disciplina = get_object_or_404(Disciplina, id=disciplina_id)

    user = request.user  # usuário logado

    # ========================== CONTROLE DE ACESSO ==========================

    # verifica se o usuário tem permissão
    tem_permissao = (
        user.is_superuser  # superusuário
        or hasattr(user, "gestor")  # gestor
        or (
            hasattr(user, "professor")  # professor
            and disciplina.professor == user.professor  # professor da disciplina
        )
    )

    # se não tiver permissão
    if not tem_permissao:
        messages.error(
            request,
            "Você não tem permissão para visualizar esta disciplina.",
        )
        return redirect("login")  # redireciona

    # ========================== DADOS ==========================

    turma = disciplina.turma  # turma da disciplina

    # lista de alunos da turma ordenados por nome
    alunos = Aluno.objects.filter(turma=turma).order_by("nome_completo")

    # busca todas as notas da disciplina
    notas = Nota.objects.filter(disciplina=disciplina)

    # cria dicionário: aluno_id -> nota (facilita acesso no template)
    notas_dict = {nota.aluno.id: nota for nota in notas}

    # ========================== CONTEXTO ==========================

    context = {
        "disciplina": disciplina,  # disciplina atual
        "turma": turma,  # turma associada
        "alunos": alunos,  # lista de alunos
        "notas": notas,  # lista de notas
        "notas_dict": notas_dict,  # dicionário para acesso rápido
    }

    # renderiza template com dados
    return render(
        request,
        "disciplina/visualizar_disciplinas.html",
        context,
    )


# ========================== EDITAR DISCIPLINA ==========================


@login_required  # exige que o usuário esteja autenticado
@user_passes_test(lambda u: u.is_superuser or hasattr(u, "gestor"))  # exige permissão
def editar_disciplina(request, disciplina_id):

    # busca disciplina pelo id ou retorna erro 404
    disciplina = get_object_or_404(Disciplina, id=disciplina_id)

    # lista de professores disponíveis (exclui superusuários)
    professores = Professor.objects.filter(user__is_superuser=False)

    # ========================== PROCESSAMENTO POST ==========================

    if request.method == "POST":

        # pega dados enviados pelo formulário
        nome = request.POST.get("nome", "").strip()  # nome da disciplina
        professor_id = request.POST.get("professor")  # id do professor

        # validação simples
        if not nome or not professor_id:
            messages.error(request, "Preencha todos os campos obrigatórios.")
        else:
            # busca professor ou retorna erro 404
            professor = get_object_or_404(Professor, id=professor_id)

            # atualiza dados da disciplina
            disciplina.nome = nome
            disciplina.professor = professor
            disciplina.save()  # salva no banco

            # mensagem de sucesso
            messages.success(request, "Disciplina atualizada com sucesso!")

            # redireciona para lista de disciplinas da turma
            return redirect(
                "listar_disciplinas_turma",
                turma_id=disciplina.turma.id,
            )

    # ========================== RENDER ==========================

    return render(
        request,
        "disciplina/cadastrar_disciplina_turma.html",
        {
            "disciplina": disciplina,  # disciplina atual
            "turma": disciplina.turma,  # turma associada
            "professores": professores,  # lista de professores
        },
    )


# ========================== EXCLUIR DISCIPLINA ==========================


@login_required  # exige login
@user_passes_test(lambda u: u.is_superuser or hasattr(u, "gestor"))  # exige permissão
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


@login_required  # exige login
@user_passes_test(lambda u: u.is_superuser or hasattr(u, "gestor"))  # exige permissão
def listar_turmas(request):

    # pega ano atual considerando timezone do Django
    ano_atual = timezone.localtime(timezone.now()).year

    query = request.GET.get("q", "").strip()  # busca por nome da turma

    # ========================== ANOS DISPONÍVEIS ==========================

    # busca anos distintos no banco
    anos_disponiveis_qs = (
        Turma.objects.values_list("ano", flat=True).distinct().order_by("-ano")
    )

    anos_disponiveis = list(anos_disponiveis_qs)  # converte para lista

    # se não houver anos no banco, usa ano atual
    if not anos_disponiveis:
        anos_disponiveis = [ano_atual]

    # ========================== FILTRO DE ANO ==========================

    ano_filtro = request.GET.get("ano")  # pega ano da URL

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

    # ========================== RENDER ==========================

    return render(
        request,
        "turma/listar_turmas.html",
        {
            "turmas": turmas,  # lista de turmas
            "query": query,  # valor da busca
            "ano_filtro": ano_filtro,  # ano selecionado
            "anos_disponiveis": anos_disponiveis,  # lista de anos
        },
    )


# ========================== CADASTRAR TURMA ==========================


@login_required  # exige que o usuário esteja autenticado
@user_passes_test(lambda u: u.is_superuser or hasattr(u, "gestor"))  # exige permissão
def cadastrar_turma(request):

    erro = None  # variável para armazenar mensagens de erro

    # pega ano atual
    ano_atual = datetime.now().year

    # cria lista de anos permitidos (2010 até próximo ano)
    anos = list(range(2010, ano_atual + 2))

    # ========================== PROCESSAMENTO POST ==========================

    if request.method == "POST":

        # pega dados do formulário
        nome = request.POST.get("nome", "").strip()  # nome da turma
        turno = request.POST.get("turno", "").strip()  # turno da turma
        ano = request.POST.get("ano")  # ano informado

        # ========================== VALIDAÇÕES ==========================

        # valida se todos os campos foram preenchidos
        if not nome or not turno or not ano:
            erro = "Todos os campos são obrigatórios."

        else:
            try:
                ano = int(ano)  # tenta converter ano para inteiro
            except (TypeError, ValueError):
                erro = "Ano letivo inválido."
            else:
                # valida intervalo de ano permitido
                if ano < 2010 or ano > ano_atual + 1:
                    erro = "O ano letivo deve ser entre 2010 e o próximo ano."

                # verifica se já existe turma com mesmo nome e ano
                elif Turma.objects.filter(nome=nome, ano=ano).exists():
                    erro = "Essa turma já existe neste ano."

                else:
                    # cria nova turma no banco
                    Turma.objects.create(nome=nome, turno=turno, ano=ano)

                    # mensagem de sucesso
                    messages.success(request, "Turma cadastrada com sucesso!")

                    return redirect("listar_turmas")  # redireciona

    # ========================== RENDER ==========================

    return render(
        request,
        "turma/cadastrar_turma.html",
        {
            "erro": erro,  # mensagem de erro (se existir)
            "anos": anos,  # lista de anos para o select
        },
    )


# ========================== EDITAR TURMA ==========================


@login_required  # exige login
@user_passes_test(lambda u: u.is_superuser or hasattr(u, "gestor"))  # exige permissão
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

        # pega dados do formulário
        nome = request.POST.get("nome", "").strip()
        turno = request.POST.get("turno", "").strip()
        ano = request.POST.get("ano")

        # valida campos obrigatórios
        if not nome or not turno or not ano:
            erro = "Todos os campos são obrigatórios."

        else:
            try:
                ano = int(ano)  # converte ano
            except (TypeError, ValueError):
                erro = "Ano letivo inválido."
            else:
                # valida intervalo permitido
                if ano < 2010 or ano > ano_atual + 1:
                    erro = "Ano fora do intervalo permitido."

                # verifica duplicidade ignorando a própria turma
                elif (
                    Turma.objects.filter(nome=nome, ano=ano)
                    .exclude(id=turma.id)
                    .exists()
                ):
                    erro = "Já existe outra turma com esse nome neste ano."

                else:
                    # atualiza dados da turma
                    turma.nome = nome
                    turma.turno = turno
                    turma.ano = ano
                    turma.save()  # salva no banco

                    # mensagem de sucesso
                    messages.success(request, "Turma atualizada com sucesso!")

                    return redirect("listar_turmas")  # redireciona

    # ========================== RENDER ==========================

    return render(
        request,
        "turma/cadastrar_turma.html",
        {
            "turma": turma,  # envia turma para edição
            "erro": erro,  # envia erro (se houver)
            "anos": anos,  # lista de anos
        },
    )


# ========================== EXCLUIR TURMA ==========================


@login_required  # exige que o usuário esteja autenticado
@user_passes_test(
    lambda u: u.is_superuser
    or (hasattr(u, "gestor") and u.gestor.cargo != "secretario")  # regra de permissão
)
def excluir_turma(request, turma_id):

    # busca turma pelo id ou retorna erro 404
    turma = get_object_or_404(Turma, id=turma_id)

    turma.delete()  # remove turma do banco

    # mensagem de sucesso
    messages.success(request, "Turma excluída com sucesso!")

    return redirect("listar_turmas")  # redireciona


# ========================== PAINEL PROFESSOR ==========================


@login_required  # exige login
def painel_professor(request):
    """Tela principal do professor com estatísticas e visão geral"""

    # verifica se usuário tem perfil de professor
    if not hasattr(request.user, "professor"):
        return redirect("login")  # redireciona se não for professor

    professor = request.user.professor  # pega perfil do professor

    foto_perfil_url = get_foto_perfil(request.user)  # pega foto do perfil

    # ========================== DISCIPLINAS ==========================

    # busca disciplinas do professor com join na turma (melhora performance)
    disciplinas = Disciplina.objects.filter(professor=professor).select_related("turma")

    # ========================== ANOS DISPONÍVEIS ==========================

    # busca anos das turmas onde o professor leciona
    anos_disponiveis_qs = (
        Turma.objects.filter(disciplina__professor=professor)
        .values_list("ano", flat=True)
        .distinct()
        .order_by("-ano")
    )

    anos_disponiveis = list(anos_disponiveis_qs)  # converte para lista

    ano_atual = datetime.now().year  # pega ano atual

    # se não houver anos no banco
    if not anos_disponiveis:
        anos_disponiveis = [ano_atual]

    # ========================== FILTRO DE ANO ==========================

    ano_filtro = request.GET.get("ano")  # pega ano da URL

    if ano_filtro:
        try:
            ano_filtro = int(ano_filtro)  # converte para inteiro
            request.session["ano_filtro_professor"] = ano_filtro  # salva na sessão
        except ValueError:
            # usa valor salvo ou ano atual
            ano_filtro = request.session.get("ano_filtro_professor", ano_atual)
    else:
        # tenta pegar da sessão
        ano_filtro = request.session.get("ano_filtro_professor", ano_atual)

    # garante que o ano está na lista
    if ano_filtro not in anos_disponiveis:
        anos_disponiveis.append(ano_filtro)
        anos_disponiveis.sort(reverse=True)

    # ========================== FILTRO DE DISCIPLINAS ==========================

    disciplinas_filtradas = disciplinas.filter(turma__ano=ano_filtro)

    # ========================== ESTATÍSTICAS ==========================

    total_disciplinas = disciplinas_filtradas.count()  # total de disciplinas

    # conta turmas únicas
    total_turmas = disciplinas_filtradas.values("turma").distinct().count()

    # ========================== TOTAL DE ALUNOS ==========================

    alunos_ids = set()  # usa set para evitar duplicidade

    for disciplina in disciplinas_filtradas:
        # pega ids dos alunos da turma
        alunos_turma = Aluno.objects.filter(turma=disciplina.turma).values_list(
            "id", flat=True
        )
        alunos_ids.update(alunos_turma)  # adiciona ao set

    total_alunos = len(alunos_ids)  # total sem duplicação

    # ========================== NOTAS ==========================

    total_notas_possiveis = 0  # total de notas possíveis
    total_notas_lancadas = 0  # total de notas já lançadas

    for disciplina in disciplinas_filtradas:

        # quantidade de alunos da turma
        alunos_count = Aluno.objects.filter(turma=disciplina.turma).count()

        total_notas_possiveis += alunos_count * 4  # 4 notas por aluno

        # busca notas da disciplina
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

    # ========================== DETALHAMENTO ==========================

    disciplinas_detalhadas = []  # lista final

    for disciplina in disciplinas_filtradas:

        # quantidade de alunos da turma
        alunos_count = Aluno.objects.filter(turma=disciplina.turma).count()

        notas_disciplina = Nota.objects.filter(disciplina=disciplina)

        notas_lancadas_disc = 0  # contador por disciplina

        # conta notas preenchidas
        for nota in notas_disciplina:
            if nota.nota1 is not None:
                notas_lancadas_disc += 1
            if nota.nota2 is not None:
                notas_lancadas_disc += 1
            if nota.nota3 is not None:
                notas_lancadas_disc += 1
            if nota.nota4 is not None:
                notas_lancadas_disc += 1

        notas_possiveis_disc = alunos_count * 4  # total possível

        # calcula percentual (evita divisão por zero)
        percentual = int(
            (notas_lancadas_disc / notas_possiveis_disc * 100)
            if notas_possiveis_disc > 0
            else 0
        )

        # adiciona dados na lista
        disciplinas_detalhadas.append(
            {
                "disciplina": disciplina,
                "alunos_count": alunos_count,
                "notas_lancadas": notas_lancadas_disc,
                "notas_possiveis": notas_possiveis_disc,
                "percentual": percentual,
            }
        )

    # ========================== RENDER ==========================

    return render(
        request,
        "professor/painel_professor.html",
        {
            "professor": professor,  # objeto professor
            "nome_exibicao": professor.nome_completo,  # nome exibido
            "total_disciplinas": total_disciplinas,
            "total_turmas": total_turmas,
            "total_alunos": total_alunos,
            "total_notas_lancadas": total_notas_lancadas,
            "total_notas_possiveis": total_notas_possiveis,
            "disciplinas_detalhadas": disciplinas_detalhadas,
            "foto_perfil_url": foto_perfil_url,
            "agora": datetime.now(),  # data atual
            "calendario": gerar_calendario(),  # calendário do mês
            "anos_disponiveis": anos_disponiveis,
            "ano_filtro": ano_filtro,
        },
    )


##✅ refatorado

# ==================== LISTAR TURMAS DO PROFESSOR ====================


@login_required  # exige que o usuário esteja autenticado
def disciplinas_professor(request):
    """Lista todas as turmas onde o professor leciona com filtro de ano"""

    # verifica se o usuário possui perfil de professor
    if not hasattr(request.user, "professor"):
        return redirect("login")  # redireciona se não for professor

    professor = request.user.professor  # obtém o professor logado

    foto_perfil_url = get_foto_perfil(request.user)  # obtém foto de perfil

    # ==================== TURMAS DO PROFESSOR ====================

    # busca ids das turmas onde o professor leciona
    turmas_ids = (
        Disciplina.objects.filter(professor=professor)
        .values_list("turma_id", flat=True)
        .distinct()
    )

    # ==================== ANOS DISPONÍVEIS ====================

    # busca anos distintos das turmas
    anos_disponiveis_qs = (
        Turma.objects.filter(id__in=turmas_ids)
        .values_list("ano", flat=True)
        .distinct()
        .order_by("-ano")
    )

    anos_disponiveis = list(anos_disponiveis_qs)  # converte para lista

    ano_atual = datetime.now().year  # ano atual

    # se não houver dados, usa ano atual
    if not anos_disponiveis:
        anos_disponiveis = [ano_atual]

    # ==================== FILTRO DE ANO ====================

    ano_filtro = request.GET.get("ano")  # pega da URL

    if ano_filtro:
        try:
            ano_filtro = int(ano_filtro)  # converte para inteiro
            request.session["ano_filtro_professor"] = ano_filtro  # salva na sessão
        except ValueError:
            # fallback para valor salvo ou atual
            ano_filtro = request.session.get("ano_filtro_professor", ano_atual)
    else:
        # tenta recuperar da sessão
        ano_filtro = request.session.get("ano_filtro_professor", ano_atual)

    # garante que o ano está na lista
    if ano_filtro not in anos_disponiveis:
        anos_disponiveis.append(ano_filtro)
        anos_disponiveis.sort(reverse=True)

    # ==================== CONSULTA DE TURMAS ====================

    # filtra turmas pelo professor e ano
    turmas = Turma.objects.filter(id__in=turmas_ids, ano=ano_filtro).order_by("nome")

    # ==================== FILTRO DE BUSCA ====================

    query = request.GET.get("q", "").strip()  # pega termo de busca

    if query:
        turmas = turmas.filter(nome__icontains=query)  # filtra por nome

    # ==================== DETALHAMENTO ====================

    turmas_detalhadas = []  # lista final

    for turma in turmas:

        # busca disciplinas do professor nessa turma
        disciplinas_turma = Disciplina.objects.filter(
            turma=turma,
            professor=professor,
        )

        # conta alunos da turma
        alunos_count = Aluno.objects.filter(turma=turma).count()

        # adiciona dados na lista
        turmas_detalhadas.append(
            {
                "turma": turma,  # objeto turma
                "disciplinas_count": disciplinas_turma.count(),  # total de disciplinas
                "alunos_count": alunos_count,  # total de alunos
                "turno_display": turma.get_turno_display(),  # texto do turno
            }
        )

    # ==================== RENDER ====================

    return render(
        request,
        "professor/disciplinas_professor.html",
        {
            "turmas_detalhadas": turmas_detalhadas,  # lista final
            "foto_perfil_url": foto_perfil_url,  # foto do usuário
            "query": query,  # valor da busca
            "anos_disponiveis": anos_disponiveis,  # lista de anos
            "ano_filtro": ano_filtro,  # ano selecionado
        },
    )


##✅✅ refatorado

#@login_required
def disciplinas_turma(request, turma_id):
    """
    Mostra as disciplinas de uma turma específica.
    Permite acesso para professor, gestor ou superusuário.
    """

    user = request.user
    turma = get_object_or_404(Turma, id=turma_id)
    foto_perfil_url = get_foto_perfil(user)

    # ==================== VERIFICA PERFIL ====================
    if hasattr(user, "professor"):
        disciplinas = Disciplina.objects.filter(turma=turma, professor=user.professor).order_by("nome")
        tipo_usuario = "professor"
    elif hasattr(user, "gestor") or user.is_superuser:
        disciplinas = Disciplina.objects.filter(turma=turma).order_by("nome")
        tipo_usuario = "gestor"
    else:
        return redirect("login")

    # ==================== DADOS DE ALUNOS E NOTAS ====================
    alunos_count = Aluno.objects.filter(turma=turma).count()
    disciplinas_detalhadas = []

    for disciplina in disciplinas:
        notas_disciplina = Nota.objects.filter(disciplina=disciplina)
        notas_lancadas = sum(
            bool(n.nota1) + bool(n.nota2) + bool(n.nota3) + bool(n.nota4)
            for n in notas_disciplina
        )
        notas_possiveis = alunos_count * 4
        percentual = int((notas_lancadas / notas_possiveis * 100) if notas_possiveis > 0 else 0)

        disciplinas_detalhadas.append({
            "disciplina": disciplina,
            "professor_nome": disciplina.professor.nome_completo if disciplina.professor else "Não atribuído",
            "alunos_count": alunos_count,
            "notas_lancadas": notas_lancadas,
            "notas_possiveis": notas_possiveis,
            "percentual": percentual,
        })

    # ==================== RENDERIZA TEMPLATE ====================
    return render(
        request,
        "disciplina/visualizar_disciplinas.html",
        {
            "turma": turma,
            "disciplinas_detalhadas": disciplinas_detalhadas,
            "foto_perfil_url": foto_perfil_url,
            "tipo_usuario": tipo_usuario,
        },
    )


@login_required  # exige que o usuário esteja autenticado
def visualizar_grade_professor(request, turma_id):
    """Visualização da grade horária para o professor (somente leitura)"""

    # verifica se o usuário possui perfil de professor
    if not hasattr(request.user, "professor"):
        return redirect("login")  # redireciona se não for professor

    professor = request.user.professor  # obtém professor logado

    # busca turma pelo id ou retorna erro 404
    turma = get_object_or_404(Turma, id=turma_id)

    # ==================== VALIDAÇÃO DE ACESSO ====================

    # verifica se o professor leciona nesta turma
    disciplinas_prof = Disciplina.objects.filter(
        turma=turma,
        professor=professor,
    )

    if not disciplinas_prof.exists():
        messages.error(
            request,
            "Você não leciona nenhuma disciplina nesta turma.",
        )
        return redirect("disciplinas_professor")  # redireciona

    # ==================== HORÁRIOS POR TURNO ====================

    # normaliza o texto do turno (remove acentos simples)
    turno_key = turma.turno.lower().replace("ã", "a").replace("á", "a")

    # dicionário com horários por turno
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

    # pega horários conforme turno da turma
    horarios = HORARIOS.get(turno_key, [])

    grade_formatada = None  # estrutura final da grade

    # ==================== BUSCA DA GRADE ====================

    try:
        # tenta buscar grade da turma
        grade_obj = GradeHorario.objects.get(turma=turma)

        # só processa se houver horários e dados
        if horarios and grade_obj.dados:

            grade_formatada = {}  # inicializa dicionário

            dias_semana = ["segunda", "terca", "quarta", "quinta", "sexta"]

            # percorre horários por índice
            for i, horario in enumerate(horarios):

                linha = {}  # dados da linha atual

                # percorre dias da semana
                for dia in dias_semana:

                    # lista de aulas do dia
                    aulas_dia = grade_obj.dados.get(dia, [])

                    # pega valor seguro (evita index error)
                    valor = aulas_dia[i] if i < len(aulas_dia) else ""

                    linha[dia] = valor  # adiciona ao dicionário

                # adiciona linha completa ao horário
                grade_formatada[horario] = linha

    except GradeHorario.DoesNotExist:
        grade_formatada = None  # mantém vazio se não existir

    # ==================== RENDER ====================

    return render(
        request,
        "professor/visualizar_grade_professor.html",
        {
            "turma": turma,  # turma atual
            "grade_horario": grade_formatada,  # grade estruturada
            "disciplinas_professor": disciplinas_prof,  # disciplinas do professor
        },
    )


##✅✅ corrijido


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
        "professor/lancar_nota.html",
        {
            "disciplina": disciplina,
            "alunos": alunos,
            "notas_dict": notas_dict,
        },
    )


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
        "aluno/painel_aluno.html",
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


# ==================== GRADE HORÁRIA ====================


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

    # normaliza turno
    turno_key = turma.turno.lower().replace("ã", "a").replace("á", "a")

    # pega horários do turno
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

    ocupados = {}  # {professor_id: {(dia, index)}}

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

            # adiciona coluna
            row["cols"].append(
                {
                    "dia": dia,
                    "valor": valor,
                    "disciplinas": disciplinas_disponiveis,
                }
            )

        rows.append(row)

    # ==================== RENDER ====================

    return render(
        request,
        "core/grade_horaria.html",
        {
            "turma": turma,
            "nomes_dias": nomes_dias,
            "rows": rows,
            "disciplinas": disciplinas_turma,
        },
    )

@login_required
def cadastrar_disciplina_para_turma(request, turma_id):
    turma = get_object_or_404(Turma, id=turma_id)

    if request.method == "POST":
        nome = request.POST.get("nome", "").strip()
        professor_id = request.POST.get("professor")
        if not nome or not professor_id:
            messages.error(request, "Todos os campos são obrigatórios.")
        else:
            # cria disciplina
            Disciplina.objects.create(nome=nome, turma=turma, professor_id=professor_id)
            messages.success(request, "Disciplina cadastrada com sucesso!")
            return redirect("disciplinas_turma", turma_id=turma.id)

    # caso GET
    return render(request, "disciplina/cadastrar_disciplina_turma.html", {"turma": turma})