"""
Relatórios consolidados e exportação (ex.: histórico em PDF com ReportLab).

O que é: painel para gestor/superusuário e endpoints AJAX de busca;
delega agregações a ``selectors.relatorios``.
"""

import datetime
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from ..selectors import relatorios as selectors_rel
from apps.usuarios.utils.perfis import is_super_ou_gestor

# ReportLab para geração de PDF
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm

@login_required
@user_passes_test(is_super_ou_gestor)
def painel_relatorios(request):
    """View principal do dashboard de relatórios."""
    ano_atual = datetime.datetime.now().year
    ano_filtro = request.GET.get('ano', ano_atual)
    mes_filtro = request.GET.get('mes')
    
    contexto = {
        "metricas": selectors_rel.get_metricas_gerais(ano=ano_filtro, mes=mes_filtro),
        "desempenho": selectors_rel.get_performance_academica(ano=ano_filtro),
        "ano_filtro": int(ano_filtro),
        "mes_filtro": int(mes_filtro) if mes_filtro else None,
        "anos_disponiveis": range(ano_atual - 5, ano_atual + 1),
        "meses_disponiveis": [
            (1, "Janeiro"), (2, "Fevereiro"), (3, "Março"), (4, "Abril"),
            (5, "Maio"), (6, "Junho"), (7, "Julho"), (8, "Agosto"),
            (9, "Setembro"), (10, "Outubro"), (11, "Novembro"), (12, "Dezembro")
        ]
    }
    
    return render(request, "relatorios/painel_relatorios.html", contexto)

@login_required
@user_passes_test(is_super_ou_gestor)
def exportar_historico_pdf(request, aluno_id):
    """Gera o Histórico Escolar em formato PDF."""
    dados = selectors_rel.get_dados_historico(aluno_id)
    if not dados:
        return HttpResponse("Aluno não encontrado", status=404)
        
    aluno = dados['aluno']
    historico = dados['historico']
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="historico_{aluno.cpf}.pdf"'
    
    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    
    # --- Cabeçalho ---
    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(width/2, height - 2*cm, "SIGE - SISTEMA INTEGRADO DE GESTÃO ESCOLAR")
    p.setFont("Helvetica", 12)
    p.drawCentredString(width/2, height - 2.8*cm, "HISTÓRICO ESCOLAR OFICIAL")
    
    p.line(1*cm, height - 3.5*cm, width - 1*cm, height - 3.5*cm)
    
    # --- Dados do Aluno ---
    p.setFont("Helvetica-Bold", 10)
    p.drawString(1*cm, height - 4.2*cm, f"NOME: {aluno.nome_completo.upper()}")
    p.drawString(1*cm, height - 4.7*cm, f"CPF: {aluno.cpf}")
    p.drawString(10*cm, height - 4.7*cm, f"DATA NASC.: {aluno.data_nascimento.strftime('%d/%m/%Y') if aluno.data_nascimento else 'N/A'}")
    p.drawString(1*cm, height - 5.2*cm, f"TURMA ATUAL: {aluno.turma.nome} ({aluno.turma.get_turno_display()})")
    
    p.line(1*cm, height - 5.7*cm, width - 1*cm, height - 5.7*cm)
    
    # --- Tabela de Notas ---
    p.setFont("Helvetica-Bold", 10)
    headers = ["ANO", "DISCIPLINA", "N1", "N2", "N3", "N4", "MÉDIA", "FREQ. %"]
    x_offsets = [1*cm, 2.5*cm, 7.5*cm, 8.5*cm, 9.5*cm, 10.5*cm, 11.5*cm, 13.5*cm]
    
    y = height - 6.5*cm
    for i, header in enumerate(headers):
        p.drawString(x_offsets[i], y, header)
        
    p.setFont("Helvetica", 9)
    y -= 0.6*cm
    
    for item in historico:
        if y < 2*cm: # Nova página se necessário (simplificado)
            p.showPage()
            y = height - 2*cm
            p.setFont("Helvetica", 9)
            
        p.drawString(x_offsets[0], y, str(item['ano']))
        p.drawString(x_offsets[1], y, item['disciplina'][:30])
        p.drawString(x_offsets[2], y, f"{item['n1']:.1f}" if item['n1'] is not None else "-")
        p.drawString(x_offsets[3], y, f"{item['n2']:.1f}" if item['n2'] is not None else "-")
        p.drawString(x_offsets[4], y, f"{item['n3']:.1f}" if item['n3'] is not None else "-")
        p.drawString(x_offsets[5], y, f"{item['n4']:.1f}" if item['n4'] is not None else "-")
        
        media = item['media']
        p.setFont("Helvetica-Bold", 9)
        p.drawString(x_offsets[6], y, f"{media:.1f}" if media is not None else "-")
        p.setFont("Helvetica", 9)
        
        p.drawString(x_offsets[7], y, f"{item['frequencia']:.1f}%")
        y -= 0.5*cm
        p.line(1*cm, y+0.2*cm, width - 1*cm, y+0.2*cm)
        y -= 0.3*cm
        
    # --- Rodapé ---
    p.setFont("Helvetica-Oblique", 8)
    p.drawString(1*cm, 1*cm, f"Gerado em: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}")
    p.drawRightString(width - 1*cm, 1*cm, "Assinatura da Direção / Secretaria")
    
    p.showPage()
    p.save()
    
    return response

@login_required
@user_passes_test(is_super_ou_gestor)
def buscar_alunos_ajax(request):
    """API para busca dinâmica de alunos para o dashboard de relatórios."""
    from django.http import JsonResponse
    from django.db.models import Q
    from apps.usuarios.models.perfis import Aluno
    from django.urls import reverse

    query = request.GET.get('q', '').strip()
    if len(query) < 3:
        return JsonResponse({"results": []})

    alunos = Aluno.objects.filter(
        Q(nome_completo__icontains=query) | Q(cpf__icontains=query)
    ).select_related('turma')[:10]  # Limite de 10 resultados para performance

    results = []
    for a in alunos:
        results.append({
            "id": a.id,
            "nome": a.nome_completo,
            "cpf": a.cpf,
            "turma": a.turma.nome,
            "url_pdf": reverse('exportar_historico', args=[a.id])
        })

    return JsonResponse({"results": results})

@login_required
def visualizar_historico(request, aluno_id=None):
    """View para visualizar o histórico escolar em HTML (Premium)."""
    # Se aluno_id não for passado, tenta pegar o do usuário logado (se for aluno)
    if aluno_id is None:
        if hasattr(request.user, 'aluno'):
            aluno_id = request.user.aluno.id
        else:
            return HttpResponse("ID do aluno não fornecido.", status=400)
    
    # Segurança: Alunos só veem o próprio histórico
    if hasattr(request.user, 'aluno') and request.user.aluno.id != int(aluno_id):
        if not is_super_ou_gestor(request.user):
            return HttpResponse("Acesso negado.", status=403)

    dados = selectors_rel.get_dados_historico(aluno_id)
    if not dados:
        return HttpResponse("Histórico não encontrado.", status=404)

    return render(request, "relatorios/historico_escolar.html", dados)
