from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from ..utils.perfis import get_nome_exibicao, get_foto_perfil, redirect_user
from apps.academico.utils.interface_usuario import gerar_calendario
from apps.academico.utils.filtros import _get_anos_filtro
from apps.academico.utils.academico import _get_grade_horario_turma

from ..models.perfis import Professor, Aluno
from apps.academico.models.academico import Turma, Disciplina

@login_required
def painel_super(request):
    """Dashboard principal para Superusuários e Gestores."""
    ano_atual = datetime.now().year
    from apps.calendario.models.calendario import EventoCalendario
    anos_turmas = list(Turma.objects.values_list("ano", flat=True).distinct())
    anos_cal = list(EventoCalendario.objects.dates('data', 'year').values_list('data__year', flat=True).distinct())
    anos_unidos = set(anos_turmas + anos_cal)
    if not anos_unidos:
        anos_unidos.add(ano_atual)
    anos_disponiveis = sorted(list(anos_unidos), reverse=True)

    ano_filtro, anos_disponiveis = _get_anos_filtro(
        anos_disponiveis, request.GET.get("ano"), ano_atual
    )

    turmas = Turma.objects.filter(ano=ano_filtro)
    MESES = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    mes_nome = MESES[datetime.now().month - 1].upper()

    contexto = {
        "usuario":           request.user,
        "nome_exibicao":     get_nome_exibicao(request.user),
        "foto_perfil_url":   get_foto_perfil(request.user),
        "agora":             datetime.now(),
        "mes_nome":          mes_nome,
        "calendario":        gerar_calendario(ano_filtro, datetime.now().month),
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


@login_required
def painel_professor(request):
    """Dashboard principal para Professores."""
    professor = getattr(request.user, 'professor', None)
    if not professor:
        return render(request, "core/sem_perfil.html")

    hoje = datetime.now()
    ano_atual = hoje.year
    
    # Filtro de Ano Letivo
    from apps.calendario.models.calendario import EventoCalendario
    anos_turmas = list(
        Turma.objects.filter(disciplinas__professor=professor)
        .values_list("ano", flat=True)
        .distinct()
    )
    anos_cal = list(EventoCalendario.objects.dates('data', 'year').values_list('data__year', flat=True).distinct())
    anos_unidos = set(anos_turmas + anos_cal)
    if not anos_unidos:
        anos_unidos.add(ano_atual)
    anos_disponiveis = sorted(list(anos_unidos), reverse=True)
    
    ano_filtro, anos_disponiveis = _get_anos_filtro(
        anos_disponiveis, request.GET.get("ano"), ano_atual
    )

    # Disciplinas e Turmas vinculadas ao professor no ano selecionado
    from apps.academico.models.academico import Disciplina
    disciplinas = Disciplina.objects.filter(
        professor=professor, 
        turma__ano=ano_filtro
    ).select_related("turma")
    
    turmas_ids = disciplinas.values_list("turma_id", flat=True).distinct()
    
    # Calcular métricas via utilitário acumulador
    from apps.academico.utils.academico import _acumular_notas_professor
    total_possiveis, total_lancadas, total_alunos_unicos, _ = _acumular_notas_professor(disciplinas)

    MESES = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    mes_nome = MESES[hoje.month - 1].upper()

    contexto = {
        "professor":               professor,
        "nome_exibicao":           get_nome_exibicao(request.user),
        "foto_perfil_url":         get_foto_perfil(request.user),
        "agora":                   hoje,
        "mes_nome":                mes_nome,
        "calendario":              gerar_calendario(ano_filtro, hoje.month),
        "total_turmas":            turmas_ids.count(),
        "total_alunos":            total_alunos_unicos,
        "total_disciplinas":       disciplinas.count(),
        "total_notas_lancadas":    total_lancadas,
        "total_notas_possiveis":   total_possiveis,
        "anos_disponiveis":        anos_disponiveis,
        "ano_filtro":              ano_filtro,
    }

    return render(request, "professor/painel_professor.html", contexto)


@login_required
def painel_aluno(request):
    """Dashboard principal para Alunos."""
    aluno = getattr(request.user, 'aluno', None)
    if not aluno:
        return render(request, "core/sem_perfil.html")

    grade = _get_grade_horario_turma(aluno.turma)
    
    from apps.academico.models.academico import Disciplina
    from apps.academico.models.desempenho import Nota, Frequencia
    from apps.academico.utils.academico import _calcular_situacao_nota
    
    disciplinas = Disciplina.objects.filter(turma=aluno.turma).select_related('professor')
    
    disciplinas_com_notas = []
    soma_medias = 0
    total_disciplinas_com_media = 0
    total_notas_possiveis = disciplinas.count() * 4
    total_notas_lancadas = 0

    for disciplina in disciplinas:
        nota = Nota.objects.filter(disciplina=disciplina, aluno=aluno).first()
        if nota:
            for n in [nota.nota1, nota.nota2, nota.nota3, nota.nota4]:
                if n is not None:
                    total_notas_lancadas += 1
            if nota.media:
                soma_medias += nota.media
                total_disciplinas_com_media += 1
        
        frequencias = Frequencia.objects.filter(disciplina=disciplina, aluno=aluno)
        total_aulas = frequencias.count()
        faltas = frequencias.filter(presente=False).count()
        percentual_faltas = (faltas / total_aulas * 100) if total_aulas > 0 else 0
        
        disciplinas_com_notas.append({
            'disciplina': disciplina,
            'nota': nota,
            'total_aulas': total_aulas,
            'faltas': faltas,
            'percentual_faltas': int(percentual_faltas)
        })
        
    media_geral = (soma_medias / total_disciplinas_com_media) if total_disciplinas_com_media > 0 else 0
    
    freq_total = Frequencia.objects.filter(aluno=aluno)
    total_aulas_gerais = freq_total.count()
    faltas_gerais = freq_total.filter(presente=False).count()
    percentual_frequencia_geral = 100 - ((faltas_gerais / total_aulas_gerais * 100) if total_aulas_gerais > 0 else 0)

    if total_disciplinas_com_media > 0 or total_aulas_gerais > 0:
        sit_dict = _calcular_situacao_nota(media_geral, percentual_frequencia_geral)
        situacao_geral = sit_dict["texto"]
        situacao_classe = sit_dict["classe"]
    else:
        situacao_geral = "--"
        situacao_classe = ""

    MESES = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    mes_nome = MESES[datetime.now().month - 1].upper()

    contexto = {
        "aluno":                 aluno,
        "nome_exibicao":         get_nome_exibicao(request.user),
        "foto_perfil_url":       get_foto_perfil(request.user),
        "agora":                 datetime.now(),
        "mes_nome":              mes_nome,
        "calendario":            gerar_calendario(aluno.turma.ano, datetime.now().month),
        "grade_horario":         grade,
        "disciplinas_com_notas": disciplinas_com_notas,
        "media_geral":           media_geral,
        "situacao_geral":        situacao_geral,
        "situacao_classe":       situacao_classe,
        "total_notas_lancadas":  total_notas_lancadas,
        "total_notas_possiveis": total_notas_possiveis,
    }

    return render(request, "aluno/painel_aluno.html", contexto)


@login_required
def painel_usuarios(request):
    """Redirecionador para os painéis específicos."""
    from ..utils.perfis import redirect_user
    return render(request, "core/usuarios.html", {
        "nome_exibicao":     get_nome_exibicao(request.user),
        "foto_perfil_url":   get_foto_perfil(request.user),
    })
