"""
Módulo de views da aplicação core do sistema SIGE.

Correções aplicadas (v2):
- gerar_calendario(): agora retorna lista plana de células ({numero, vazio, hoje})
  compatível com {% for celula in calendario %} nos templates de aluno e professor.
- _get_grade_horario_turma(): nova função auxiliar que lê GradeHorario do banco
  e devolve o dicionário {horario: {dia: nome_disciplina}} para exibição simples.
- painel_aluno: usa _get_grade_horario_turma() e gerar_calendario() corretamente.
- painel_professor: passa 'calendario' ao contexto (estava ausente).
- visualizar_grade_professor: usa _get_grade_horario_turma() em vez de
  _get_grade_formatada() (que é exclusiva para colorir valores de notas).
- Removidas as definições duplicadas de login_view e logout_view.
- Renomeada _calcular_situacao_aluno() da seção de notas para
  _calcular_situacao_nota() para evitar conflito de nome com a homônima
  do painel do aluno.
"""

import calendar
import json
from datetime import date, datetime
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import (
    Avg,
    Count,
    DecimalField,
    ExpressionWrapper,
    F,
    Q,
)
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404, redirect, render
from django.templatetags.static import static
from django.urls import reverse
from django.utils import timezone
from django.utils.timezone import now

from .forms import (AlunoForm, EditarPerfilForm, GestorForm, LoginForm,
                    ProfessorForm)
from .models import (Aluno, Disciplina, Frequencia, Gestor, GradeHorario,
                     Nota, Professor, Turma)

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
NOMES_DIAS  = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]


# =====================================================================
# Funções Auxiliares — Situação Acadêmica e Formatação de Notas
# =====================================================================

def _calcular_situacao_nota(media_final, frequencia_percentual):
    """
    Define a situação acadêmica do aluno com base na média e na frequência.

    Regras de negócio padrão:
      - Frequência < 75 %              → Reprovado por Falta
      - Média >= 7.0 e freq >= 75 %   → Aprovado
      - Média >= 5.0                   → Recuperação
      - Média < 5.0                    → Reprovado

    Retorna um dicionário com 'texto', 'classe' (CSS badge) e 'aprovado' (bool).

    NOTA: Esta função foi renomeada de _calcular_situacao_aluno para evitar
    conflito com a homônima definida na seção do Painel do Aluno.
    """
    MEDIA_APROVACAO  = 7.0
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
    if media_final >= MEDIA_RECUPERACAO:
        return {
            "texto": "Recuperação",
            "classe": "badge bg-warning text-dark",
            "aprovado": False,
        }
    return {"texto": "Reprovado", "classe": "badge bg-danger", "aprovado": False}


def _formatar_nota(nota_valor):
    """
    Formata o valor numérico de uma nota para exibição no boletim e retorna
    a classe CSS de cor correspondente ao desempenho.

    Utilizado exclusivamente para estilização de células em tabelas de notas.
    Não deve ser chamada com objetos de turma ou disciplina — recebe apenas
    um valor numérico (float/Decimal) ou None.
    """
    if nota_valor is None:
        return {"valor": "-", "classe": "text-muted"}

    try:
        valor = float(nota_valor)
        if valor >= 7.0:
            classe = "text-success fw-bold"
        elif valor >= 5.0:
            classe = "text-warning fw-bold"
        else:
            classe = "text-danger fw-bold"
        return {"valor": f"{valor:.1f}", "classe": classe}
    except (ValueError, TypeError):
        return {"valor": "-", "classe": "text-muted"}


# =====================================================================
# Funções Auxiliares — Grade Horária
# =====================================================================

def _get_turno_key(turno):
    """Normaliza a string do turno para uso como chave no dicionário HORARIOS."""
    if not turno:
        return ""
    return turno.lower().replace("ã", "a").replace("á", "a")


def _get_grade_horario_turma(turma):
    """
    Consulta o banco de dados e retorna a grade horária de uma turma no formato
    de dicionário adequado para exibição nos templates de aluno e professor:

        {
            "07:00 às 07:45": {
                "segunda": "Matemática",
                "terca":   None,
                ...
            },
            ...
        }

    Retorna None quando não há nenhum horário cadastrado para a turma,
    permitindo que o template exiba a mensagem "grade não definida".

    Esta função substitui o uso incorreto de _formatar_nota() (antiga
    _get_grade_formatada) que era chamada com um objeto Turma como argumento
    nas views painel_aluno e visualizar_grade_professor.
    """
    turno_key = _get_turno_key(turma.turno)
    horarios  = HORARIOS.get(turno_key, [])

    if not horarios:
        return None

    # Monta a estrutura base com todos os slots vazios
    grade_horario = {
        horario: {dia: None for dia in DIAS_SEMANA}
        for horario in horarios
    }

    # Preenche os slots com as disciplinas cadastradas no banco
    registros = (
        GradeHorario.objects
        .filter(turma=turma)
        .select_related("disciplina")
    )

    houve_registro = False
    for registro in registros:
        if registro.horario in grade_horario and registro.dia in grade_horario[registro.horario]:
            grade_horario[registro.horario][registro.dia] = registro.disciplina.nome
            houve_registro = True

    # Retorna None se a grade existe na estrutura mas está completamente vazia
    return grade_horario if houve_registro else None


def _get_ocupados_por_professor(professor_id, ano_letivo, turma_id_atual=None):
    """
    Retorna um conjunto de strings 'DIA-INDICE_HORARIO' representando os
    slots já ocupados por um professor em outras turmas do mesmo ano letivo.

    O parâmetro turma_id_atual exclui a turma em edição da verificação,
    evitando falsos positivos ao editar uma grade existente.
    """
    ocupados = set()

    queryset = GradeHorario.objects.filter(turma__ano=ano_letivo).select_related(
        "disciplina__professor", "turma"
    )
    if turma_id_atual:
        queryset = queryset.exclude(turma_id=turma_id_atual)

    for registro in queryset:
        if (
            registro.disciplina
            and registro.disciplina.professor
            and registro.disciplina.professor.id == professor_id
        ):
            # Determina o índice do horário dentro do turno da turma
            turno_key = _get_turno_key(registro.turma.turno)
            lista_horarios = HORARIOS.get(turno_key, [])
            try:
                idx = lista_horarios.index(registro.horario)
                ocupados.add(f"{registro.dia}-{idx}")
            except ValueError:
                continue

    return ocupados


# =====================================================================
# Funções Auxiliares — Calendário
# =====================================================================

