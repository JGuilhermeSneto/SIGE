from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Q, Count
from django.utils import timezone
import json

from ...utils.perfis import get_nome_exibicao, get_foto_perfil
from apps.academico.utils.interface_usuario import gerar_calendario
from apps.academico.utils.filtros import _get_anos_filtro
from apps.academico.models import Turma, Disciplina
from apps.usuarios.models.perfis import Professor, Aluno
from apps.comunicacao.models.comunicado import Comunicado


@login_required
def painel_super(request):
    """Dashboard principal para Superusuários e Gestores."""
    agora = datetime.now()
    ano_atual = agora.year
    from apps.calendario.models.calendario import EventoCalendario
    from apps.saude.models.ficha_medica import AtestadoMedico
    from apps.biblioteca.models.biblioteca import Livro, Emprestimo

    anos_turmas = list(Turma.objects.values_list("ano", flat=True).distinct())
    anos_cal = list(
        EventoCalendario.objects.dates("data", "year")
        .values_list("data__year", flat=True)
        .distinct()
    )
    anos_unidos = set(anos_turmas + anos_cal)
    if not anos_unidos:
        anos_unidos.add(ano_atual)
    anos_disponiveis = sorted(list(anos_unidos), reverse=True)

    ano_filtro, anos_disponiveis = _get_anos_filtro(
        anos_disponiveis, request.GET.get("ano"), ano_atual
    )

    turmas = Turma.objects.filter(ano=ano_filtro)
    MESES = [
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
    mes_nome = MESES[agora.month - 1].upper()

    # BI: Alunos por Turma
    alunos_por_turma_qs = (
        Aluno.objects.filter(turma__in=turmas)
        .values("turma__nome")
        .annotate(total=Count("id"))
        .order_by("turma__nome")
    )
    bi_turmas_labels = [row["turma__nome"] for row in alunos_por_turma_qs]
    bi_turmas_data = [row["total"] for row in alunos_por_turma_qs]

    # BI: Status de Matrícula
    status_labels_map = {
        "ATIVO": "Ativos",
        "INATIVO": "Inativos",
        "EVADIDO": "Evadidos",
        "TRANSFERIDO": "Transferidos",
        "FORMADO": "Formados",
    }
    status_qs = (
        Aluno.objects.filter(turma__in=turmas)
        .values("status_matricula")
        .annotate(total=Count("id"))
    )
    status_dict = {row["status_matricula"]: row["total"] for row in status_qs}
    bi_status_labels = list(status_labels_map.values())
    bi_status_data = [status_dict.get(k, 0) for k in status_labels_map]

    # BI: Evolução de Matrículas (Otimizado para 1 query)
    todos_anos = sorted(set(anos_turmas), reverse=False)[-5:]
    bi_evolucao_labels = [str(a) for a in todos_anos]
    
    evolucao_qs = Aluno.objects.filter(turma__ano__in=todos_anos).values("turma__ano").annotate(total=Count("id"))
    evolucao_dict = {row["turma__ano"]: row["total"] for row in evolucao_qs}
    bi_evolucao_data = [evolucao_dict.get(a, 0) for a in todos_anos]

    # BI: Atestados por Status
    atestado_status_map = {
        "PENDENTE": "Pendentes",
        "APROVADO": "Aprovados",
        "REJEITADO": "Rejeitados",
    }
    atestado_qs = AtestadoMedico.objects.values("status").annotate(total=Count("id"))
    atestado_dict = {row["status"]: row["total"] for row in atestado_qs}
    bi_atestado_labels = list(atestado_status_map.values())
    bi_atestado_data = [atestado_dict.get(k, 0) for k in atestado_status_map]

    total_livros = Livro.objects.count()
    emprestimos_ativos = Emprestimo.objects.filter(status="ATIVO").count()

    contexto = {
        "usuario": request.user,
        "nome_exibicao": get_nome_exibicao(request.user),
        "foto_perfil_url": get_foto_perfil(request.user),
        "agora": agora,
        "mes_nome": mes_nome,
        "calendario": gerar_calendario(ano_atual, agora.month, user=request.user),
        "ano_calendario": ano_atual,
        "anos_disponiveis": anos_disponiveis,
        "ano_filtro": ano_filtro,
        "total_professores": Professor.objects.filter(disciplinas__turma__in=turmas)
        .distinct()
        .count(),
        "total_alunos": Aluno.objects.filter(turma__in=turmas).distinct().count(),
        "total_turmas": turmas.count(),
        "total_disciplinas": Disciplina.objects.filter(turma__in=turmas)
        .distinct()
        .count(),
        "atestados_pendentes_count": atestado_dict.get("PENDENTE", 0),
        "total_livros": total_livros,
        "emprestimos_ativos": emprestimos_ativos,
        "comunicados": Comunicado.objects.filter(
            Q(data_expiracao__gte=timezone.now().date())
            | Q(data_expiracao__isnull=True)
        )[:5],
        "bi_turmas_labels": json.dumps(bi_turmas_labels),
        "bi_turmas_data": json.dumps(bi_turmas_data),
        "bi_status_labels": json.dumps(bi_status_labels),
        "bi_status_data": json.dumps(bi_status_data),
        "bi_evolucao_labels": json.dumps(bi_evolucao_labels),
        "bi_evolucao_data": json.dumps(bi_evolucao_data),
        "bi_atestado_labels": json.dumps(bi_atestado_labels),
        "bi_atestado_data": json.dumps(bi_atestado_data),
    }

    return render(request, "superusuario/painel_super.html", contexto)


# O painel_gestor é atualmente um alias para o painel_super (conforme URLs)
painel_gestor = painel_super
