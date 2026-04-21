import csv
import datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.db.models import Avg, Count, Q, Case, When, FloatField, F, Value, ExpressionWrapper, DecimalField
from django.db.models.functions import Coalesce

from apps.academico.models.academico import Turma, Disciplina
from apps.academico.models.desempenho import Nota
from apps.usuarios.models.perfis import Aluno
from apps.saude.models.ficha_medica import FichaMedica
from apps.usuarios.utils.perfis import is_super_ou_gestor, get_nome_exibicao, get_foto_perfil
from apps.biblioteca.models.biblioteca import Emprestimo
from apps.dashboards.utils.pdf_engine import RelatorioMasterPDF

@login_required
@user_passes_test(is_super_ou_gestor)
def dashboard_saude_inclusao(request):
    """Painel analítico focado em acessibilidade, inclusão e saúde dos alunos."""
    total_alunos = Aluno.objects.count()
    total_pcd = Aluno.objects.filter(possui_necessidade_especial=True).count()
    
    # Alunos com alergias (vê se o campo não está vazio)
    fichas_com_alergia = FichaMedica.objects.exclude(alergias__isnull=True).exclude(alergias="")
    total_alergias = fichas_com_alergia.count()
    
    # Detalhes das alergias para a lista de alertas
    alertas_criticos = []
    for f in fichas_com_alergia.select_related('aluno')[:15]:
        alertas_criticos.append({
            'aluno': f.aluno.nome_completo,
            'alergia': f.alergias,
            'medicamento': f.medicamentos_continuos or "N/A"
        })

    # Distribuição Sanguínea
    sanguineo_qs = FichaMedica.objects.values('tipo_sanguineo').annotate(total=Count('id'))
    sanguineo_labels = [row['tipo_sanguineo'] or 'N/A' for row in sanguineo_qs]
    sanguineo_data = [row['total'] for row in sanguineo_qs]

    import json
    contexto = {
        'stats': {
            'total': total_alunos,
            'pcd': total_pcd,
            'alergias': total_alergias,
            'percentual_pcd': round((total_pcd / total_alunos * 100), 1) if total_alunos > 0 else 0
        },
        'alertas_criticos': alertas_criticos,
        'sanguineo_labels': json.dumps(sanguineo_labels),
        'sanguineo_data': json.dumps(sanguineo_data),
        'nome_exibicao': get_nome_exibicao(request.user),
        'foto_perfil_url': get_foto_perfil(request.user),
    }
    return render(request, 'dashboards/dashboard_inclusao.html', contexto)

@login_required
def dashboard_bi_academico(request):
    """Painel de Business Intelligence Macro com Preditivo de Evasão e Gráficos."""
    ano_atual = datetime.datetime.now().year
    
    # 1. Performance de Turmas Base
    calc_media_disc = ExpressionWrapper(
        (Coalesce(F('alunos__notas__nota1'), Value(0.0)) + 
         Coalesce(F('alunos__notas__nota2'), Value(0.0)) + 
         Coalesce(F('alunos__notas__nota3'), Value(0.0)) + 
         Coalesce(F('alunos__notas__nota4'), Value(0.0))) / 4.0,
        output_field=FloatField()
    )

    dados_turmas = Turma.objects.filter(ano=ano_atual).annotate(
        media_geral=Avg(calc_media_disc),
        total_freq=Count('alunos__frequencias'),
        taxa_frequencia=Case(
            When(total_freq__gt=0, then=100.0 * Count('alunos__frequencias', filter=Q(alunos__frequencias__presente=True)) / F('total_freq')),
            default=Value(100.0),
            output_field=FloatField()
        )
    ).values('nome', 'media_geral', 'taxa_frequencia', 'turno')

    # 2. Preditivo de Evasão
    calc_media_aluno = ExpressionWrapper(
        (Coalesce(F('notas__nota1'), Value(0.0)) + 
         Coalesce(F('notas__nota2'), Value(0.0)) + 
         Coalesce(F('notas__nota3'), Value(0.0)) + 
         Coalesce(F('notas__nota4'), Value(0.0))) / 4.0,
        output_field=FloatField()
    )

    alunos = Aluno.objects.annotate(
        avg_nota=Coalesce(Avg(calc_media_aluno), Value(0.0)),
        tot_freq=Count('frequencias'),
        taxa_freq=Case(
            When(tot_freq__gt=0, then=100.0 * Count('frequencias', filter=Q(frequencias__presente=True)) / F('tot_freq')),
            default=Value(100.0),
            output_field=FloatField()
        )
    )

    alunos_em_risco = alunos.filter(Q(taxa_freq__lt=75) | (Q(avg_nota__lt=5.0) & Q(avg_nota__gt=0)))
    total_risco = alunos_em_risco.count()
    total_saudaveis = alunos.count() - total_risco

    # 3. Fluxo Demográfico e Extras
    demografia_turnos = list(Aluno.objects.values('turma__turno').annotate(total=Count('id')))
    livros_circulacao = Emprestimo.objects.filter(data_devolucao_real__isnull=True).count()
    livros_atrasados  = Emprestimo.objects.filter(status='ATRASADO').count()
    alunos_pcd = Aluno.objects.filter(possui_necessidade_especial=True).count()

    # 4. Status de Matrícula (campo real no model)
    STATUS_MAP = {
        "ATIVO": "Ativos", "INATIVO": "Inativos",
        "EVADIDO": "Evadidos", "TRANSFERIDO": "Transferidos", "FORMADO": "Formados",
    }
    status_qs   = Aluno.objects.values("status_matricula").annotate(total=Count("id"))
    status_dict = {row["status_matricula"]: row["total"] for row in status_qs if row["status_matricula"]}
    bi_status_labels = list(STATUS_MAP.values())
    bi_status_data   = [status_dict.get(k, 0) for k in STATUS_MAP]

    # 5. Evolução de Matrículas por Ano (últimos 5 anos)
    alunos_com_ano = Aluno.objects.exclude(turma__ano__isnull=True)
    todos_anos = sorted(set(alunos_com_ano.values_list("turma__ano", flat=True).distinct()))[-5:]
    bi_evolucao_labels = [str(a) for a in todos_anos]
    bi_evolucao_data   = [Aluno.objects.filter(turma__ano=a).count() for a in todos_anos]

    import json
    contexto = {
        'dados_turmas': json.dumps(list(dados_turmas)),
        'ano_referencia': ano_atual,
        'risco_evasao': {
            'critico': total_risco,
            'saudavel': total_saudaveis,
            'lista_criticos': alunos_em_risco[:10]
        },
        'demografia_turnos': json.dumps(demografia_turnos),
        'extra_saude': alunos_pcd,
        'extra_biblioteca': json.dumps({'ativo': livros_circulacao, 'atrasado': livros_atrasados}),
        # Novos dados BI de status de matrícula
        'bi_status_labels': json.dumps(bi_status_labels),
        'bi_status_data':   json.dumps(bi_status_data),
        'bi_evolucao_labels': json.dumps(bi_evolucao_labels),
        'bi_evolucao_data':   json.dumps(bi_evolucao_data),
    }
    return render(request, 'dashboards/bi_academico.html', contexto)


