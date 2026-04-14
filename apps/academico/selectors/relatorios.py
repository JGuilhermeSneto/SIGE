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
    """Calcula estatísticas de aprovação, conselho e recuperação."""
    # Nota: No SIGE, a média é calculada per disciplina. 
    # Para o relatório geral, vamos considerar a média das médias do aluno.
    
    notas = Nota.objects.filter(disciplina__turma__ano=ano)
    
    aprovados = 0
    reprovados = 0
    conselho = 0
    recuperacao = 0
    
    # Agrupar por aluno para ter uma visão do "estudante" e não apenas da "nota disciplina"
    alunos = Aluno.objects.filter(turma__ano=ano)
    
    for aluno in alunos:
        notas_aluno = Nota.objects.filter(aluno=aluno)
        if not notas_aluno.exists():
            continue
            
        medias = [float(n.media) for n in notas_aluno if n.media is not None]
        if not medias:
            continue
            
        media_geral = sum(medias) / len(medias)
        
        # Lógica definida pelo usuário:
        # > 6.0 Aprovado
        # 4.9 a 5.9 Conselho
        # < 4.9 Reprovado
        
        if media_geral >= 6.0:
            aprovados += 1
        elif 4.9 <= media_geral <= 5.9:
            conselho += 1
        elif media_geral < 4.9:
            reprovados += 1
        else:
            recuperacao += 1 # Caso genérico se as faixas não cobrirem tudo
            
    return {
        "aprovados": aprovados,
        "reprovados": reprovados,
        "conselho": conselho,
        "recuperacao": recuperacao,
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