def gerar_calendario(ano=None, mes=None):
    """
    Gera uma lista plana de células para renderização do calendário mensal
    nos templates de aluno e professor.

    Cada célula é um dicionário com:
      - numero (int | None): número do dia (None para células vazias)
      - vazio  (bool): True para dias fora do mês atual (preenchimento da grade)
      - hoje   (bool): True se a célula corresponde ao dia atual

    A grade começa no Domingo (firstweekday=6), seguindo o padrão escolar BR.

    Retorna:
        list[dict]: lista plana de células prontas para {% for celula in calendario %}.
    """
    hoje_real = datetime.now()
    ano = int(ano) if ano else hoje_real.year
    mes = int(mes) if mes else hoje_real.month

    # firstweekday=6 faz a semana iniciar no Domingo
    cal    = calendar.Calendar(firstweekday=6)
    semanas = cal.monthdayscalendar(ano, mes)

    celulas = []
    for semana in semanas:
        for dia_num in semana:
            if dia_num == 0:
                # Célula de preenchimento fora do mês
                celulas.append({"numero": None, "vazio": True, "hoje": False})
            else:
                eh_hoje = (
                    ano   == hoje_real.year
                    and mes == hoje_real.month
                    and dia_num == hoje_real.day
                )
                celulas.append({"numero": dia_num, "vazio": False, "hoje": eh_hoje})

    return celulas


# =====================================================================
# Funções Auxiliares — Contagem de Notas
# =====================================================================

def _contar_notas_lancadas(disciplina, turma):
    """
    Conta o total de avaliações (campos nota1..nota4) já preenchidas para
    uma disciplina em uma turma específica.

    Retorna o somatório de bimestres preenchidos, útil para calcular o
    percentual de progresso no lançamento de notas.
    """
    notas_qs = Nota.objects.filter(disciplina=disciplina, aluno__turma=turma)
    contagem = notas_qs.aggregate(
        n1=Count("nota1"),
        n2=Count("nota2"),
        n3=Count("nota3"),
        n4=Count("nota4"),
    )
    return (
        (contagem["n1"] or 0)
        + (contagem["n2"] or 0)
        + (contagem["n3"] or 0)
        + (contagem["n4"] or 0)
    )


def _calcular_detalhes_disciplina(disciplina, turma):
    """
    Calcula estatísticas agregadas de nota e frequência para uma disciplina
    dentro de uma turma específica.

    Retorna dicionário com:
      - disciplina, total_alunos, media_geral, frequencia_geral, status_turma
    """
    total_alunos = Aluno.objects.filter(turma=turma).count()

    # Média calculada via ORM, com Decimal para consistência de tipo
    expressao_media = ExpressionWrapper(
        (
            Coalesce(F("nota1"), Decimal("0.0"))
            + Coalesce(F("nota2"), Decimal("0.0"))
            + Coalesce(F("nota3"), Decimal("0.0"))
            + Coalesce(F("nota4"), Decimal("0.0"))
        ) / 4,
        output_field=DecimalField(),
    )
    resultado_nota = Nota.objects.filter(
        disciplina=disciplina, aluno__turma=turma
    ).aggregate(media_turma=Avg(expressao_media))

    media_geral = resultado_nota["media_turma"] or 0

    # Frequência
    frequencias      = Frequencia.objects.filter(disciplina=disciplina, aluno__turma=turma)
    total_registros  = frequencias.count()
    total_presentes  = frequencias.filter(presente=True).count()
    frequencia_geral = (
        (total_presentes / total_registros * 100) if total_registros > 0 else 100
    )

    return {
        "disciplina":       disciplina,
        "total_alunos":     total_alunos,
        "media_geral":      round(float(media_geral), 1),
        "frequencia_geral": round(frequencia_geral, 1),
        "status_turma":     "Bom" if media_geral >= 7 else "Atenção",
    }


# =====================================================================
# Funções Utilitárias — Perfil e Roteamento
# =====================================================================

def is_superuser(user):
    """Verifica se o usuário tem privilégios exclusivos de superusuário."""
    return user.is_active and user.is_superuser


def is_super_ou_gestor(user):
    """
    Verifica acesso a áreas administrativas.
    Aceita tanto superusuários quanto usuários com perfil de Gestor vinculado.
    """
    return user.is_active and (user.is_superuser or hasattr(user, "gestor"))


def get_user_profile(user):
    """
    Retorna a instância de perfil (Aluno, Professor ou Gestor) vinculada
    ao usuário logado, ou None quando nenhum perfil for encontrado.
    """
    for tipo in ("aluno", "professor", "gestor"):
        perfil = getattr(user, tipo, None)
        if perfil:
            return perfil
    return None


def get_nome_exibicao(user):
    """
    Retorna o nome de exibição preferencial do usuário, consultando os
    perfis específicos (Gestor, Professor, Aluno) antes de recorrer
    ao nome do objeto User do Django Auth.
    """
    for tipo in ("gestor", "professor", "aluno"):
        perfil = getattr(user, tipo, None)
        if perfil and getattr(perfil, "nome_completo", None):
            return perfil.nome_completo

    nome_auth = f"{user.first_name} {user.last_name}".strip()
    return nome_auth if nome_auth else user.email


def get_foto_perfil(user):
    """
    Retorna a URL da foto de perfil do usuário ou a imagem padrão do sistema
    caso nenhuma foto tenha sido cadastrada.
    """
    for tipo in ("gestor", "professor", "aluno"):
        perfil = getattr(user, tipo, None)
        if perfil and getattr(perfil, "foto", None) and perfil.foto:
            return perfil.foto.url
    return static("core/img/default-user.png")


