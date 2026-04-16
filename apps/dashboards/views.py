from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.academico.models.academico import Turma, Disciplina
from apps.academico.models.desempenho import Nota
from django.db.models import Avg
import csv
from django.http import HttpResponse

import datetime
from django.db.models import Avg, Count, Q, Case, When, FloatField, F, Value, ExpressionWrapper, DecimalField
from django.db.models.functions import Coalesce

@login_required
def dashboard_bi_academico(request):
    """Painel de Business Intelligence Acadêmico com indicadores reais."""
    ano_atual = datetime.datetime.now().year
    
    # Cálculo da média por disciplina no banco com tipos seguros
    calc_media_disc = ExpressionWrapper(
        (Coalesce(F('alunos__notas__nota1'), Value(0.0)) + 
         Coalesce(F('alunos__notas__nota2'), Value(0.0)) + 
         Coalesce(F('alunos__notas__nota3'), Value(0.0)) + 
         Coalesce(F('alunos__notas__nota4'), Value(0.0))) / 4.0,
        output_field=DecimalField(max_digits=5, decimal_places=2)
    )

    # Média de notas e Taxa de Frequência por turma
    dados_turmas = Turma.objects.filter(ano=ano_atual).annotate(
        media_geral=Avg(calc_media_disc),
        total_freq=Count('alunos__frequencias'),
        presencas=Count('alunos__frequencias', filter=Q(alunos__frequencias__presente=True))
    ).annotate(
        taxa_frequencia=Case(
            When(total_freq__gt=0, then=100.0 * Count('alunos__frequencias', filter=Q(alunos__frequencias__presente=True)) / Count('alunos__frequencias')),
            default=100.0,
            output_field=FloatField()
        )
    ).values('nome', 'media_geral', 'taxa_frequencia')

    contexto = {
        'dados_turmas': list(dados_turmas),
        'ano_referencia': ano_atual
    }
    return render(request, 'dashboards/bi_academico.html', contexto)

@login_required
def exportar_notas_csv(request):
    """Exporta todas as notas registradas para CSV."""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="notas_sige.csv"'

    writer = csv.writer(response)
    writer.writerow(['Aluno', 'Turma', 'Disciplina', 'Nota 1', 'Nota 2', 'Nota 3', 'Nota 4', 'Média'])

    notas = Nota.objects.all().select_related('aluno', 'disciplina', 'aluno__turma')
    for n in notas:
        writer.writerow([
            n.aluno.nome_completo,
            n.aluno.turma.nome,
            n.disciplina.nome,
            n.nota1, n.nota2, n.nota3, n.nota4,
            n.media
        ])

    return response
