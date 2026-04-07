"""
Módulo de views da aplicação core do sistema SIGE.
"""

import calendar
from datetime import date, datetime
from django.templatetags.static import static
from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.timezone import now

from .forms import (AlunoForm, EditarPerfilForm, GestorForm, LoginForm,
                    ProfessorForm)
from .models import (Aluno, Disciplina, Frequencia, Gestor, GradeHorario, Nota,
                     Professor, Turma)

# =====================================================================
# Constantes
# =====================================================================

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


# =====================================================================
# Funções Auxiliares
# =====================================================================
def _calcular_situacao_aluno(media_final, frequencia_percentual):
    """
    Define a situação acadêmica do aluno baseada em notas e faltas.
    Regra: Média >= 7 e Frequência >= 75% -> Aprovado
    """
    # Regras de negócio (ajuste os valores se a sua escola usar critérios diferentes)
    MEDIA_APROVACAO = 7.0
    MEDIA_RECUPERACAO = 5.0
    FREQUENCIA_MINIMA = 75.0

    if frequencia_percentual < FREQUENCIA_MINIMA:
        return {
            "texto": "Reprovado por Falta",
            "classe": "badge bg-danger",
            "aprovado": False,
        }

    if media_final >= MEDIA_APROVACAO:
        return {"texto": "Aprovado", "classe": "badge bg-success", "aprovado": True}
    elif media_final >= MEDIA_RECUPERACAO:
        return {
            "texto": "Recuperação",
            "classe": "badge bg-warning text-dark",
            "aprovado": False,
        }
    else:
        return {"texto": "Reprovado", "classe": "badge bg-danger", "aprovado": False}


def _get_grade_formatada(nota_valor):
    """
    Formata o valor da nota para exibição no boletim e define a classe CSS de cor.
    Útil para tabelas de notas de alunos.
    """
    if nota_valor is None:
        return {"valor": "-", "classe": "text-muted"}

    try:
        valor = float(nota_valor)
        if valor >= 7.0:
            classe = "text-success fw-bold"  # Azul/Verde para aprovado
        elif valor >= 5.0:
            classe = "text-warning fw-bold"  # Amarelo para recuperação
        else:
            classe = "text-danger fw-bold"  # Vermelho para reprovado

        return {"valor": f"{valor:.1f}", "classe": classe}
    except (ValueError, TypeError):
        return {"valor": "-", "classe": "text-muted"}


import json

from .models import Turma


def _get_ocupados_por_professor(professor_id, ano_letivo, turma_id_atual=None):
    """
    Retorna um conjunto (set) de strings 'DIA-HORARIO' onde o professor já tem aula.
    Adicionado 'turma_id_atual' para evitar falsos positivos na turma que está sendo editada.
    """
    ocupados = set()

    # Filtra turmas do mesmo ano
    # .exclude() garante que não vamos marcar como "ocupado" um horário da própria turma
    queryset = Turma.objects.filter(ano=ano_letivo)
    if turma_id_atual:
        queryset = queryset.exclude(id=turma_id_atual)

    # Convertemos o ID para string uma única vez para otimizar a comparação no loop
    prof_id_str = str(professor_id)

    for turma in queryset:
        if not turma.grade_horaria:
            continue

        try:
            # Garante que temos um dicionário, seja o campo JSONField ou CharField
            grade = turma.grade_horaria
            if isinstance(grade, str):
                grade = json.loads(grade)

            # Se por algum motivo o JSON não for um dicionário após o load
            if not isinstance(grade, dict):
                continue

            # Percorre a estrutura: { "dia": { "hora": { "professor_id": "..." } } }
            for dia, horarios in grade.items():
                if not isinstance(horarios, dict):
                    continue

                for hora, info in horarios.items():
                    # Verifica se info é um dicionário e se o ID bate
                    if (
                        isinstance(info, dict)
                        and str(info.get("professor_id")) == prof_id_str
                    ):
                        ocupados.add(f"{dia}-{hora}")

        except (json.JSONDecodeError, AttributeError, TypeError):
            continue

    return ocupados


def _contar_notas_lancadas(disciplina, turma):
    """
    Conta quantas notas foram lançadas para uma disciplina em uma turma específica.
    Útil para exibir o progresso de lançamento do professor.
    """
    from .models import Aluno, Nota

    # Total de alunos na turma
    total_alunos = Aluno.objects.filter(turma=turma).count()

    # Total de notas já registradas para essa disciplina e turma
    notas_existentes = Nota.objects.filter(
        disciplina=disciplina, aluno__turma=turma
    ).count()

    # Retorna um dicionário com os dados de progresso
    return {
        "total": total_alunos,
        "lancadas": notas_existentes,
        "pendentes": max(0, total_alunos - notas_existentes),
        "porcentagem": (
            round((notas_existentes / total_alunos * 100), 1) if total_alunos > 0 else 0
        ),
    }


def is_superuser(user):
    """Verifica se o usuário tem privilégios de superusuário."""
    return user.is_active and user.is_superuser


# =====================================================================
# FUNÇÕES UTILITÁRIAS (AUXILIARES)
# =====================================================================


def get_user_profile(user):
    """
    Retorna a instância de perfil (Aluno, Professor ou Gestor)
    vinculada ao usuário logado.
    """
    if hasattr(user, "aluno"):
        return user.aluno
    if hasattr(user, "professor"):
        return user.professor
    if hasattr(user, "gestor"):
        return user.gestor
    return None


def get_nome_exibicao(user):
    for tipo in ["gestor", "professor", "aluno"]:
        perfil = getattr(user, tipo, None)
        if perfil and getattr(perfil, "nome_completo", None):
            return perfil.nome_completo

    nome_auth = f"{user.first_name} {user.last_name}".strip()
    return nome_auth if nome_auth else user.email


def is_super_ou_gestor(user):
    """
    Define permissões para áreas administrativas.
    Verifica o atributo 'gestor' via hasattr para evitar exceções de RelatedObjectDoesNotExist.
    """
    return user.is_active and (user.is_superuser or hasattr(user, "gestor"))


from django.templatetags.static import static

def get_foto_perfil(user):
    """
    Retorna a URL da foto de perfil do usuário
    ou uma imagem padrão caso não exista.
    """
    for tipo in ["gestor", "professor", "aluno"]:
        perfil = getattr(user, tipo, None)
        if perfil and perfil.foto:
            return perfil.foto.url

    return static("core/img/default-user.png")


def redirect_user(user):
    """
    Lógica central de roteamento pós-login.
    Corrigido: Gestores agora são direcionados explicitamente para 'painel_gestor'.
    """
    if user.is_superuser:
        return "painel_super"
    if hasattr(user, "gestor"):
        return "painel_gestor"
    if hasattr(user, "professor"):
        return "painel_professor"
    if hasattr(user, "aluno"):
        return "painel_aluno"
    return "login"


def _get_turno_key(turno):
    """Normaliza a string do turno para busca no dicionário de constantes."""
    if not turno:
        return ""
    return turno.lower().replace("ã", "a").replace("á", "a")


# =====================================================================
# Views — Autenticação
# =====================================================================


def login_view(request):
    """
    Gerencia a autenticação de usuários.
    Inclui verificação de usuários ativos e redirecionamento dinâmico.
    """
    if request.user.is_authenticated:
        return redirect(redirect_user(request.user))

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None and user.is_active:
                login(request, user)
                return redirect(redirect_user(user))
            else:
                messages.error(request, "Esta conta está desativada.")
        else:
            # As mensagens de erro específicas (E-mail não encontrado, senha incorreta)
            # já são levantadas pelo ValidationError no LoginForm.clean()
            pass
    else:
        form = LoginForm()

    return render(request, "auth/login.html", {"form": form})