def redirect_user(user):
    """
    Determina a URL de destino após autenticação com base no perfil do usuário.
    A ordem de verificação garante que superusuários sejam tratados primeiro.
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


def _get_anos_filtro(anos_disponiveis, ano_selecionado, ano_atual):
    """
    Processa a seleção de ano letivo para os filtros dos dashboards.

    Garante que o ano atual e o ano selecionado estejam sempre presentes na
    lista de opções, evitando que o select fique sem a opção ativa.

    Retorna:
        (int, list): tupla com o ano de filtro ativo e a lista ordenada de anos.
    """
    try:
        ano_filtro = int(ano_selecionado) if ano_selecionado else ano_atual
    except (ValueError, TypeError):
        ano_filtro = ano_atual

    lista_anos = list(anos_disponiveis)
    if ano_atual not in lista_anos:
        lista_anos.append(ano_atual)
    if ano_filtro not in lista_anos:
        lista_anos.append(ano_filtro)

    lista_anos.sort(reverse=True)
    return ano_filtro, lista_anos


# =====================================================================
# Views — Autenticação
# =====================================================================

def login_view(request):
    """
    Gerencia a autenticação de usuários.

    Se o usuário já estiver autenticado, redireciona diretamente para o painel
    correspondente ao seu perfil, evitando acesso redundante à tela de login.
    Em caso de credenciais inválidas, o LoginForm levanta ValidationError com
    mensagem específica (e-mail não encontrado / senha incorreta).
    """
    if request.user.is_authenticated:
        return redirect(redirect_user(request.user))

    form = LoginForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        if user and user.is_active:
            login(request, user)
            return redirect(redirect_user(user))
        else:
            messages.error(request, "Esta conta está desativada.")

    return render(request, "auth/login.html", {"form": form})


def logout_view(request):
    """
    Encerra a sessão do usuário e redireciona para a tela de login.
    """
    logout(request)
    return redirect("login")


# =====================================================================
# Views — Painel Principal (Superusuário e Gestor)
# =====================================================================

@login_required
@user_passes_test(is_super_ou_gestor)
def painel_super(request):
    """
    Dashboard principal para Superusuários e Gestores.

    Exibe métricas consolidadas (professores, alunos, turmas, disciplinas)
    filtradas pelo ano letivo selecionado via query string (?ano=XXXX).
    """
    ano_atual = datetime.now().year

    anos_disponiveis = list(
        Turma.objects.values_list("ano", flat=True).distinct().order_by("-ano")
    ) or [ano_atual]

    ano_filtro, anos_disponiveis = _get_anos_filtro(
        anos_disponiveis, request.GET.get("ano"), ano_atual
    )

    turmas = Turma.objects.filter(ano=ano_filtro)

    contexto = {
        "usuario":           request.user,
        "nome_exibicao":     get_nome_exibicao(request.user),
        "foto_perfil_url":   get_foto_perfil(request.user),
        "agora":             datetime.now(),
        "calendario":        gerar_calendario(),
        "anos_disponiveis":  anos_disponiveis,
        "ano_filtro":        ano_filtro,
        "total_professores": (
            Professor.objects.filter(disciplinas__turma__in=turmas).distinct().count()
        ),
        "total_alunos":      Aluno.objects.filter(turma__in=turmas).distinct().count(),
        "total_turmas":      turmas.count(),
        "total_disciplinas": (
            Disciplina.objects.filter(turma__in=turmas).distinct().count()
        ),
    }

    return render(request, "superusuario/painel_super.html", contexto)


# =====================================================================
# Views — Usuários e Perfil
# =====================================================================

@login_required
def usuarios(request):
    """
    Controla o acesso à listagem geral de usuários.
    Gestores com cargo de diretor ou vice-diretor possuem privilégios estendidos
    para visualizar também os perfis de outros gestores.
    """
    pode_ver_gestores = request.user.is_superuser or (
        hasattr(request.user, "gestor")
        and request.user.gestor.cargo in ("diretor", "vice_diretor")
    )

    return render(
        request,
        "core/usuarios.html",
        {
            "pode_ver_gestores":  pode_ver_gestores,
            "nome_exibicao":     get_nome_exibicao(request.user),
            "foto_perfil_url":   get_foto_perfil(request.user),
        },
    )


@login_required
def editar_perfil(request):
    """
    Gerencia a atualização de dados do próprio usuário, incluindo senha e foto.

    Implementa persistência dupla:
      1. Objeto User do Django Auth (e-mail, nome)
      2. Objeto de perfil específico (Aluno / Professor / Gestor) para a foto
    Após troca de senha, atualiza o hash da sessão para não deslogar o usuário.
    """
    user   = request.user
    perfil = get_user_profile(user)

    form = EditarPerfilForm(request.POST or None, request.FILES or None, instance=user)

    if request.method == "POST":
        if form.is_valid():
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
        else:
            messages.error(request, "Erro ao atualizar perfil. Verifique os campos abaixo.")

    foto_atual = perfil.foto.url if perfil and getattr(perfil, "foto", None) else None

    return render(
        request,
        "core/editar_perfil.html",
        {
            "form":            form,
            "perfil":          perfil,
            "foto_atual":      foto_atual,
            "foto_perfil_url": get_foto_perfil(user),
            "nome_exibicao":   get_nome_exibicao(user),
        },
    )


@login_required
def remover_foto_perfil(request):
    """
    Remove fisicamente o arquivo de imagem associado ao perfil e limpa
    a referência no banco de dados.
    """
    perfil = get_user_profile(request.user)

    if not perfil:
        messages.error(request, "Nenhum perfil associado ao usuário.")
        return redirect("editar_perfil")

    if getattr(perfil, "foto", None):
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
    Usa select_related('user') para reduzir o número de queries ao banco.
    """
    query      = request.GET.get("q", "")
    professores = Professor.objects.all().select_related("user")

    if query:
        professores = professores.filter(nome_completo__icontains=query)

    return render(
        request,
        "professor/listar_professores.html",
        {
            "professores":    professores,
            "query":          query,
            "nome_exibicao":  get_nome_exibicao(request.user),
            "foto_perfil_url": get_foto_perfil(request.user),
        },
    )


@login_required
@user_passes_test(is_super_ou_gestor)
def cadastrar_professor(request):
    """
    Processa a criação de um novo professor e seu respectivo usuário de acesso.
    Erros de validação são exibidos individualmente via Django Messages.
    """
    if request.method == "POST":
        form = ProfessorForm(request.POST, request.FILES, request=request)
        if form.is_valid():
            professor = form.save()
            messages.success(
                request,
                f"Professor(a) {professor.nome_completo} cadastrado(a) com sucesso!",
            )
            return redirect("listar_professores")

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
            "form":            form,
            "professor":       None,
            "nome_exibicao":   get_nome_exibicao(request.user),
            "foto_perfil_url": get_foto_perfil(request.user),
        },
    )


@login_required
@user_passes_test(is_super_ou_gestor)
def editar_professor(request, professor_id):
    """
    Atualiza os dados de um professor existente.
    A instância é passada ao form garantindo que o Django execute UPDATE.
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
            "form":            form,
            "professor":       professor,
            "nome_exibicao":   get_nome_exibicao(request.user),
            "foto_perfil_url": get_foto_perfil(request.user),
        },
    )


@login_required
@user_passes_test(is_super_ou_gestor)
def excluir_professor(request, professor_id):
    """
    Remove o professor do sistema.
    A exclusão via professor.user.delete() revoga também o acesso ao sistema
    graças ao CASCADE configurado no modelo.
    """
    professor = get_object_or_404(Professor, id=professor_id)

    try:
        nome = professor.nome_completo
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
    Utiliza get_cargo_display() para exibir o nome amigável do cargo.
    """
    gestor = get_object_or_404(Gestor, id=gestor_id) if gestor_id else None

    if request.method == "POST":
        form = GestorForm(request.POST, request.FILES, instance=gestor, request=request)
        if form.is_valid():
            gestor_obj = form.save()
            acao = "atualizado" if gestor_id else "cadastrado"
            messages.success(
                request,
                f"{gestor_obj.get_cargo_display()} {gestor_obj.nome_completo} {acao} com sucesso!",
            )
            return redirect("listar_gestores")

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
        {
            "form":            form,
            "gestor":          gestor,
            "nome_exibicao":   get_nome_exibicao(request.user),
            "foto_perfil_url": get_foto_perfil(request.user),
        },
    )


