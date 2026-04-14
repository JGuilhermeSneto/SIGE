from apps.comum.utils.constantes import HORARIOS, DIAS_SEMANA

def _calcular_situacao_nota(media_final, frequencia_percentual):
    """Define a situação acadêmica do aluno com base na média e na frequência."""
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
    """Formata valor da nota e retorna classe CSS correspondente."""
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


def _get_turno_key(turno):
    """Normaliza a string do turno."""
    if not turno:
        return ""
    return turno.lower().replace("ã", "a").replace("á", "a")


def _get_grade_horario_turma(turma):
    """Retorna a grade horária de uma turma em formato de dicionário."""
    turno_key = _get_turno_key(turma.turno)
    horarios  = HORARIOS.get(turno_key, [])

    if not horarios:
        return None

    grade_horario = {
        horario: {dia: None for dia in DIAS_SEMANA}
        for horario in horarios
    }

    from ..models.academico import GradeHorario
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

    return grade_horario if houve_registro else None


def _get_ocupados_por_professor(professor_id, ano_letivo, turma_id_atual=None):
    """IDENTIFICA slots já ocupados por um professor em outras turmas."""
    ocupados = set()
    from ..models.academico import GradeHorario
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
            turno_key = _get_turno_key(registro.turma.turno)
            lista_horarios = HORARIOS.get(turno_key, [])
            try:
                idx = lista_horarios.index(registro.horario)
                ocupados.add(f"{registro.dia}-{idx}")
            except ValueError:
                continue

    return ocupados


def _contar_notas_lancadas(disciplina, turma):
    """Conta total de avaliações preenchidas."""
    from django.db.models import Count
    from ..models.desempenho import Nota
    notas_qs = Nota.objects.filter(disciplina=disciplina, aluno__turma=turma)
    contagem = notas_qs.aggregate(
        n1=Count("nota1"),
        n2=Count("nota2"),
        n3=Count("nota3"),
        n4=Count("nota4"),
    )
    return (
        (contagem["n1"] or 0) + (contagem["n2"] or 0) +
        (contagem["n3"] or 0) + (contagem["n4"] or 0)
    )


def _calcular_detalhes_disciplina(disciplina, turma):
    """Calcula estatísticas de nota e frequência para uma disciplina."""
    from apps.usuarios.models.perfis import Aluno
    from ..models.desempenho import Nota, Frequencia
    from django.db.models import ExpressionWrapper, F, Avg, DecimalField
    from django.db.models.functions import Coalesce
    from decimal import Decimal
    total_alunos = Aluno.objects.filter(turma=turma).count()

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

    frequencias = Frequencia.objects.filter(disciplina=disciplina, aluno__turma=turma)
    total_registros = frequencias.count()
    presencas = frequencias.filter(presente=True).count()
    frequencia_geral = (presencas / total_registros * 100) if total_registros > 0 else 100

    return {
        "disciplina":       disciplina,
        "total_alunos":     total_alunos,
        "media_geral":      media_geral,
        "frequencia_geral": frequencia_geral,
    }


def _acumular_notas_professor(disciplinas_filtradas):
    """Calcula métricas globais de preenchimento para o professor."""
    from apps.usuarios.models.perfis import Aluno
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