def logout_view(request):
    """Finaliza a sessão e limpa mensagens pendentes."""
    logout(request)
    messages.info(request, "Você saiu do sistema.")
    return redirect("login")


# =====================================================================
# Views — Autenticação
# =====================================================================


def login_view(request):
    """
    Realiza a autenticação do usuário.
    Se o usuário já estiver autenticado, redireciona para o painel correspondente
    evitando o acesso redundante à página de login.
    """
    if request.user.is_authenticated:
        return redirect(redirect_user(request.user))

    # Instancia o formulário com dados POST ou vazio
    form = LoginForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        if user:
            login(request, user)
            # Redireciona dinamicamente com base no perfil detectado
            return redirect(redirect_user(user))

    return render(request, "auth/login.html", {"form": form})


def logout_view(request):
    """
    Encerra a sessão do usuário e redireciona para a tela de login.
    """
    logout(request)
    return redirect("login")


# =====================================================================
# Views — Painel Principal (Gestão e Superusuário)
# =====================================================================


@login_required
@user_passes_test(is_super_ou_gestor)
def painel_super(request):
    """
    Exibe o dashboard principal para Superusuários e Gestores.
    Realiza o levantamento de métricas (professores, alunos, turmas)
    com base em um filtro de ano letivo.
    """
    ano_atual = datetime.now().year

    # Recupera anos que possuem turmas cadastradas para o filtro do Dashboard
    anos_disponiveis = list(
        Turma.objects.values_list("ano", flat=True).distinct().order_by("-ano")
    ) or [ano_atual]

    # Define o ano de filtragem baseado na query string ou ano atual
    ano_filtro, anos_disponiveis = _get_anos_filtro(
        anos_disponiveis, request.GET.get("ano"), ano_atual
    )

    # Filtra o conjunto de turmas pelo ano selecionado para basear as métricas
    turmas = Turma.objects.filter(ano=ano_filtro)

    contexto = {
        "usuario": request.user,
        "nome_exibicao": get_nome_exibicao(request.user),
        "foto_perfil_url": get_foto_perfil(request.user),
        "agora": datetime.now(),
        "calendario": gerar_calendario(),
        "anos_disponiveis": anos_disponiveis,
        "ano_filtro": ano_filtro,
        # Métricas quantitativas com tratamento de duplicidade via distinct()
        "total_professores": (
            Professor.objects.filter(disciplinas__turma__in=turmas).distinct().count()
        ),
        "total_alunos": Aluno.objects.filter(turma__in=turmas).distinct().count(),
        "total_turmas": turmas.count(),
        "total_disciplinas": (
            Disciplina.objects.filter(turma__in=turmas).distinct().count()
        ),
    }

    return render(request, "superusuario/painel_super.html", contexto)


def gerar_calendario(ano=None, mes=None):
    """
    Gera uma estrutura de semanas e dias para exibição no template.
    Retorna um dicionário com os dados do mês.
    """
    hoje = datetime.now()
    ano = int(ano) if ano else hoje.year
    mes = int(mes) if mes else hoje.month

    # Define o primeiro dia da semana como Domingo (6) ou Segunda (0)
    # Geralmente calendários escolares usam Domingo como início:
    cal = calendar.Calendar(firstweekday=6)

    # monthdayscalendar retorna uma lista de semanas,
    # cada semana é uma lista de 7 números (0 para dias fora do mês)
    semanas = cal.monthdayscalendar(ano, mes)

    # Nomes dos meses em português (opcional, se o locale não estiver setado)
    meses_pt = [
        "",
        "Janeiro",
        "Fevereiro",
        "Março",
        "Abril",
        "Maio",
        "Junho",
        "Julho",
        "Agosto",
        "Setembro",
        "Outubro",
        "Novembro",
        "Dezembro",
    ]

    return {
        "semanas": semanas,
        "mes_nome": meses_pt[mes],
        "ano": ano,
        "mes": mes,
        "hoje": hoje.day if ano == hoje.year and mes == hoje.month else None,
    }


def _get_anos_filtro(anos_disponiveis, ano_selecionado, ano_atual):
    """
    Auxiliar para processar a lógica de seleção de ano nos filtros.
    Retorna o ano que deve ser filtrado e a lista de anos para o template.
    """
    # Se o usuário escolheu um ano no select, usa ele. Caso contrário, usa o ano atual.
    try:
        ano_filtro = int(ano_selecionado) if ano_selecionado else ano_atual
    except (ValueError, TypeError):
        ano_filtro = ano_atual

    # Garante que o ano atual ou o selecionado estejam na lista de opções do Select
    lista_anos = list(anos_disponiveis)
    if ano_atual not in lista_anos:
        lista_anos.append(ano_atual)
    if ano_filtro not in lista_anos:
        lista_anos.append(ano_filtro)

    # Ordena do mais recente para o mais antigo
    lista_anos.sort(reverse=True)

    return ano_filtro, lista_anos


# =====================================================================
# Views — Usuários
# =====================================================================


@login_required
def usuarios(request):
    """
    Controla o acesso à listagem geral de usuários do sistema.
    Define permissões granulares: Gestores com cargos de diretoria possuem
    privilégios de visualização estendidos.
    """
    # Verifica se o usuário é superusuário ou gestor de alto nível (diretor/vice)
    pode_ver_gestores = request.user.is_superuser or (
        hasattr(request.user, "gestor")
        and request.user.gestor.cargo in ("diretor", "vice_diretor")
    )

    return render(
        request,
        "core/usuarios.html",
        {
            "pode_ver_gestores": pode_ver_gestores,
            "nome_exibicao": get_nome_exibicao(request.user),
            "foto_perfil_url": get_foto_perfil(request.user),
        },
    )


# =====================================================================
# Views — Perfil do Usuário
# =====================================================================


@login_required
def editar_perfil(request):
    """
    Gerencia a atualização de dados do próprio usuário, incluindo senha e foto.
    Implementa a persistência dupla: objeto User (auth) e objeto Perfil (core).
    """
    user = request.user
    perfil = get_user_profile(user)

    # Inicializa o formulário com dados POST e FILES para processamento de imagem
    form = EditarPerfilForm(request.POST or None, request.FILES or None, instance=user)

    if request.method == "POST":
        if form.is_valid():
            # Salva os dados básicos do usuário (E-mail, etc)
            user = form.save(commit=False)

            # Tratamento de troca de senha voluntária
            nova_senha = form.cleaned_data.get("nova_senha")
            if nova_senha:
                user.set_password(nova_senha)
                # Atualiza o hash da sessão para não deslogar o usuário após trocar a senha
                update_session_auth_hash(request, user)

            user.save()

            # Processamento da foto de perfil vinculado ao modelo específico (Aluno/Professor/Gestor)
            foto = request.FILES.get("foto")
            if perfil and foto:
                perfil.foto = foto
                perfil.save()

            messages.success(request, "Perfil atualizado com sucesso!")
            return redirect(redirect_user(user))
        else:
            messages.error(
                request, "Erro ao atualizar perfil. Verifique os campos abaixo."
            )

    # Recuperação de metadados para exibição no template
    foto_atual = perfil.foto.url if perfil and getattr(perfil, "foto", None) else None

    return render(
        request,
        "core/editar_perfil.html",
        {
            "form": form,
            "perfil": perfil,
            "foto_atual": foto_atual,
            "foto_perfil_url": get_foto_perfil(user),
            "nome_exibicao": get_nome_exibicao(user),
        },
    )