@login_required
@user_passes_test(is_superuser)
def listar_gestores(request):
    """
    Lista todos os gestores cadastrados.
    Implementa busca por nome e usa select_related para otimizar as queries.
    """
    query    = request.GET.get("q", "")
    gestores = Gestor.objects.select_related("user").all()

    if query:
        gestores = gestores.filter(nome_completo__icontains=query)

    return render(
        request,
        "gestor/listar_gestores.html",
        {
            "gestores":        gestores,
            "query":           query,
            "nome_exibicao":   get_nome_exibicao(request.user),
            "foto_perfil_url": get_foto_perfil(request.user),
        },
    )


@login_required
@user_passes_test(is_superuser)
def excluir_gestor(request, gestor_id):
    """
    Remove o gestor e seu acesso ao sistema via exclusão do User (CASCADE).
    """
    gestor = get_object_or_404(Gestor, id=gestor_id)

    try:
        if gestor.user:
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
    Exibe a listagem de alunos.
    select_related('user', 'turma') evita múltiplas queries durante a
    renderização da lista.
    """
    query  = request.GET.get("q", "")
    alunos = Aluno.objects.all().select_related("user", "turma")

    if query:
        alunos = alunos.filter(nome_completo__icontains=query)

    return render(
        request,
        "aluno/listar_alunos.html",
        {
            "alunos":          alunos,
            "query":           query,
            "nome_exibicao":   get_nome_exibicao(request.user),
            "foto_perfil_url": get_foto_perfil(request.user),
        },
    )


@login_required
@user_passes_test(is_super_ou_gestor)
def cadastrar_aluno(request):
    """
    Realiza a matrícula de um novo aluno.
    request.FILES é obrigatório para processar o upload da foto.
    """
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

    return render(
        request,
        "aluno/cadastrar_aluno.html",
        {
            "form":            form,
            "aluno":           None,
            "nome_exibicao":   get_nome_exibicao(request.user),
            "foto_perfil_url": get_foto_perfil(request.user),
        },
    )


@login_required
@user_passes_test(is_super_ou_gestor)
def editar_aluno(request, aluno_id):
    """
    Edita o prontuário de um aluno existente.
    A instância passada ao form garante a execução de UPDATE no banco.
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
            "form":            form,
            "aluno":           aluno,
            "nome_exibicao":   get_nome_exibicao(request.user),
            "foto_perfil_url": get_foto_perfil(request.user),
        },
    )


@login_required
@user_passes_test(is_super_ou_gestor)
def excluir_aluno(request, aluno_id):
    """
    Remove o registro do aluno e suas credenciais de acesso via CASCADE do User.
    """
    aluno = get_object_or_404(Aluno, id=aluno_id)

    try:
        nome = aluno.nome_completo
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

@login_required
@user_passes_test(is_super_ou_gestor)
def listar_turmas(request):
    """
    Lista as turmas com filtragem por ano letivo e busca por nome.
    """
    ano_atual = timezone.localtime(timezone.now()).year
    query     = request.GET.get("q", "").strip()

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
            "turmas":           turmas,
            "query":            query,
            "ano_filtro":       ano_filtro,
            "anos_disponiveis": anos_disponiveis,
            "nome_exibicao":    get_nome_exibicao(request.user),
            "foto_perfil_url":  get_foto_perfil(request.user),
        },
    )


@login_required
@user_passes_test(is_super_ou_gestor)
def cadastrar_turma(request):
    """
    Gerencia a criação de novas turmas com validação de unicidade por ano.
    """
    erro      = None
    ano_atual = datetime.now().year
    anos      = list(range(2010, ano_atual + 2))

    if request.method == "POST":
        nome    = request.POST.get("nome")
        turno   = request.POST.get("turno")
        ano_str = request.POST.get("ano")

        try:
            ano = int(ano_str)
            if ano < 2010 or ano > ano_atual + 1:
                erro = "O ano letivo deve estar entre 2010 e o próximo ano."
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
            "erro":            erro,
            "anos":            anos,
            "nome_exibicao":   get_nome_exibicao(request.user),
            "foto_perfil_url": get_foto_perfil(request.user),
        },
    )


