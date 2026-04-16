"""
Consultas complexas só leitura para relatórios (métricas, agregações ORM).

O que é: camada “selector” para manter views finas e SQL/ORM reutilizável.
"""

from django.db.models import Count, Q, Avg, F
from django.utils import timezone
from apps.usuarios.models.perfis import Aluno, Professor, Gestor
from ..models.academico import Turma, Disciplina
from ..models.desempenho import Nota, Frequencia
from django.contrib.auth import get_user_model

User = get_user_model()

def get_metricas_gerais(ano=None, mes=None):
    """Retorna métricas básicas para o dashboard de relatórios."""
    hoje = timezone.now()
    ano = int(ano) if ano else hoje.year
    
    # Filtro base por ano/mês para ingressantes
    filtro_data = Q(criado_em__year=ano)
    if mes:
        filtro_data &= Q(criado_em__month=mes)

    metricas = {
        "total_alunos": Aluno.objects.count(),
        "total_turmas": Turma.objects.filter(ano=ano).count(),
        "total_disciplinas": Disciplina.objects.filter(turma__ano=ano).count(),
        "usuarios_ativos": User.objects.filter(is_active=True).count(),
        "usuarios_inativos": User.objects.filter(is_active=False).count(),
        "ingressantes": Aluno.objects.filter(filtro_data).count(),
    }
    
    # Concluintes (Baseado no nome da turma seguindo o padrão informado pelo usuário)
    # Procuramos por "9" ou "3" que geralmente indicam o ano final
    metricas["concluintes"] = Aluno.objects.filter(
        Q(turma__nome__icontains="9") | Q(turma__nome__icontains="3º"),
        turma__ano=ano
    ).count()
    
    return metricas

def get_performance_academica(ano):
    """Calcula estatísticas de aprovação, conselho e recuperação usando agregação ORM."""
    
    # 1. Filtramos alunos do ano solicitado
    # 2. Anotamos cada aluno com sua média geral (média das médias de cada disciplina)
    # 3. Contamos por categoria usando condicionais Case/When
    
    from django.db.models import Case, When, IntegerField, Value, Avg, Q, F, DecimalField, ExpressionWrapper
    from django.db.models.functions import Coalesce
    
    # Cálculo da média aritmética ponderada no banco com tipos consistentes
    calc_media = ExpressionWrapper(
        (Coalesce(F('notas__nota1'), Value(0.0)) + 
         Coalesce(F('notas__nota2'), Value(0.0)) + 
         Coalesce(F('notas__nota3'), Value(0.0)) + 
         Coalesce(F('notas__nota4'), Value(0.0))) / 4.0,
        output_field=DecimalField(max_digits=5, decimal_places=2)
    )

    perf_data = Aluno.objects.filter(turma__ano=ano).annotate(
        media_aluno=Avg(calc_media)
    ).aggregate(
        aprovados=Count(Case(When(media_aluno__gte=6.0, then=Value(1)), output_field=IntegerField())),
        conselho=Count(Case(When(media_aluno__range=(4.9, 5.9), then=Value(1)), output_field=IntegerField())),
        reprovados=Count(Case(When(media_aluno__lt=4.9, then=Value(1)), output_field=IntegerField())),
    )
    
    # Adicionamos uma lógica para recuperação (não previsto explicitamente no loop original mas pode ser útil)
    # Aqui vamos apenas retornar as chaves que o template espera
    return {
        "aprovados": perf_data['aprovados'] or 0,
        "reprovados": perf_data['reprovados'] or 0,
        "conselho": perf_data['conselho'] or 0,
        "recuperacao": 0, # Placeholder para compatibilidade
    }

def get_dados_historico(aluno_id):
    """Coleta todos os dados necessários para o PDF do Histórico Escolar."""
    try:
        aluno = Aluno.objects.select_related('turma').get(id=aluno_id)
        # Notas agrupadas por ano letivo
        notas = Nota.objects.filter(aluno=aluno).select_related('disciplina', 'disciplina__turma').order_by('disciplina__turma__ano', 'disciplina__nome')
        
        # Frequência consolidada por disciplina
        frequencias = Frequencia.objects.filter(aluno=aluno).values('disciplina').annotate(
            total=Count('id'),
            presencas=Count('id', filter=Q(presente=True))
        )
        
        freq_map = {f['disciplina']: (f['presencas']/f['total']*100 if f['total'] > 0 else 100) for f in frequencias}
        
        historico = []
        for n in notas:
            historico.append({
                "ano": n.disciplina.turma.ano,
                "disciplina": n.disciplina.nome,
                "n1": n.nota1,
                "n2": n.nota2,
                "n3": n.nota3,
                "n4": n.nota4,
                "media": n.media,
                "frequencia": freq_map.get(n.disciplina.id, 100)
            })
            
        return {
            "aluno": aluno,
            "historico": historico
        }
    except Aluno.DoesNotExist:
        return None