@login_required
def exportar_notas_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="notas_sige.csv"'
    writer = csv.writer(response)
    writer.writerow(['Aluno', 'Turma', 'Disciplina', 'Nota 1', 'Nota 2', 'Nota 3', 'Nota 4', 'Média'])
    
    notas = Nota.objects.all().select_related('aluno', 'disciplina', 'aluno__turma')
    for n in notas:
        writer.writerow([n.aluno.nome_completo, n.aluno.turma.nome, n.disciplina.nome, n.nota1, n.nota2, n.nota3, n.nota4, n.media])
    return response

@login_required
def exportar_relatorio_evasao(request):
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="risco_evasao_sige.csv"'
    calc_media_aluno = ExpressionWrapper(
        (Coalesce(F('notas__nota1'), Value(0.0)) + Coalesce(F('notas__nota2'), Value(0.0)) + Coalesce(F('notas__nota3'), Value(0.0)) + Coalesce(F('notas__nota4'), Value(0.0))) / 4.0,
        output_field=FloatField()
    )
    alunos = Aluno.objects.annotate(
        avg_nota=Coalesce(Avg(calc_media_aluno), Value(0.0)),
        tot_freq=Count('frequencias'),
        taxa_freq=Case(
            When(tot_freq__gt=0, then=100.0 * Count('frequencias', filter=Q(frequencias__presente=True)) / F('tot_freq')),
            default=Value(100.0), output_field=FloatField()
        )
    ).filter(Q(taxa_freq__lt=75) | (Q(avg_nota__lt=5.0) & Q(avg_nota__gt=0)))

    writer = csv.writer(response)
    writer.writerow(['Nome do Aluno', 'Turma', 'Turno', 'Contato', 'Taxa de Frequencia Global', 'Media Geral'])
    for al in alunos:
        writer.writerow([al.nome_completo, al.turma.nome, al.turma.get_turno_display(), "(XX) 9XXXX-XXXX", f"{al.taxa_freq:.2f}%" if al.taxa_freq else "0%", f"{al.avg_nota:.2f}" if al.avg_nota else "0.00"])
    return response

@login_required
def exportar_master_pdf(request):
    """Gera Documento PDF corporativo timbrado com estatísticas mastigadas da escola inteira."""
    
    calc_media_aluno = ExpressionWrapper(
        (Coalesce(F('notas__nota1'), Value(0.0)) + Coalesce(F('notas__nota2'), Value(0.0)) + Coalesce(F('notas__nota3'), Value(0.0)) + Coalesce(F('notas__nota4'), Value(0.0))) / 4.0,
        output_field=FloatField()
    )

    alunos = Aluno.objects.annotate(
        avg_nota=Coalesce(Avg(calc_media_aluno), Value(0.0)),
        tot_freq=Count('frequencias'),
        taxa_freq=Case(
            When(tot_freq__gt=0, then=100.0 * Count('frequencias', filter=Q(frequencias__presente=True)) / F('tot_freq')),
            default=Value(100.0),
            output_field=FloatField()
        )
    )

    evasao = alunos.filter(Q(taxa_freq__lt=75) | (Q(avg_nota__lt=5.0) & Q(avg_nota__gt=0))).order_by('avg_nota')
    
    metricas = {
        'total_alunos': alunos.count(),
        'total_risco': evasao.count(),
        'livros_ativos': Emprestimo.objects.filter(data_devolucao_real__isnull=True).count(),
        'lista_evasao': list(evasao)
    }

    motor = RelatorioMasterPDF(titulo_relatorio="DOSSIÊ GLOBAL DA GESTÃO")
    buffer = motor.gerar_pdf(metricas)

    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="sige_dossie_global.pdf"'
    return response