@login_required
@user_passes_test(is_super_ou_gestor)
def editar_turma(request, turma_id):
    """
    Atualiza os dados de uma turma, verificando conflito de nome/ano com
    outras turmas (excluindo a própria instância da verificação).
    """
    turma     = get_object_or_404(Turma, id=turma_id)
    erro      = None
    ano_atual = datetime.now().year
    anos      = list(range(2010, ano_atual + 2))

    if request.method == "POST":
        nome  = request.POST.get("nome")
        turno = request.POST.get("turno")
        ano   = request.POST.get("ano")

        if Turma.objects.filter(nome=nome, ano=ano).exclude(id=turma.id).exists():
            erro = "Já existe outra turma com esse nome cadastrada para este ano."
        else:
            turma.nome  = nome
            turma.turno = turno
            turma.ano   = ano
            turma.save()
            messages.success(request, "Dados da turma atualizados com sucesso.")
            return redirect("listar_turmas")

    return render(
        request,
        "turma/cadastrar_turma.html",
        {
            "turma":           turma,
            "erro":            erro,
            "anos":            anos,
            "nome_exibicao":   get_nome_exibicao(request.user),
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
    Secretários não têm permissão para realizar esta ação.
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
    Exibe os detalhes de uma disciplina com a lista de alunos e suas notas.
    Acesso: Superusuários, Gestores e o Professor responsável pela disciplina.
    """
    disciplina = get_object_or_404(Disciplina, id=disciplina_id)

    eh_professor_da_disc = (
        hasattr(request.user, "professor")
        and disciplina.professor == request.user.professor
    )

    if not (is_super_ou_gestor(request.user) or eh_professor_da_disc):
        messages.error(request, "Você não tem permissão para visualizar esta disciplina.")
        return redirect("dashboard")

    turma = disciplina.turma
    alunos = (
        Aluno.objects.filter(turma=turma)
        .select_related("user")
        .order_by("nome_completo")
    )
    notas      = Nota.objects.filter(disciplina=disciplina).select_related("aluno")
    notas_dict = {nota.aluno.id: nota for nota in notas}

    return render(
        request,
        "disciplina/visualizar_disciplinas.html",
        {
            "disciplina":        disciplina,
            "turma":             turma,
            "alunos":            alunos,
            "notas_dict":        notas_dict,
            "nome_exibicao":     get_nome_exibicao(request.user),
            "foto_perfil_url":   get_foto_perfil(request.user),
            "is_gestor_ou_super": is_super_ou_gestor(request.user),
        },
    )


@login_required
@user_passes_test(is_super_ou_gestor)
def cadastrar_disciplina_para_turma(request, turma_id):
    """
    Vincula uma nova disciplina (com professor responsável) a uma turma.
    """
    turma = get_object_or_404(Turma, id=turma_id)

    if request.method == "POST":
        nome         = request.POST.get("nome")
        professor_id = request.POST.get("professor")

        if not nome or not professor_id:
            messages.error(request, "Preencha todos os campos obrigatórios.")
        else:
            professor = get_object_or_404(Professor, id=professor_id)
            if Disciplina.objects.filter(nome=nome, turma=turma).exists():
                messages.error(request, f"A disciplina '{nome}' já existe nesta turma.")
            else:
                Disciplina.objects.create(nome=nome, professor=professor, turma=turma)
                messages.success(request, f"Disciplina '{nome}' cadastrada com sucesso!")
                return redirect("listar_disciplinas_turma", turma_id=turma.id)

    professores = Professor.objects.all().select_related("user")
    return render(
        request,
        "disciplina/cadastrar_disciplina_turma.html",
        {
            "turma":           turma,
            "professores":     professores,
            "nome_exibicao":   get_nome_exibicao(request.user),
            "foto_perfil_url": get_foto_perfil(request.user),
        },
    )


@login_required
@user_passes_test(is_super_ou_gestor)
def editar_disciplina(request, disciplina_id):
    """
    Edita o nome e/ou o professor responsável por uma disciplina.
    """
    disciplina  = get_object_or_404(Disciplina, id=disciplina_id)
    professores = Professor.objects.all().select_related("user")

    if request.method == "POST":
        nome         = request.POST.get("nome")
        professor_id = request.POST.get("professor")
        professor_novo = get_object_or_404(Professor, id=professor_id)

        disciplina.nome      = nome
        disciplina.professor = professor_novo
        disciplina.save()

        messages.success(request, "Disciplina atualizada com sucesso!")
        return redirect("listar_disciplinas_turma", turma_id=disciplina.turma.id)

    return render(
        request,
        "disciplina/cadastrar_disciplina_turma.html",
        {
            "disciplina":      disciplina,
            "turma":           disciplina.turma,
            "professores":     professores,
            "nome_exibicao":   get_nome_exibicao(request.user),
            "foto_perfil_url": get_foto_perfil(request.user),
        },
    )


@login_required
@user_passes_test(is_super_ou_gestor)
def listar_disciplinas_turma(request, turma_id):
    """
    Visão administrativa: lista todas as disciplinas de uma turma.
    """
    turma      = get_object_or_404(Turma, id=turma_id)
    query      = request.GET.get("q", "")
    disciplinas = Disciplina.objects.filter(turma=turma).select_related("professor__user")

    if query:
        disciplinas = disciplinas.filter(nome__icontains=query)

    return render(
        request,
        "disciplina/listar_disciplinas_turma.html",
        {
            "turma":           turma,
            "disciplinas":     disciplinas,
            "query":           query,
            "nome_exibicao":   get_nome_exibicao(request.user),
            "foto_perfil_url": get_foto_perfil(request.user),
        },
    )


@login_required
def disciplinas_turma(request, turma_id):
    """
    Visão híbrida: exibe as disciplinas de uma turma com dados analíticos.
    Professor vê apenas as suas; Gestor/Super vê todas.
    """
    user  = request.user
    turma = get_object_or_404(Turma, id=turma_id)

    if hasattr(user, "professor"):
        disciplinas_qs = Disciplina.objects.filter(turma=turma, professor=user.professor)
    elif user.is_superuser or hasattr(user, "gestor"):
        disciplinas_qs = Disciplina.objects.filter(turma=turma)
    else:
        return redirect("login")

    disciplinas_qs = disciplinas_qs.order_by("nome")

    if not disciplinas_qs.exists():
        messages.warning(request, "Nenhuma disciplina encontrada nesta turma.")
        return redirect("listar_turmas")

    disciplinas_detalhadas = [
        _calcular_detalhes_disciplina(d, turma) for d in disciplinas_qs
    ]

    return render(
        request,
        "professor/disciplinas_turma.html",
        {
            "turma":               turma,
            "disciplinas_detalhadas": disciplinas_detalhadas,
            "is_gestor_ou_super":  user.is_superuser or hasattr(user, "gestor"),
            "nome_exibicao":       get_nome_exibicao(user),
            "foto_perfil_url":     get_foto_perfil(user),
        },
    )


@login_required
@user_passes_test(is_super_ou_gestor)
def excluir_disciplina(request, disciplina_id):
    """
    Remove uma disciplina da grade da turma.
    """
    disciplina = get_object_or_404(Disciplina, id=disciplina_id)
    turma_id   = disciplina.turma.id
    nome_disc  = disciplina.nome

    disciplina.delete()
    messages.success(request, f"Disciplina '{nome_disc}' excluída com sucesso!")
    return redirect("listar_disciplinas_turma", turma_id=turma_id)


# =====================================================================
# Funções Auxiliares — Painel do Professor
# =====================================================================

def _get_ano_filtro_professor(request, anos_disponiveis, ano_atual):
    """
    Gerencia a persistência do filtro de ano letivo na sessão do usuário.
    Prioriza o parâmetro GET; quando ausente, usa o valor salvo na sessão;
    como último recurso, usa o ano atual.
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
        anos_disponiveis = sorted(
            list(set(anos_disponiveis + [ano_filtro])), reverse=True
        )
    return ano_filtro, anos_disponiveis


def _acumular_notas_professor(disciplinas_filtradas):
    """
    Calcula métricas globais de preenchimento de notas para o painel do professor.

    Retorna:
        (int, int, int, list): total de notas possíveis, lançadas,
        número único de alunos e lista detalhada de disciplinas com percentuais.
    """
    total_notas_possiveis = 0
    total_notas_lancadas  = 0
    alunos_ids            = set()
    disciplinas_detalhadas = []

    for disciplina in disciplinas_filtradas:
        turma        = disciplina.turma
        alunos_da_turma = Aluno.objects.filter(turma=turma).values_list("id", flat=True)
        alunos_count    = alunos_da_turma.count()
        alunos_ids.update(alunos_da_turma)

        notas_possiveis_disc = alunos_count * 4
        notas_lancadas_disc  = _contar_notas_lancadas(disciplina, turma)

        total_notas_possiveis += notas_possiveis_disc
        total_notas_lancadas  += notas_lancadas_disc

        percentual = (
            int((notas_lancadas_disc / notas_possiveis_disc * 100))
            if notas_possiveis_disc > 0 else 0
        )

        disciplinas_detalhadas.append({
            "disciplina":      disciplina,
            "alunos_count":    alunos_count,
            "notas_lancadas":  notas_lancadas_disc,
            "notas_possiveis": notas_possiveis_disc,
            "percentual":      percentual,
        })

    return (
        total_notas_possiveis,
        total_notas_lancadas,
        len(alunos_ids),
        disciplinas_detalhadas,
    )


# =====================================================================
# Views — Painel do Professor
# =====================================================================

@login_required
def painel_professor(request):
    """
    Dashboard principal do professor.

    Exibe métricas de disciplinas, turmas, alunos e progresso de notas
    filtradas pelo ano letivo. Também passa o calendário mensal e a hora
    atual para o template.

    CORREÇÃO: 'calendario' agora é incluído no contexto via gerar_calendario(),
    que retorna a lista plana de células ({numero, vazio, hoje}) esperada
    pelo template ({% for celula in calendario %}).
    """
    if not hasattr(request.user, "professor"):
        messages.error(request, "Acesso restrito a professores.")
        return redirect("login")

    professor = request.user.professor
    ano_atual = timezone.now().year

    # Anos em que o professor possui disciplinas cadastradas
    anos_disponiveis = list(
        Turma.objects.filter(disciplinas__professor=professor)
        .values_list("ano", flat=True)
        .distinct()
        .order_by("-ano")
    ) or [ano_atual]

    ano_filtro, anos_disponiveis = _get_ano_filtro_professor(
        request, anos_disponiveis, ano_atual
    )

    disciplinas_filtradas = Disciplina.objects.filter(
        professor=professor, turma__ano=ano_filtro
    ).select_related("turma")

    (
        total_notas_possiveis,
        total_notas_lancadas,
        total_alunos,
        disciplinas_detalhadas,
    ) = _acumular_notas_professor(disciplinas_filtradas)

    agora = timezone.now()

    return render(
        request,
        "professor/painel_professor.html",
        {
            "professor":            professor,
            "nome_exibicao":        professor.nome_completo,
            "foto_perfil_url":      get_foto_perfil(request.user),
            "total_disciplinas":    disciplinas_filtradas.count(),
            "total_turmas":         disciplinas_filtradas.values("turma").distinct().count(),
            "total_alunos":         total_alunos,
            "total_notas_lancadas": total_notas_lancadas,
            "total_notas_possiveis": total_notas_possiveis,
            "disciplinas_detalhadas": disciplinas_detalhadas,
            "anos_disponiveis":     anos_disponiveis,
            "ano_filtro":           ano_filtro,
            "agora":                agora,
            # CORREÇÃO: calendário ausente anteriormente — agora incluído corretamente.
            # gerar_calendario() retorna lista plana compatível com o template.
            "calendario":           gerar_calendario(agora.year, agora.month),
        },
    )


@login_required
def disciplinas_professor(request):
    """
    Lista as turmas do professor com opção de filtrar por ano e buscar por nome.
    """
    if not hasattr(request.user, "professor"):
        return redirect("login")

    professor = request.user.professor
    ano_atual = timezone.now().year

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
            "turma":            turma,
            "disciplinas_count": Disciplina.objects.filter(
                turma=turma, professor=professor
            ).count(),
            "alunos_count":    Aluno.objects.filter(turma=turma).count(),
            "turno_display":   turma.get_turno_display(),
        }
        for turma in turmas
    ]

    return render(
        request,
        "professor/disciplinas_professor.html",
        {
            "turmas_detalhadas": turmas_detalhadas,
            "nome_exibicao":    get_nome_exibicao(request.user),
            "foto_perfil_url":  get_foto_perfil(request.user),
            "query":            query,
            "anos_disponiveis": anos_disponiveis,
            "ano_filtro":       ano_filtro,
        },
    )


