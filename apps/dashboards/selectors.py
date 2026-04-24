"""
Camada de Selectors para o BI Executivo (Estilo SIGEDUC/SUAP).
Focado em alta performance (agregações ORM) e dados limpos.
"""

from django.db.models import Avg, Count, Q, F, Case, When, Value, FloatField, ExpressionWrapper
from django.db.models.functions import Coalesce
from apps.academico.models.academico import Turma, Disciplina, AtividadeProfessor, PlanejamentoAula, EntregaAtividade
from apps.academico.models.desempenho import Nota
from apps.usuarios.models.perfis import Aluno, Professor

def get_distribuicao_notas(ano):
    """Retorna contagem de alunos por faixas de notas (Histograma)."""
    calc_media = ExpressionWrapper(
        (Coalesce(F('nota1'), Value(0.0)) + Coalesce(F('nota2'), Value(0.0)) + 
         Coalesce(F('nota3'), Value(0.0)) + Coalesce(F('nota4'), Value(0.0))) / 4.0,
        output_field=FloatField()
    )
    
    stats = Nota.objects.filter(disciplina__turma__ano=ano).annotate(
        media_nota=calc_media
    ).aggregate(
        critico=Count(Case(When(media_nota__lt=5.0, then=1))),
        regular=Count(Case(When(media_nota__gte=5.0, media_nota__lt=7.0, then=1))),
        excelente=Count(Case(When(media_nota__gte=7.0, then=1))),
    )
    return stats

def get_materias_criticas(ano):
    """Identifica as 5 disciplinas com menor média de notas."""
    calc_media = ExpressionWrapper(
        (Coalesce(F('notas__nota1'), Value(0.0)) + Coalesce(F('notas__nota2'), Value(0.0)) + 
         Coalesce(F('notas__nota3'), Value(0.0)) + Coalesce(F('notas__nota4'), Value(0.0))) / 4.0,
        output_field=FloatField()
    )
    
    return Disciplina.objects.filter(turma__ano=ano).annotate(
        media_geral=Avg(calc_media)
    ).order_by('media_geral')[:5]

def get_status_diarios(ano):
    """Métrica de Eficiência: % de aulas planejadas que foram concluídas."""
    total = PlanejamentoAula.objects.filter(turma__ano=ano).count()
    concluidos = PlanejamentoAula.objects.filter(turma__ano=ano, concluido=True).count()
    
    if total == 0: return 100
    return round((concluidos / total) * 100, 1)

def get_engajamento_atividades(ano):
    """Métrica de Engajamento: % de entrega de atividades pelos alunos."""
    atividades = AtividadeProfessor.objects.filter(disciplina__turma__ano=ano)
    total_alunos = Aluno.objects.filter(turma__ano=ano).count()
    
    if not atividades.exists() or total_alunos == 0:
        return 0
        
    total_esperado = atividades.count() * total_alunos
    total_entregue = EntregaAtividade.objects.filter(atividade__in=atividades).count()
    
    return round((total_entregue / total_esperado * 100), 1) if total_esperado > 0 else 0

def get_metricas_professores():
    """Retorna workload e métricas de professores."""
    return Professor.objects.annotate(
        total_disciplinas=Count('disciplinas'),
        total_alunos=Count('disciplinas__turma__alunos', distinct=True)
    ).order_by('-total_disciplinas')