@login_required
def remover_foto_perfil(request):
    """
    Remove fisicamente o arquivo de imagem associado ao perfil e limpa o campo no banco.
    """
    perfil = get_user_profile(request.user)

    if not perfil:
        messages.error(request, "Nenhum perfil associado ao usuário.")
        return redirect("editar_perfil")

    if getattr(perfil, "foto", None):
        # Exclui o arquivo do armazenamento antes de limpar a referência no banco
        perfil.foto.delete(save=False)
        perfil.foto = None
        perfil.save()
        messages.success(request, "Foto removida com sucesso!")
    else:
        messages.info(request, "Você não possui uma foto de perfil cadastrada.")

    return redirect("editar_perfil")


# =====================================================================
# Views — Professores
# =====================================================================


@login_required
@user_passes_test(is_super_ou_gestor)
def listar_professores(request):
    """
    Lista os professores cadastrados com suporte a busca por nome.
    Utiliza select_related para otimizar a performance da consulta ao banco.
    """
    query = request.GET.get("q", "")
    # Otimização: select_related('user') reduz o número de queries ao buscar dados do login
    professores = Professor.objects.all().select_related("user")

    if query:
        professores = professores.filter(nome_completo__icontains=query)

    return render(
        request,
        "professor/listar_professores.html",
        {
            "professores": professores,
            "query": query,
            "nome_exibicao": get_nome_exibicao(request.user),
            "foto_perfil_url": get_foto_perfil(request.user),
        },
    )


@login_required
@user_passes_test(is_super_ou_gestor)
def cadastrar_professor(request):
    """
    Processa a criação de um novo professor e seu respectivo usuário.
    Implementa a exibição detalhada de erros de validação via messages.
    """
    if request.method == "POST":
        # Passa request.FILES para suportar o upload da foto e o request para lógica interna do form
        form = ProfessorForm(request.POST, request.FILES, request=request)
        if form.is_valid():
            professor = form.save()
            messages.success(
                request,
                f"Professor(a) {professor.nome_completo} cadastrado(a) com sucesso!",
            )
            return redirect("listar_professores")

        # Tratamento formal de erros de validação para feedback ao usuário
        for field, erros in form.errors.items():
            label = form.fields[field].label if field in form.fields else field
            for erro in erros:
                messages.error(request, f"{label}: {erro}")
    else:
        form = ProfessorForm(request=request)

    return render(
        request,
        "professor/cadastrar_professor.html",
        {
            "form": form,
            "professor": None,
            "nome_exibicao": get_nome_exibicao(request.user),
            "foto_perfil_url": get_foto_perfil(request.user),
        },
    )


@login_required
@user_passes_test(is_super_ou_gestor)
def editar_professor(request, professor_id):
    """
    Atualiza os dados de um professor existente.
    Mantém a integridade entre o formulário e a instância do modelo.
    """
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
        {
            "form": form,
            "professor": professor,
            "nome_exibicao": get_nome_exibicao(request.user),
            "foto_perfil_url": get_foto_perfil(request.user),
        },
    )


@login_required
@user_passes_test(is_super_ou_gestor)
def excluir_professor(request, professor_id):
    """
    Remove o professor do sistema.
    A exclusão é realizada através do objeto User para garantir que o acesso
    também seja revogado, aproveitando o on_delete=models.CASCADE.
    """
    professor = get_object_or_404(Professor, id=professor_id)

    # É recomendável realizar exclusões apenas via método POST para segurança,
    # mas mantendo sua lógica atual com uma verificação adicional:
    try:
        nome = professor.nome_completo
        # Deletar o User remove o Professor automaticamente via CASCADE no banco de dados
        professor.user.delete()
        messages.success(request, f"Professor(a) {nome} removido(a) com sucesso.")
    except Exception as e:
        messages.error(request, f"Erro ao remover professor: {str(e)}")

    return redirect("listar_professores")


# =====================================================================
# Views — Gestores
# =====================================================================


@login_required
@user_passes_test(is_superuser)
def cadastrar_editar_gestor(request, gestor_id=None):
    """
    View unificada para criação e atualização de perfis de Gestão.
    Restrita exclusivamente a Superusuários.
    """
    gestor = get_object_or_404(Gestor, id=gestor_id) if gestor_id else None

    if request.method == "POST":
        # Processamento de formulário com suporte a arquivos (foto) e instância existente
        form = GestorForm(request.POST, request.FILES, instance=gestor, request=request)
        if form.is_valid():
            gestor_obj = form.save()
            acao = "atualizado" if gestor_id else "cadastrado"

            # Utiliza get_cargo_display() para exibir o nome amigável do ChoiceField
            messages.success(
                request,
                f"{gestor_obj.get_cargo_display()} {gestor_obj.nome_completo} {acao} com sucesso!",
            )
            return redirect("listar_gestores")

        # Captura de erros de validação para feedback via Django Messages
        for field, erros in form.errors.items():
            label = form.fields[field].label if field in form.fields else field
            for erro in erros:
                messages.error(request, f"{label}: {erro}")
    else:
        # Preenchimento inicial do e-mail caso seja uma edição
        initial = {"email": gestor.user.email} if gestor and gestor.user else {}
        form = GestorForm(instance=gestor, initial=initial, request=request)

    return render(
        request,
        "gestor/cadastrar_gestor.html",
        {
            "form": form,
            "gestor": gestor,
            "nome_exibicao": get_nome_exibicao(request.user),
            "foto_perfil_url": get_foto_perfil(request.user),
        },
    )


@login_required
@user_passes_test(is_superuser)
def listar_gestores(request):
    """
    Lista todos os gestores cadastrados.
    Implementa busca por nome e otimização de banco de dados via select_related.
    """
    query = request.GET.get("q", "")
    # Otimiza a consulta trazendo os dados do User associado em um único JOIN
    gestores = Gestor.objects.select_related("user").all()

    if query:
        gestores = gestores.filter(nome_completo__icontains=query)

    return render(
        request,
        "gestor/listar_gestores.html",
        {
            "gestores": gestores,
            "query": query,
            "nome_exibicao": get_nome_exibicao(request.user),
            "foto_perfil_url": get_foto_perfil(request.user),
        },
    )


@login_required
@user_passes_test(is_superuser)
def excluir_gestor(request, gestor_id):
    """
    Remove o gestor e seu respectivo acesso (User) ao sistema.
    """
    gestor = get_object_or_404(Gestor, id=gestor_id)

    try:
        if gestor.user:
            # A exclusão do User aciona o CASCADE para o perfil Gestor
            gestor.user.delete()
        else:
            gestor.delete()
        messages.success(request, "Gestor removido com sucesso.")
    except Exception as e:
        messages.error(request, f"Erro ao remover gestor: {str(e)}")

    return redirect("listar_gestores")


# =====================================================================
# Views — Alunos
# =====================================================================


@login_required
@user_passes_test(is_super_ou_gestor)
def listar_alunos(request):
    """
    Exibe a listagem de alunos cadastrados.
    Utiliza select_related para carregar o User e a Turma em uma única consulta,
    evitando múltiplas idas ao banco de dados durante a renderização da lista.
    """
    query = request.GET.get("q", "")
    # Otimização: select_related('user', 'turma') é essencial pela relação ForeignKey/OneToOne
    alunos = Aluno.objects.all().select_related("user", "turma")

    if query:
        alunos = alunos.filter(nome_completo__icontains=query)

    return render(
        request,
        "aluno/listar_alunos.html",
        {
            "alunos": alunos,
            "query": query,
            "nome_exibicao": get_nome_exibicao(request.user),
            "foto_perfil_url": get_foto_perfil(request.user),
        },
    )


