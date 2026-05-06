from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Q
from django.utils import timezone

from ...utils.perfis import get_nome_exibicao, get_foto_perfil
from apps.academico.utils.interface_usuario import gerar_calendario
from apps.academico.utils.filtros import _get_anos_filtro
from apps.academico.models.academico import Turma, Disciplina
from apps.comunicacao.models.comunicado import Comunicado

@login_required
def painel_professor(request):
    """Dashboard principal para Professores."""
    professor = getattr(request.user, 'professor', None)
    if not professor:
        return render(request, "core/sem_perfil.html")

    hoje = datetime.now()
    ano_atual = hoje.year
    
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

    disciplinas = Disciplina.objects.filter(
        professor=professor, 
        turma__ano=ano_filtro
    ).select_related("turma")
    
    turmas_ids = disciplinas.values_list("turma_id", flat=True).distinct()
    
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
        "calendario":              gerar_calendario(ano_atual, hoje.month, user=request.user),
        "ano_calendario":          ano_atual,
        "total_turmas":            turmas_ids.count(),
        "total_alunos":            total_alunos_unicos,
        "total_disciplinas":       disciplinas.count(),
        "total_notas_lancadas":    total_lancadas,
        "total_notas_possiveis":   total_possiveis,
        "anos_disponiveis":        anos_disponiveis,
        "ano_filtro":              ano_filtro,
        "comunicados": Comunicado.objects.filter(
            Q(publico_alvo__in=['GLOBAL', 'PROFESSORES']),
            Q(data_expiracao__gte=timezone.now().date()) | Q(data_expiracao__isnull=True)
        )[:5],
    }
    
    from apps.biblioteca.models.biblioteca import Emprestimo
    contexto["meus_emprestimos"] = Emprestimo.objects.filter(
        usuario_professor=professor
    ).exclude(status='DEVOLVIDO').select_related('livro').order_by('-data_emprestimo')
    
    contexto["livros_devolvidos"] = Emprestimo.objects.filter(
        usuario_professor=professor, 
        status='DEVOLVIDO'
    ).select_related('livro').order_by('-data_devolucao_real')[:10]

    return render(request, "professor/painel_professor.html", contexto)