@login_required
def visualizar_grade_professor(request, turma_id):
    """
    Exibe a grade horária de uma turma na perspectiva do professor.

    CORREÇÃO: substituída a chamada incorreta a _formatar_nota(turma) pela
    função adequada _get_grade_horario_turma(turma), que consulta o modelo
    GradeHorario e devolve o dicionário {horario: {dia: nome_disciplina}}.
    """
    if not hasattr(request.user, "professor"):
        return redirect("login")

    professor       = request.user.professor
    turma           = get_object_or_404(Turma, id=turma_id)
    disciplinas_prof = Disciplina.objects.filter(turma=turma, professor=professor)

    if not disciplinas_prof.exists():
        messages.error(request, "Você não possui disciplinas vinculadas a esta turma.")
        return redirect("disciplinas_professor")

    return render(
        request,
        "professor/visualizar_grade_professor.html",
        {
            "turma":                turma,
            # CORREÇÃO: usa _get_grade_horario_turma() — lê GradeHorario do banco.
            "grade_horario":        _get_grade_horario_turma(turma),
            "nomes_dias":           NOMES_DIAS,
            "disciplinas_professor": disciplinas_prof,
            "nome_exibicao":        get_nome_exibicao(request.user),
            "foto_perfil_url":      get_foto_perfil(request.user),
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

    Segurança: apenas o Professor da disciplina, Gestores e Superusuários
    têm acesso. Valores inválidos são reportados sem interromper o salvamento
    das notas válidas restantes.
    """
    disciplina = get_object_or_404(Disciplina, id=disciplina_id)
    user       = request.user

    eh_professor_da_disc = (
        hasattr(user, "professor") and disciplina.professor == user.professor
    )
    if not (is_super_ou_gestor(user) or eh_professor_da_disc):
        messages.error(request, "Você não tem permissão para lançar notas nesta disciplina.")
        return redirect("dashboard")

    alunos = (
        Aluno.objects.filter(turma_id=disciplina.turma_id)
        .select_related("user")
        .order_by("nome_completo")
    )

    if request.method == "POST":
        houve_erro = False
        for aluno in alunos:
            nota_obj, _ = Nota.objects.get_or_create(
                aluno_id=aluno.pk, disciplina_id=disciplina.id
            )

            for i in range(1, 5):
                campo = f"nota{i}_{aluno.pk}"
                valor = request.POST.get(campo, "").strip()

                if valor == "":
                    setattr(nota_obj, f"nota{i}", None)
                    continue

                try:
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

            nota_obj.save()

        if not houve_erro:
            messages.success(request, "Notas processadas e salvas com sucesso!")
        else:
            messages.warning(
                request,
                "Algumas notas foram salvas, mas houve erros em valores específicos.",
            )
        return redirect("lancar_nota", disciplina_id=disciplina.id)

    notas_dict = {
        n.aluno_id: n for n in Nota.objects.filter(disciplina_id=disciplina.id)
    }

    return render(
        request,
        "professor/lancar_nota.html",
        {
            "disciplina":        disciplina,
            "alunos":            alunos,
            "notas_dict":        notas_dict,
            "is_gestor_ou_super": is_super_ou_gestor(user),
            "nome_exibicao":     get_nome_exibicao(user),
            "foto_perfil_url":   get_foto_perfil(user),
        },
    )


# =====================================================================
# Funções Auxiliares — Painel do Aluno
# =====================================================================

def _calcular_situacao_aluno(disciplinas_com_notas, total_lancadas, total_possiveis):
    """
    Define a situação acadêmica geral do aluno com base nas médias e no
    progresso de lançamento de notas.

    Retorna uma tupla (texto_situacao, classe_css).
    """
    if total_possiveis == 0:
        return "Sem Dados", "info"

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
    Agrega notas e estatísticas de frequência para todas as disciplinas do aluno.

    Realiza as queries de forma otimizada (uma por tipo de dado) para evitar
    o problema N+1 durante a renderização do painel.

    Retorna:
        (list, float|None, int): lista de disciplinas com dados, média geral e
        total de bimestres lançados.
    """
    disciplinas_com_notas = []
    soma_medias     = 0
    total_com_media = 0
    total_lancadas  = 0

    # Busca todas as notas do aluno de uma só vez para evitar N+1
    notas_aluno = {n.disciplina_id: n for n in Nota.objects.filter(aluno=aluno)}

    # Frequências agregadas por disciplina — evita múltiplas queries no loop
    frequencias_agregadas = (
        Frequencia.objects.filter(aluno=aluno)
        .values("disciplina_id")
        .annotate(
            total=Count("id"),
            presencas=Count("id", filter=Q(presente=True)),
        )
    )
    freq_dict = {f["disciplina_id"]: f for f in frequencias_agregadas}

    for disciplina in disciplinas:
        nota = notas_aluno.get(disciplina.id)

        total_lancadas += _contar_notas_lancadas(disciplina, aluno.turma)

        dados_freq   = freq_dict.get(disciplina.id, {"total": 0, "presencas": 0})
        total_aulas  = dados_freq["total"]
        presencas    = dados_freq["presencas"]
        faltas       = total_aulas - presencas
        percentual_faltas = (
            round((faltas / total_aulas * 100), 1) if total_aulas > 0 else 0
        )

        disciplinas_com_notas.append({
            "disciplina":        disciplina,
            "nota":              nota,
            "total_aulas":       total_aulas,
            "presencas":         presencas,
            "faltas":            faltas,
            "percentual_faltas": percentual_faltas,
        })

        if nota and nota.media is not None:
            soma_medias     += float(nota.media)
            total_com_media += 1

    media_geral = soma_medias / total_com_media if total_com_media > 0 else None
    return disciplinas_com_notas, media_geral, total_lancadas


# =====================================================================
# Views — Painel do Aluno
# =====================================================================

@login_required
def painel_aluno(request):
    """
    Dashboard principal do aluno.

    Exibe notas bimestrais, média geral, frequência por disciplina,
    situação acadêmica, grade horária e calendário mensal.

    CORREÇÕES:
    - grade_horario: substituída a chamada incorreta a _formatar_nota(turma)
      por _get_grade_horario_turma(turma), que consulta GradeHorario no banco.
    - calendario: gerar_calendario() agora retorna lista plana de células
      ({numero, vazio, hoje}), compatível com {% for celula in calendario %}.
    """
    if not hasattr(request.user, "aluno"):
        messages.error(request, "Acesso negado. Perfil de aluno não encontrado.")
        return redirect("login")

    aluno = request.user.aluno
    turma = aluno.turma

    disciplinas = Disciplina.objects.filter(turma=turma).select_related("professor")
    total_possiveis = disciplinas.count() * 4

    disciplinas_com_notas, media_geral, total_lancadas = _coletar_notas_aluno(
        aluno, disciplinas
    )

    situacao_geral, situacao_classe = _calcular_situacao_aluno(
        disciplinas_com_notas, total_lancadas, total_possiveis
    )

    agora = timezone.now()

    return render(
        request,
        "aluno/painel_aluno.html",
        {
            "aluno":                  aluno,
            "turma":                  turma,
            "nome_exibicao":          aluno.nome_completo,
            "foto_perfil_url":        get_foto_perfil(request.user),
            "disciplinas_com_notas":  disciplinas_com_notas,
            "media_geral":            media_geral,
            "total_notas_lancadas":   total_lancadas,
            "total_notas_possiveis":  total_possiveis,
            "situacao_geral":         situacao_geral,
            "situacao_classe":        situacao_classe,
            "agora":                  agora,
            # CORREÇÃO: consulta GradeHorario no banco via função dedicada.
            "grade_horario":          _get_grade_horario_turma(turma),
            # CORREÇÃO: lista plana de células compatível com o template.
            "calendario":             gerar_calendario(agora.year, agora.month),
        },
    )


# =====================================================================
# Views — Grade Horária (Gestor)
# =====================================================================

@login_required
@user_passes_test(is_super_ou_gestor)
def grade_horaria(request, turma_id):
    """
    Permite ao Gestor/Superusuário visualizar e editar a grade horária de uma turma.

    No POST: apaga os registros anteriores de GradeHorario e recria via bulk_create,
    garantindo atomicidade simples sem necessidade de transação explícita.

    No GET: monta duas estruturas de dados:
      - rows: formato avançado (para o formulário do gestor com detecção de conflitos)
      - grade_horario: formato simples {horario: {dia: nome}} (para visualização)
    """
    turma    = get_object_or_404(Turma, id=turma_id)
    user     = request.user
    turno_key = _get_turno_key(turma.turno)
    horarios  = HORARIOS.get(turno_key, [])

    disciplinas_da_turma = (
        Disciplina.objects
        .filter(turma=turma)
        .select_related("professor")
    )

    # ----------------------------------------------------------------
    # POST — Salvar grade horária
    # ----------------------------------------------------------------
    if request.method == "POST":
        if not is_super_ou_gestor(user):
            messages.error(request, "Você não tem permissão para alterar a grade horária.")
            return redirect("grade_horaria", turma_id=turma.id)

        # Remove todos os slots existentes antes de recriar
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

    # ----------------------------------------------------------------
    # GET — Exibir grade
    # ----------------------------------------------------------------

    grades    = (
        GradeHorario.objects
        .filter(turma=turma)
        .select_related("disciplina", "disciplina__professor")
    )
    mapa_grade = {(g.dia, g.horario): g for g in grades}

    # Pré-calcula slots ocupados por cada professor em outras turmas do mesmo ano
    conflitos_professores = {}
    for disc in disciplinas_da_turma:
        if disc.professor and disc.professor.id not in conflitos_professores:
            conflitos_professores[disc.professor.id] = _get_ocupados_por_professor(
                professor_id=disc.professor.id,
                ano_letivo=turma.ano,
                turma_id_atual=turma.id,
            )

    # Formato avançado para o formulário de edição do gestor
    rows = []
    for i, horario in enumerate(horarios):
        row = {"horario": horario, "dias": []}
        for dia in DIAS_SEMANA:
            grade      = mapa_grade.get((dia, horario))
            disciplina = grade.disciplina if grade else None

            tem_conflito = False
            if disciplina and disciplina.professor:
                chave = f"{dia}-{i}"
                if chave in conflitos_professores.get(disciplina.professor.id, set()):
                    tem_conflito = True

            row["dias"].append({
                "dia_slug":        dia,
                "slot_index":      i,
                "disciplina_atual": disciplina,
                "id_atual":        disciplina.id if disciplina else "",
                "conflito":        tem_conflito,
            })
        rows.append(row)

    # Formato simples {horario: {dia: nome}} para visualização de aluno/professor
    grade_horario = {
        horario: {dia: None for dia in DIAS_SEMANA}
        for horario in horarios
    }
    for g in grades:
        if g.horario in grade_horario:
            grade_horario[g.horario][g.dia] = g.disciplina.nome

    return render(
        request,
        "core/grade_horaria.html",
        {
            "turma":             turma,
            "nomes_dias":        NOMES_DIAS,
            "rows":              rows,
            "grade_horario":     grade_horario,
            "disciplinas":       disciplinas_da_turma,
            "nome_exibicao":     get_nome_exibicao(user),
            "foto_perfil_url":   get_foto_perfil(user),
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

    Permite selecionar a data via GET e salvar presenças/faltas em massa via POST.
    Usa update_or_create para idempotência: chamar duas vezes na mesma data
    atualiza o registro em vez de duplicá-lo.
    """
    disciplina = get_object_or_404(Disciplina, id=disciplina_id)
    user       = request.user

    eh_professor_da_aula = (
        hasattr(user, "professor") and disciplina.professor == user.professor
    )
    if not (is_super_ou_gestor(user) or eh_professor_da_aula):
        messages.error(request, "Você não tem permissão para realizar esta chamada.")
        return redirect("disciplinas_professor")

    data_str = request.GET.get("data") or request.POST.get("data")
    try:
        data_selecionada = (
            date.fromisoformat(data_str) if data_str else timezone.now().date()
        )
    except ValueError:
        data_selecionada = timezone.now().date()

    alunos = disciplina.turma.alunos.all().order_by("nome_completo")

    frequencias_existentes = {
        f.aluno_id: f
        for f in Frequencia.objects.filter(disciplina=disciplina, data=data_selecionada)
    }

    if request.method == "POST":
        presentes_ids = request.POST.getlist("presentes")

        for aluno in alunos:
            esta_presente = str(aluno.id) in presentes_ids
            observacao    = request.POST.get(f"observacao_{aluno.id}", "").strip()

            # Alunos presentes não precisam de observação de falta
            if esta_presente:
                observacao = ""

            Frequencia.objects.update_or_create(
                aluno=aluno,
                disciplina=disciplina,
                data=data_selecionada,
                defaults={"presente": esta_presente, "observacao": observacao},
            )

        messages.success(
            request,
            f"Chamada de {disciplina.nome} ({data_selecionada.strftime('%d/%m/%Y')}) salva!",
        )
        return redirect(
            f"{reverse('lancar_chamada', args=[disciplina.id])}?data={data_selecionada}"
        )

    return render(
        request,
        "frequencia/lancar_chamada.html",
        {
            "disciplina":            disciplina,
            "alunos":                alunos,
            "data_selecionada":      data_selecionada.isoformat(),
            "data_formatada":        data_selecionada.strftime("%d/%m/%Y"),
            "frequencias_existentes": frequencias_existentes,
            "nome_exibicao":         get_nome_exibicao(user),
            "foto_perfil_url":       get_foto_perfil(user),
        },
    )


@login_required
def historico_frequencia(request, disciplina_id):
    """
    Exibe um resumo cronológico de todas as chamadas realizadas em uma disciplina.
    Usa anotação ORM para evitar queries adicionais durante a renderização.
    """
    disciplina = get_object_or_404(Disciplina, id=disciplina_id)
    user       = request.user

    if not (
        is_super_ou_gestor(user)
        or (hasattr(user, "professor") and disciplina.professor == user.professor)
    ):
        messages.error(request, "Acesso negado ao histórico desta disciplina.")
        return redirect("disciplinas_professor")

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
            "disciplina":      disciplina,
            "resumo_por_data": resumo_por_data,
            "nome_exibicao":   get_nome_exibicao(user),
            "foto_perfil_url": get_foto_perfil(user),
        },
    )


@login_required
def frequencia_aluno(request):
    """
    Exibe ao aluno logado seu histórico de frequência consolidado por disciplina.
    """
    if not hasattr(request.user, "aluno"):
        messages.error(request, "Apenas alunos podem visualizar este relatório.")
        return redirect("dashboard")

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
        {
            "aluno":           aluno,
            "frequencias":     frequencias,
            "nome_exibicao":   get_nome_exibicao(request.user),
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
    Visão consolidada da base de usuários do sistema para auditoria e controle.
    Em bases muito grandes, as contagens podem ser cacheadas para melhorar
    a performance do dashboard.
    """
    user = request.user

    context = {
        "total_usuarios":    User.objects.count(),
        "total_alunos":      Aluno.objects.count(),
        "total_professores": Professor.objects.count(),
        "total_gestores":    Gestor.objects.count(),
        "nome_exibicao":     get_nome_exibicao(user),
        "foto_perfil_url":   get_foto_perfil(user),
        "is_gestor_ou_super": is_super_ou_gestor(user),
        "data_relatorio":    timezone.now(),
    }

    return render(request, "usuarios/usuarios.html", context)