@login_required
@user_passes_test(is_super_ou_gestor)
def cadastrar_aluno(request):
    """
    Realiza a matrícula de um novo aluno.
    Garante que erros de validação (como CPF duplicado) sejam reportados via messages.
    """
    if request.method == "POST":
        # Passagem de request.FILES é obrigatória para salvar a foto do aluno
        form = AlunoForm(request.POST, request.FILES, request=request)
        if form.is_valid():
            aluno = form.save()
            messages.success(
                request,
                f"Aluno(a) {aluno.nome_completo} cadastrado(a) com sucesso!",
            )
            return redirect("listar_alunos")

        # Tratamento formal de erros do formulário
        for field, erros in form.errors.items():
            label = form.fields[field].label if field in form.fields else field
            for erro in erros:
                messages.error(request, f"{label}: {erro}")
    else:
        form = AlunoForm(request=request)

    return render(
        request,
        "aluno/cadastrar_aluno.html",
        {
            "form": form,
            "aluno": None,
            "nome_exibicao": get_nome_exibicao(request.user),
            "foto_perfil_url": get_foto_perfil(request.user),
        },
    )


@login_required
@user_passes_test(is_super_ou_gestor)
def editar_aluno(request, aluno_id):
    """
    Edita o prontuário de um aluno existente.
    A instância é passada ao form para garantir que o Django realize um UPDATE.
    """
    aluno = get_object_or_404(Aluno, id=aluno_id)

    if request.method == "POST":
        form = AlunoForm(request.POST, request.FILES, instance=aluno, request=request)
        if form.is_valid():
            aluno_obj = form.save()
            messages.success(
                request,
                f"Aluno(a) {aluno_obj.nome_completo} atualizado(a) com sucesso!",
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
        {
            "form": form,
            "aluno": aluno,
            "nome_exibicao": get_nome_exibicao(request.user),
            "foto_perfil_url": get_foto_perfil(request.user),
        },
    )


@login_required
@user_passes_test(is_super_ou_gestor)
def excluir_aluno(request, aluno_id):
    """
    Remove o registro do aluno.
    A exclusão via aluno.user.delete() garante que tanto o perfil quanto as
    credenciais de acesso sejam removidas simultaneamente (CASCADE).
    """
    aluno = get_object_or_404(Aluno, id=aluno_id)

    try:
        nome = aluno.nome_completo
        # A deleção do User é a forma mais limpa de encerrar o vínculo
        if aluno.user:
            aluno.user.delete()
        else:
            aluno.delete()
        messages.success(request, f"Aluno(a) {nome} removido(a) com sucesso.")
    except Exception as e:
        messages.error(request, f"Erro ao remover aluno: {str(e)}")

    return redirect("listar_alunos")


# =====================================================================
# Views — Turmas
# =====================================================================
# =====================================================================
# Views — Turmas
# =====================================================================


@login_required
@user_passes_test(is_super_ou_gestor)
def listar_turmas(request):
    """
    Lista as turmas cadastradas com filtragem por ano letivo e busca por nome.
    Utiliza a lógica de anos_disponiveis para facilitar a navegação histórica.
    """
    ano_atual = timezone.localtime(timezone.now()).year
    query = request.GET.get("q", "").strip()

    # Recupera a lista de anos que possuem turmas para o componente de filtro
    anos_disponiveis = list(
        Turma.objects.values_list("ano", flat=True).distinct().order_by("-ano")
    ) or [ano_atual]

    # Aplica a lógica auxiliar para determinar qual ano está sendo visualizado
    ano_filtro, anos_disponiveis = _get_anos_filtro(
        anos_disponiveis, request.GET.get("ano"), ano_atual
    )

    # Filtra as turmas pelo ano e pela query de busca, se houver
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
            "nome_exibicao": get_nome_exibicao(request.user),
            "foto_perfil_url": get_foto_perfil(request.user),
        },
    )


@login_required
@user_passes_test(is_super_ou_gestor)
def cadastrar_turma(request):
    """
    Gerencia a criação de novas turmas.
    Implementa validação manual de regras de negócio para garantir unicidade por ano.
    """
    erro = None
    ano_atual = datetime.now().year
    # Define o range de anos para o seletor do template (limite de 1 ano à frente)
    anos = list(range(2010, ano_atual + 2))

    if request.method == "POST":
        nome = request.POST.get("nome")
        turno = request.POST.get("turno")
        ano_str = request.POST.get("ano")

        try:
            ano = int(ano_str)
            # Validação de integridade do ano letivo
            if ano < 2010 or ano > ano_atual + 1:
                erro = "O ano letivo deve estar entre 2010 e o próximo ano."
            # Validação de duplicidade (Nome + Ano)
            elif Turma.objects.filter(nome=nome, ano=ano).exists():
                erro = f"A turma '{nome}' já existe no ano letivo de {ano}."
            else:
                Turma.objects.create(nome=nome, turno=turno, ano=ano)
                messages.success(request, f"Turma {nome} criada com sucesso!")
                return redirect("listar_turmas")
        except (TypeError, ValueError):
            erro = "Ano letivo informado é inválido."

    return render(
        request,
        "turma/cadastrar_turma.html",
        {
            "erro": erro,
            "anos": anos,
            "nome_exibicao": get_nome_exibicao(request.user),
            "foto_perfil_url": get_foto_perfil(request.user),
        },
    )


@login_required
@user_passes_test(is_super_ou_gestor)
def editar_turma(request, turma_id):
    """
    Atualiza os dados de uma turma existente.
    Verifica se a alteração de nome/ano não gera conflito com turmas existentes.
    """
    turma = get_object_or_404(Turma, id=turma_id)
    erro = None
    ano_atual = datetime.now().year
    anos = list(range(2010, ano_atual + 2))

    if request.method == "POST":
        nome = request.POST.get("nome")
        turno = request.POST.get("turno")
        ano = request.POST.get("ano")

        # Verifica duplicidade excluindo a própria instância que está sendo editada
        if Turma.objects.filter(nome=nome, ano=ano).exclude(id=turma.id).exists():
            erro = "Já existe outra turma com esse nome cadastrada para este ano."
        else:
            turma.nome = nome
            turma.turno = turno
            turma.ano = ano
            turma.save()
            messages.success(request, "Dados da turma atualizados com sucesso.")
            return redirect("listar_turmas")

    return render(
        request,
        "turma/cadastrar_turma.html",
        {
            "turma": turma,
            "erro": erro,
            "anos": anos,
            "nome_exibicao": get_nome_exibicao(request.user),
            "foto_perfil_url": get_foto_perfil(request.user),
        },
    )


@login_required
@user_passes_test(
    lambda u: u.is_superuser
    or (hasattr(u, "gestor") and u.gestor.cargo != "secretario")
)
def excluir_turma(request, turma_id):
    """
    Exclui permanentemente uma turma.
    Restringe a ação para evitar que secretários removam turmas acidentalmente.
    """
    turma = get_object_or_404(Turma, id=turma_id)
    try:
        nome_turma = turma.nome
        turma.delete()
        messages.success(request, f"Turma {nome_turma} excluída com sucesso!")
    except Exception as e:
        messages.error(request, f"Não foi possível excluir a turma: {str(e)}")

    return redirect("listar_turmas")


# =====================================================================
# Views — Disciplinas
# =====================================================================


@login_required
def visualizar_disciplinas(request, disciplina_id):
    """
    Exibe os detalhes de uma disciplina, incluindo a lista de alunos e suas notas.
    Acesso permitido para: Superusuários, Gestores e o Professor da disciplina.
    """
    disciplina = get_object_or_404(Disciplina, id=disciplina_id)

    # Validação de permissão específica
    eh_professor_da_disc = (
        hasattr(request.user, "professor")
        and disciplina.professor == request.user.professor
    )

    if not (is_super_ou_gestor(request.user) or eh_professor_da_disc):
        messages.error(
            request, "Você não tem permissão para visualizar esta disciplina."
        )
        return redirect("dashboard")

    turma = disciplina.turma
    # Otimização: Busca alunos da turma e notas já vinculadas à disciplina
    alunos = (
        Aluno.objects.filter(turma=turma)
        .select_related("user")
        .order_by("nome_completo")
    )
    notas = Nota.objects.filter(disciplina=disciplina).select_related("aluno")

    # Dicionário para facilitar a busca de notas por aluno no template
    notas_dict = {nota.aluno.id: nota for nota in notas}

    return render(
        request,
        "disciplina/visualizar_disciplinas.html",
        {
            "disciplina": disciplina,
            "turma": turma,
            "alunos": alunos,
            "notas_dict": notas_dict,
            "nome_exibicao": get_nome_exibicao(request.user),
            "foto_perfil_url": get_foto_perfil(request.user),
            "is_gestor_ou_super": is_super_ou_gestor(request.user),
        },
    )


@login_required
@user_passes_test(is_super_ou_gestor)
def cadastrar_disciplina_para_turma(request, turma_id):
    """
    Vincula uma nova disciplina a uma turma específica.
    """
    turma = get_object_or_404(Turma, id=turma_id)

    if request.method == "POST":
        nome = request.POST.get("nome")
        professor_id = request.POST.get("professor")

        if not nome or not professor_id:
            messages.error(request, "Preencha todos os campos obrigatórios.")
        else:
            professor = get_object_or_404(Professor, id=professor_id)
            if Disciplina.objects.filter(nome=nome, turma=turma).exists():
                messages.error(request, f"A disciplina '{nome}' já existe nesta turma.")
            else:
                Disciplina.objects.create(nome=nome, professor=professor, turma=turma)
                messages.success(
                    request, f"Disciplina '{nome}' cadastrada com sucesso!"
                )
                return redirect("listar_disciplinas_turma", turma_id=turma.id)

    # Lista apenas professores (excluindo superusuários que não lecionam)
    professores = Professor.objects.all().select_related("user")
    return render(
        request,
        "disciplina/cadastrar_disciplina_turma.html",
        {
            "turma": turma,
            "professores": professores,
            "nome_exibicao": get_nome_exibicao(request.user),
            "foto_perfil_url": get_foto_perfil(request.user),
        },
    )


@login_required
@user_passes_test(is_super_ou_gestor)
def editar_disciplina(request, disciplina_id):
    """
    Edita os dados básicos de uma disciplina (nome ou professor responsável).
    """
    disciplina = get_object_or_404(Disciplina, id=disciplina_id)
    professores = Professor.objects.all().select_related("user")

    if request.method == "POST":
        nome = request.POST.get("nome")
        professor_id = request.POST.get("professor")

        professor_novo = get_object_or_404(Professor, id=professor_id)

        disciplina.nome = nome
        disciplina.professor = professor_novo
        disciplina.save()

        messages.success(request, "Disciplina atualizada com sucesso!")
        return redirect("listar_disciplinas_turma", turma_id=disciplina.turma.id)

    return render(
        request,
        "disciplina/cadastrar_disciplina_turma.html",
        {
            "disciplina": disciplina,
            "turma": disciplina.turma,
            "professores": professores,
            "nome_exibicao": get_nome_exibicao(request.user),
            "foto_perfil_url": get_foto_perfil(request.user),
        },
    )


@login_required
@user_passes_test(is_super_ou_gestor)
def listar_disciplinas_turma(request, turma_id):
    """
    Visão do Gestor: Lista todas as disciplinas de uma turma para fins administrativos.
    """
    turma = get_object_or_404(Turma, id=turma_id)
    query = request.GET.get("q", "")
    disciplinas = Disciplina.objects.filter(turma=turma).select_related(
        "professor__user"
    )

    if query:
        disciplinas = disciplinas.filter(nome__icontains=query)

    return render(
        request,
        "disciplina/listar_disciplinas_turma.html",
        {
            "turma": turma,
            "disciplinas": disciplinas,
            "query": query,
            "nome_exibicao": get_nome_exibicao(request.user),
            "foto_perfil_url": get_foto_perfil(request.user),
        },
    )


from decimal import Decimal

from django.db.models import Avg, DecimalField, ExpressionWrapper, F
from django.db.models.functions import Coalesce


def _calcular_detalhes_disciplina(disciplina, turma):
    """
    Calcula estatísticas tratando o erro de tipos mistos (Decimal vs Float).
    """
    from .models import Aluno, Frequencia, Nota

    total_alunos = Aluno.objects.filter(turma=turma).count()

    # Criamos a expressão da média definindo explicitamente que o resultado é Decimal
    # Usamos Decimal('0.0') no Coalesce para manter a consistência
    expressao_media = ExpressionWrapper(
        (
            Coalesce(F("nota1"), Decimal("0.0"))
            + Coalesce(F("nota2"), Decimal("0.0"))
            + Coalesce(F("nota3"), Decimal("0.0"))
            + Coalesce(F("nota4"), Decimal("0.0"))
        )
        / 4,
        output_field=DecimalField(),
    )

    resultado_nota = Nota.objects.filter(
        disciplina=disciplina, aluno__turma=turma
    ).aggregate(media_turma=Avg(expressao_media))

    media_geral = resultado_nota["media_turma"] or 0

    # Cálculo de frequência
    frequencias = Frequencia.objects.filter(disciplina=disciplina, aluno__turma=turma)
    total_registros = frequencias.count()
    total_presentes = frequencias.filter(presente=True).count()

    frequencia_geral = (
        (total_presentes / total_registros * 100) if total_registros > 0 else 100
    )

    return {
        "disciplina": disciplina,
        "total_alunos": total_alunos,
        "media_geral": round(float(media_geral), 1),
        "frequencia_geral": round(frequencia_geral, 1),
        "status_turma": "Bom" if media_geral >= 7 else "Atenção",
    }


@login_required
def disciplinas_turma(request, turma_id):
    """
    Visão Híbrida: Mostra as disciplinas de uma turma com dados analíticos.
    """
    user = request.user
    turma = get_object_or_404(Turma, id=turma_id)

    # Filtragem por perfil (Professor vê apenas as dele, Gestor vê todas)
    if hasattr(user, "professor"):
        disciplinas_qs = Disciplina.objects.filter(
            turma=turma, professor=user.professor
        )
    elif user.is_superuser or hasattr(user, "gestor"):
        disciplinas_qs = Disciplina.objects.filter(turma=turma)
    else:
        return redirect("login")

    disciplinas_qs = disciplinas_qs.order_by("nome")

    if not disciplinas_qs.exists():
        messages.warning(request, "Nenhuma disciplina encontrada nesta turma.")
        return redirect("listar_turmas")

    # Gerar a lista de dicionários com os cálculos
    disciplinas_detalhadas = [
        _calcular_detalhes_disciplina(d, turma) for d in disciplinas_qs
    ]

    # Renderização da página (fora da função auxiliar)
    return render(
        request,
        "professor/disciplinas_turma.html",
        {
            "turma": turma,
            "disciplinas_detalhadas": disciplinas_detalhadas,
            "is_gestor_ou_super": user.is_superuser or hasattr(user, "gestor"),
            # Adicione aqui outras funções de contexto se necessário, como fotos ou nomes
        },
    )


@login_required
@user_passes_test(is_super_ou_gestor)
def excluir_disciplina(request, disciplina_id):
    """
    Remove uma disciplina da grade da turma.
    """
    disciplina = get_object_or_404(Disciplina, id=disciplina_id)
    turma_id = disciplina.turma.id
    nome_disc = disciplina.nome

    disciplina.delete()
    messages.success(request, f"Disciplina '{nome_disc}' excluída com sucesso!")
    return redirect("listar_disciplinas_turma", turma_id=turma_id)


# =====================================================================
# FUNÇÕES AUXILIARES DO PAINEL (Devem vir ANTES da view principal)
# =====================================================================


def _get_ano_filtro_professor(request, anos_disponiveis, ano_atual):
    """
    Gerencia a persistência do filtro de ano letivo na sessão do usuário.
    """
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
        # Garante que o ano atual ou o filtrado esteja na lista para não quebrar o select
        anos_disponiveis = sorted(
            list(set(anos_disponiveis + [ano_filtro])), reverse=True
        )
    return ano_filtro, anos_disponiveis


def _contar_notas_lancadas(disciplina, turma):
    """
    Conta o total de avaliações (bimestres) já preenchidas para uma disciplina.
    """
    from django.db.models import Count

    from .models import Nota

    notas_qs = Nota.objects.filter(disciplina=disciplina, aluno__turma=turma)
    contagem = notas_qs.aggregate(
        n1=Count("nota1"), n2=Count("nota2"), n3=Count("nota3"), n4=Count("nota4")
    )
    return (
        (contagem["n1"] or 0)
        + (contagem["n2"] or 0)
        + (contagem["n3"] or 0)
        + (contagem["n4"] or 0)
    )


def _acumular_notas_professor(disciplinas_filtradas):
    """
    Calcula métricas de desempenho e preenchimento de notas.
    """
    total_notas_possiveis = 0
    total_notas_lancadas = 0
    alunos_ids = set()
    disciplinas_detalhadas = []

    for disciplina in disciplinas_filtradas:
        turma = disciplina.turma
        from .models import Aluno

        alunos_da_turma = Aluno.objects.filter(turma=turma).values_list("id", flat=True)
        alunos_count = alunos_da_turma.count()
        alunos_ids.update(alunos_da_turma)

        notas_possiveis_disc = alunos_count * 4
        notas_lancadas_disc = _contar_notas_lancadas(disciplina, turma)

        total_notas_possiveis += notas_possiveis_disc
        total_notas_lancadas += notas_lancadas_disc

        percentual = (
            int((notas_lancadas_disc / notas_possiveis_disc * 100))
            if notas_possiveis_disc > 0
            else 0
        )

        disciplinas_detalhadas.append(
            {
                "disciplina": disciplina,
                "alunos_count": alunos_count,
                "notas_lancadas": notas_lancadas_disc,
                "notas_possiveis": notas_possiveis_disc,
                "percentual": percentual,
            }
        )

    return (
        total_notas_possiveis,
        total_notas_lancadas,
        len(alunos_ids),
        disciplinas_detalhadas,
    )


# =====================================================================
# VIEW PRINCIPAL (PAINEL DO PROFESSOR)
# =====================================================================


@login_required
def painel_professor(request):
    if not hasattr(request.user, "professor"):
        messages.error(request, "Acesso restrito a professores.")
        return redirect("login")

    professor = request.user.professor
    ano_atual = timezone.now().year

    # 1. Buscar anos disponíveis
    anos_disponiveis = list(
        Turma.objects.filter(disciplinas__professor=professor)
        .values_list("ano", flat=True)
        .distinct()
        .order_by("-ano")
    ) or [ano_atual]

    # 2. Chamar a função de filtro (AGORA DEFINIDA ACIMA)
    ano_filtro, anos_disponiveis = _get_ano_filtro_professor(
        request, anos_disponiveis, ano_atual
    )

    # 3. Filtrar disciplinas
    disciplinas_filtradas = Disciplina.objects.filter(
        professor=professor, turma__ano=ano_filtro
    ).select_related("turma")

    # 4. Acumular métricas
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
            "anos_disponiveis": anos_disponiveis,
            "ano_filtro": ano_filtro,
            "agora": timezone.now(),
        },
    )


@login_required
def disciplinas_professor(request):
    """
    Lista as turmas do professor, permitindo filtrar por ano e buscar por nome.
    """
    if not hasattr(request.user, "professor"):
        return redirect("login")

    professor = request.user.professor
    ano_atual = timezone.now().year

    # IDs das turmas onde este professor leciona
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

    # Agregação de dados para exibição nos cards de turma
    turmas_detalhadas = []
    for turma in turmas:
        turmas_detalhadas.append(
            {
                "turma": turma,
                "disciplinas_count": Disciplina.objects.filter(
                    turma=turma, professor=professor
                ).count(),
                "alunos_count": Aluno.objects.filter(turma=turma).count(),
                "turno_display": turma.get_turno_display(),
            }
        )

    return render(
        request,
        "professor/disciplinas_professor.html",
        {
            "turmas_detalhadas": turmas_detalhadas,
            "nome_exibicao": get_nome_exibicao(request.user),
            "foto_perfil_url": get_foto_perfil(request.user),
            "query": query,
            "anos_disponiveis": anos_disponiveis,
            "ano_filtro": ano_filtro,
        },
    )


@login_required
def visualizar_grade_professor(request, turma_id):
    """
    Exibe a grade horária de uma turma específica, focando nas aulas do professor.
    """
    if not hasattr(request.user, "professor"):
        return redirect("login")

    professor = request.user.professor
    turma = get_object_or_404(Turma, id=turma_id)
    disciplinas_prof = Disciplina.objects.filter(turma=turma, professor=professor)

    if not disciplinas_prof.exists():
        messages.error(request, "Você não possui disciplinas vinculadas a esta turma.")
        return redirect("disciplinas_professor")

    return render(
        request,
        "professor/visualizar_grade_professor.html",
        {
            "turma": turma,
            "grade_horario": _get_grade_formatada(turma),  # Função definida no Bloco 2
            "disciplinas_professor": disciplinas_prof,
            "nome_exibicao": get_nome_exibicao(request.user),
            "foto_perfil_url": get_foto_perfil(request.user),
        },
    )


# =====================================================================
# Views — Lançamento de Notas
# =====================================================================


@login_required
def lancar_nota(request, disciplina_id):
    """
    Realiza o lançamento de notas bimestrais (1º ao 4º bimestre).
    Cada par (aluno, disciplina) possui uma única instância do modelo Nota.
    """
    disciplina = get_object_or_404(Disciplina, id=disciplina_id)
    user = request.user

    # Validação de Segurança: Apenas Gestores/Super ou o próprio Professor da matéria
    eh_professor_da_disc = (
        hasattr(user, "professor") and disciplina.professor == user.professor
    )
    if not (is_super_ou_gestor(user) or eh_professor_da_disc):
        messages.error(
            request, "Você não tem permissão para lançar notas nesta disciplina."
        )
        return redirect("dashboard")

    # Busca alunos da turma ordenados para manter a consistência da tabela no template
    alunos = (
        Aluno.objects.filter(turma_id=disciplina.turma_id)
        .select_related("user")
        .order_by("nome_completo")
    )

    if request.method == "POST":
        houve_erro = False
        for aluno in alunos:
            # get_or_create garante que a linha de nota exista antes da atribuição
            nota_obj, _ = Nota.objects.get_or_create(
                aluno_id=aluno.pk, disciplina_id=disciplina.id
            )

            # Itera sobre os 4 bimestres
            for i in range(1, 5):
                campo = f"nota{i}_{aluno.pk}"
                valor = request.POST.get(campo, "").strip()

                if valor == "":
                    # Permite deixar o campo vazio no banco (null/None) se não houver nota
                    setattr(nota_obj, f"nota{i}", None)
                    continue

                try:
                    # Converte formato BR (vírgula) para Float padrão
                    valor_float = float(valor.replace(",", "."))

                    if not (0 <= valor_float <= 10):
                        raise ValueError("A nota deve estar entre 0 e 10.")

                    setattr(nota_obj, f"nota{i}", valor_float)

                except ValueError:
                    messages.error(
                        request,
                        f"Valor inválido '{valor}' para {aluno.nome_completo} no {i}º Bimestre.",
                    )
                    houve_erro = True

            # Salva o objeto após processar os 4 bimestres do aluno
            nota_obj.save()

        if not houve_erro:
            messages.success(request, "Notas processadas e salvas com sucesso!")
        else:
            messages.warning(
                request,
                "Algumas notas foram salvas, mas houve erros em valores específicos.",
            )

        return redirect("lancar_nota", disciplina_id=disciplina.id)

    # Prepara dicionário de notas existentes para preencher os inputs do template
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
            "is_gestor_ou_super": is_super_ou_gestor(user),
            "nome_exibicao": get_nome_exibicao(user),
            "foto_perfil_url": get_foto_perfil(user),
        },
    )


# =====================================================================
# Funções Auxiliares — Painel do Aluno
# =====================================================================


def _calcular_situacao_aluno(disciplinas_com_notas, total_lancadas, total_possiveis):
    """
    Define a situação acadêmica do aluno com base nas médias e preenchimento.
    """
    if total_possiveis == 0:
        return "Sem Dados", "info"

    progresso = (total_lancadas / total_possiveis) * 100

    # Cálculo de médias válidas
    medias = [
        d["nota"].media
        for d in disciplinas_com_notas
        if d["nota"] and d["nota"].media is not None
    ]

    if not medias:
        return "Cursando", "warning"

    media_final = sum(medias) / len(medias)

    if media_final >= 7:
        return "Aprovado", "success"
    elif media_final >= 5:
        return "Recuperação", "warning"
    else:
        return "Reprovado", "danger"


def _coletar_notas_aluno(aluno, disciplinas):
    """
    Agrega notas e estatísticas de frequência para o perfil do aluno.
    """
    from django.db.models import Count, Q

    from .models import Frequencia, Nota

    disciplinas_com_notas = []
    soma_medias = 0
    total_com_media = 0
    total_lancadas = 0

    # Busca todas as notas do aluno de uma vez
    notas_aluno = {n.disciplina_id: n for n in Nota.objects.filter(aluno=aluno)}

    # Busca frequências agregadas
    frequencias_agregadas = (
        Frequencia.objects.filter(aluno=aluno)
        .values("disciplina_id")
        .annotate(total=Count("id"), presencas=Count("id", filter=Q(presente=True)))
    )
    freq_dict = {f["disciplina_id"]: f for f in frequencias_agregadas}

    for disciplina in disciplinas:
        nota = notas_aluno.get(disciplina.id)

        # CORREÇÃO: Passando disciplina e turma para a contagem
        # Usamos a função global definida anteriormente
        total_lancadas += _contar_notas_lancadas(disciplina, aluno.turma)

        # Dados de Frequência
        dados_freq = freq_dict.get(disciplina.id, {"total": 0, "presencas": 0})
        total_aulas = dados_freq["total"]
        presencas = dados_freq["presencas"]
        faltas = total_aulas - presencas

        percentual_faltas = (
            round((faltas / total_aulas * 100), 1) if total_aulas > 0 else 0
        )

        disciplinas_com_notas.append(
            {
                "disciplina": disciplina,
                "nota": nota,
                "total_aulas": total_aulas,
                "presencas": presencas,
                "faltas": faltas,
                "percentual_faltas": percentual_faltas,
            }
        )

        if nota and nota.media is not None:
            soma_medias += float(nota.media)
            total_com_media += 1

    media_geral = soma_medias / total_com_media if total_com_media > 0 else None
    return disciplinas_com_notas, media_geral, total_lancadas


# =====================================================================
# View — Painel do Aluno
# =====================================================================


@login_required
def painel_aluno(request):
    """
    Dashboard principal do aluno.
    """
    if not hasattr(request.user, "aluno"):
        messages.error(request, "Acesso negado. Perfil de aluno não encontrado.")
        return redirect("login")

    aluno = request.user.aluno
    turma = aluno.turma

    # Otimização: carrega disciplinas e professores
    disciplinas = Disciplina.objects.filter(turma=turma).select_related("professor")

    total_possiveis = disciplinas.count() * 4

    # Coleta notas e frequências
    disciplinas_com_notas, media_geral, total_lancadas = _coletar_notas_aluno(
        aluno, disciplinas
    )

    # Calcula situação (Aprovado/Reprovado/Recuperação)
    situacao_geral, situacao_classe = _calcular_situacao_aluno(
        disciplinas_com_notas, total_lancadas, total_possiveis
    )

    return render(
        request,
        "aluno/painel_aluno.html",
        {
            "aluno": aluno,
            "turma": turma,
            "nome_exibicao": aluno.nome_completo,
            "foto_perfil_url": get_foto_perfil(request.user),
            "disciplinas_com_notas": disciplinas_com_notas,
            "media_geral": media_geral,
            "total_notas_lancadas": total_lancadas,
            "total_notas_possiveis": total_possiveis,
            "situacao_geral": situacao_geral,
            "situacao_classe": situacao_classe,
            "agora": timezone.now(),
            # Certifique-se que estas funções auxiliares existam em seu arquivo:
            "grade_horario": (
                _get_grade_formatada(turma)
                if "_get_grade_formatada" in locals()
                or "_get_grade_formatada" in globals()
                else None
            ),
            "calendario": (
                gerar_calendario()
                if "gerar_calendario" in locals() or "gerar_calendario" in globals()
                else None
            ),
        },
    )

# =====================================================================
# Views — Grade Horária (VERSÃO CORRIGIDA)
# =====================================================================
@login_required
@user_passes_test(is_super_ou_gestor)
def grade_horaria(request, turma_id):
    turma = get_object_or_404(Turma, id=turma_id)
    user = request.user

    # Turno e horários
    turno_key = _get_turno_key(turma.turno)
    horarios = HORARIOS.get(turno_key, [])

    # Disciplinas da turma
    disciplinas_da_turma = (
        Disciplina.objects
        .filter(turma=turma)
        .select_related("professor")
    )

    # ============================
    # POST — SALVAR
    # ============================
    if request.method == "POST":

        if not is_super_ou_gestor(user):
            messages.error(
                request, "Você não tem permissão para alterar a grade horária."
            )
            return redirect("grade_horaria", turma_id=turma.id)

        GradeHorario.objects.filter(turma=turma).delete()

        registros = []

        for dia in DIAS_SEMANA:
            for i, horario in enumerate(horarios):
                disciplina_id = request.POST.get(f"{dia}_{i}")

                if not disciplina_id:
                    continue

                try:
                    disciplina = disciplinas_da_turma.get(id=disciplina_id)
                except Disciplina.DoesNotExist:
                    continue

                registros.append(
                    GradeHorario(
                        turma=turma,
                        disciplina=disciplina,
                        dia=dia,
                        horario=horario,
                    )
                )

        if registros:
            GradeHorario.objects.bulk_create(registros)

        messages.success(
            request,
            f"Grade horária da turma {turma.nome} atualizada com sucesso!"
        )
        return redirect("grade_horaria", turma_id=turma.id)

    # ============================
    # GET — EXIBIR GRADE
    # ============================

    grades = (
        GradeHorario.objects
        .filter(turma=turma)
        .select_related("disciplina", "disciplina__professor")
    )

    # ============================
    # MAPA BASE
    # ============================

    mapa_grade = {(g.dia, g.horario): g for g in grades}

    # ============================
    # CONFLITOS (GESTOR)
    # ============================

    conflitos_professores = {}
    for disc in disciplinas_da_turma:
        if disc.professor and disc.professor.id not in conflitos_professores:
            conflitos_professores[disc.professor.id] = _get_ocupados_por_professor(
                professor_id=disc.professor.id,
                ano_letivo=turma.ano,
                turma_id_atual=turma.id,
            )

    # ============================
    # FORMATO AVANÇADO (GESTOR)
    # ============================

    rows = []

    for i, horario in enumerate(horarios):
        row = {
            "horario": horario,
            "dias": []
        }

        for dia in DIAS_SEMANA:
            grade = mapa_grade.get((dia, horario))
            disciplina = grade.disciplina if grade else None

            tem_conflito = False
            if disciplina and disciplina.professor:
                chave = f"{dia}-{i}"
                if chave in conflitos_professores.get(
                    disciplina.professor.id, set()
                ):
                    tem_conflito = True

            row["dias"].append({
                "dia_slug": dia,
                "slot_index": i,
                "disciplina_atual": disciplina,
                "id_atual": disciplina.id if disciplina else "",
                "conflito": tem_conflito,
            })

        rows.append(row)

    # ============================
    # FORMATO SIMPLES (ALUNO/PROF)
    # ============================

    grade_horario = {}

    for horario in horarios:
        grade_horario[horario] = {
            "segunda": None,
            "terca": None,
            "quarta": None,
            "quinta": None,
            "sexta": None,
        }

    for g in grades:
        if g.horario in grade_horario:
            grade_horario[g.horario][g.dia] = g.disciplina.nome

    # ============================
    # CONTEXT FINAL
    # ============================

    return render(
        request,
        "core/grade_horaria.html",
        {
            "turma": turma,
            "nomes_dias": NOMES_DIAS,
            "rows": rows,  # gestor
            "grade_horario": grade_horario,  # aluno/professor
            "disciplinas": disciplinas_da_turma,
            "nome_exibicao": get_nome_exibicao(user),
            "foto_perfil_url": get_foto_perfil(user),
            "is_gestor_ou_super": is_super_ou_gestor(user),
        },
    )
# =====================================================================
# Views — Frequência
# =====================================================================


@login_required
def lancar_chamada(request, disciplina_id):
    """
    Interface para o professor realizar a chamada diária.
    Permite selecionar a data e salvar presenças/faltas em massa.
    """
    disciplina = get_object_or_404(Disciplina, id=disciplina_id)
    user = request.user

    # Validação de Permissão: Superuser, Gestor ou o Professor da Disciplina
    eh_professor_da_aula = (
        hasattr(user, "professor") and disciplina.professor == user.professor
    )
    if not (is_super_ou_gestor(user) or eh_professor_da_aula):
        messages.error(request, "Você não tem permissão para realizar esta chamada.")
        return redirect("disciplinas_professor")

    # Tratamento da Data (via GET para troca de data na interface ou POST para salvar)
    data_str = request.GET.get("data") or request.POST.get("data")
    try:
        data_selecionada = (
            date.fromisoformat(data_str) if data_str else timezone.now().date()
        )
    except ValueError:
        data_selecionada = timezone.now().date()

    alunos = disciplina.turma.alunos.all().order_by("nome_completo")

    # Mapeia frequências já existentes para carregar o formulário preenchido
    frequencias_existentes = {
        f.aluno_id: f
        for f in Frequencia.objects.filter(disciplina=disciplina, data=data_selecionada)
    }

    if request.method == "POST":
        # Lista de IDs de alunos marcados como presentes no formulário
        presentes_ids = request.POST.getlist("presentes")

        for aluno in alunos:
            # Verifica se o ID do aluno está na lista de presentes
            está_presente = str(aluno.id) in presentes_ids
            observacao = request.POST.get(f"observacao_{aluno.id}", "").strip()

            # Se estiver presente, remove observações de justificativa de falta
            if está_presente:
                observacao = ""

            Frequencia.objects.update_or_create(
                aluno=aluno,
                disciplina=disciplina,
                data=data_selecionada,
                defaults={
                    "presente": está_presente,
                    "observacao": observacao,
                },
            )

        messages.success(
            request,
            f"Chamada de {disciplina.nome} ({data_selecionada.strftime('%d/%m/%Y')}) salva!",
        )
        # Redireciona mantendo a data para conferência
        return redirect(
            f"{reverse('lancar_chamada', args=[disciplina.id])}?data={data_selecionada}"
        )

    return render(
        request,
        "frequencia/lancar_chamada.html",
        {
            "disciplina": disciplina,
            "alunos": alunos,
            "data_selecionada": data_selecionada.isoformat(),
            "data_formatada": data_selecionada.strftime("%d/%m/%Y"),
            "frequencias_existentes": frequencias_existentes,
            "nome_exibicao": get_nome_exibicao(user),
            "foto_perfil_url": get_foto_perfil(user),
        },
    )


@login_required
def historico_frequencia(request, disciplina_id):
    """
    Exibe um resumo cronológico de todas as chamadas realizadas em uma disciplina.
    """
    disciplina = get_object_or_404(Disciplina, id=disciplina_id)
    user = request.user

    if not (
        is_super_ou_gestor(user)
        or (hasattr(user, "professor") and disciplina.professor == user.professor)
    ):
        messages.error(request, "Acesso negado ao histórico desta disciplina.")
        return redirect("disciplinas_professor")

    # Agregação para evitar loop de queries no banco (otimização de performance)
    resumo_por_data = (
        Frequencia.objects.filter(disciplina=disciplina)
        .values("data")
        .annotate(
            total=Count("id"),
            presencas=Count("id", filter=Q(presente=True)),
            faltas=Count("id", filter=Q(presente=False)),
        )
        .order_by("-data")
    )

    return render(
        request,
        "frequencia/historico_frequencia.html",
        {
            "disciplina": disciplina,
            "resumo_por_data": resumo_por_data,
            "nome_exibicao": get_nome_exibicao(user),
            "foto_perfil_url": get_foto_perfil(user),
        },
    )


@login_required
def frequencia_aluno(request):
    """
    Visão do aluno sobre sua própria assiduidade por disciplina.
    """
    if not hasattr(request.user, "aluno"):
        messages.error(request, "Apenas alunos podem visualizar este relatório.")
        return redirect("dashboard")

    aluno = request.user.aluno

    # Agrega estatísticas de frequência do aluno logado
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
        {
            "aluno": aluno,
            "frequencias": frequencias,
            "nome_exibicao": get_nome_exibicao(request.user),
            "foto_perfil_url": get_foto_perfil(request.user),
        },
    )


# =====================================================================
# Views — Painel Administrativo de Usuários
# =====================================================================


@login_required
@user_passes_test(is_super_ou_gestor)
def painel_usuarios(request):
    """
    Exibe uma visão consolidada da base de usuários do sistema.
    Ideal para o controle de licenças, matrículas e auditoria de perfis.
    """
    user = request.user

    # Consolidação de estatísticas
    # Nota: Em bases de dados muito grandes, estas contagens podem ser
    # cacheadas para melhorar a performance do dashboard.
    context = {
        # Estatísticas Globais
        "total_usuarios": User.objects.count(),
        "total_alunos": Aluno.objects.count(),
        "total_professores": Professor.objects.count(),
        "total_gestores": Gestor.objects.count(),
        # Dados de Interface (Header/Sidebar)
        "nome_exibicao": get_nome_exibicao(user),
        "foto_perfil_url": get_foto_perfil(user),
        # Auxiliares de Template
        "is_gestor_ou_super": is_super_ou_gestor(user),
        "data_relatorio": timezone.now(),
    }

    return render(request, "usuarios/usuarios.html", context)
