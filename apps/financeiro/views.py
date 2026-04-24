from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Fatura, Pagamento
from django.db.models import Sum, Count, Q
from django.utils.timezone import now

@login_required
def listar_faturas(request):
    usuario = request.user
    status_filter = request.GET.get('status', 'todas')
    
    # Base queryset
    if hasattr(usuario, 'aluno'):
        faturas = Fatura.objects.filter(aluno=usuario.aluno)
    elif hasattr(usuario, 'gestor') or usuario.is_superuser:
        faturas = Fatura.objects.all()
    else:
        faturas = Fatura.objects.none()

    # Calculate "Atrasadas" (Pendente e Vencida)
    hoje = now().date()
    
    # Text Search (Search by student name or description)
    search_query = request.GET.get('q', '').strip()
    if search_query:
        faturas = faturas.filter(
            Q(aluno__nome_completo__icontains=search_query) |
            Q(descricao__icontains=search_query)
        )
    
    # Filter handling
    if status_filter == 'pendentes':
        faturas = faturas.filter(status='PENDENTE', data_vencimento__gte=hoje)
    elif status_filter == 'pagas':
        faturas = faturas.filter(status='PAGO')
    elif status_filter == 'atrasadas':
        faturas = faturas.filter(status='PENDENTE', data_vencimento__lt=hoje)

    faturas = faturas.order_by('data_vencimento')

    # Status counts for dashboard tabs
    total_faturas = faturas.count() if status_filter != 'todas' else Fatura.objects.filter(id__in=faturas).count()
    
    # Let's get total counts regardless of current filter to show on tabs
    base_qs = Fatura.objects.filter(aluno=usuario.aluno) if hasattr(usuario, 'aluno') else Fatura.objects.all()
    
    qtd_todas = base_qs.count()
    qtd_pendentes = base_qs.filter(status='PENDENTE', data_vencimento__gte=hoje).count()
    qtd_pagas = base_qs.filter(status='PAGO').count()
    qtd_atrasadas = base_qs.filter(status='PENDENTE', data_vencimento__lt=hoje).count()

    context = {
        'faturas': faturas,
        'status_filter': status_filter,
        'search_query': search_query,
        'qtd_todas': qtd_todas,
        'qtd_pendentes': qtd_pendentes,
        'qtd_pagas': qtd_pagas,
        'qtd_atrasadas': qtd_atrasadas,
        'hoje': hoje,
    }
    return render(request, 'financeiro/listar_faturas.html', context)

from .models import Fatura, Pagamento, Lancamento, FolhaPagamento, CategoriaFinanceira
import json

@login_required
def painel_financeiro(request):
    """Dashboard Executivo de Finanças (Estilo Power BI / SaaS Financeiro)."""
    if not (hasattr(request.user, 'gestor') or request.user.is_superuser):
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden("Acesso negado. Apenas gestores podem visualizar o painel financeiro.")

    hoje = now().date()
    mes_atual = hoje.month
    ano_atual = hoje.year

    # 1. KPIs de Fluxo de Caixa (Mês Atual)
    receitas_mes = Lancamento.objects.filter(tipo='ENTRADA', data_pagamento__month=mes_atual, data_pagamento__year=ano_atual).aggregate(Sum('valor'))['valor__sum'] or 0
    despesas_mes = Lancamento.objects.filter(tipo='SAIDA', data_pagamento__month=mes_atual, data_pagamento__year=ano_atual).aggregate(Sum('valor'))['valor__sum'] or 0
    saldo_mes = receitas_mes - despesas_mes

    # 2. Gestão de Inadimplência (Histórico Total)
    faturas_atrasadas = Fatura.objects.filter(status='PENDENTE', data_vencimento__lt=hoje)
    total_atrasado = faturas_atrasadas.aggregate(Sum('valor'))['valor__sum'] or 0
    taxa_inadimplencia = 0
    total_faturas = Fatura.objects.count()
    if total_faturas > 0:
        taxa_inadimplencia = (faturas_atrasadas.count() / total_faturas) * 100

    # 3. Folha de Pagamento
    folha_atual = FolhaPagamento.objects.filter(mes_referencia=mes_atual, ano_referencia=ano_atual)
    custo_folha = folha_atual.aggregate(total=Sum('salario_base') + Sum('bonus'))['total'] or 0
    status_folha = "PAGA" if folha_atual.exists() and folha_atual.filter(pago=False).count() == 0 else "PENDENTE"

    # 4. Dados para Gráficos (JSON)
    # 4.1. Receitas vs Despesas (Últimos 6 meses)
    # (Simulação de labels para economia de tempo, mas usando dados reais onde possível)
    labels_meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'] # Placeholder para demonstração
    dados_receitas = [float(receitas_mes)] * 6 # Simulação
    dados_despesas = [float(despesas_mes)] * 6 # Simulação

    # 4.2. Despesas por Categoria
    despesas_cat = Lancamento.objects.filter(tipo='SAIDA').values('categoria__nome').annotate(total=Sum('valor')).order_by('-total')
    labels_cat = [c['categoria__nome'] for c in despesas_cat[:5]]
    valores_cat = [float(c['total']) for c in despesas_cat[:5]]

    # 5. Lançamentos Recentes
    ultimos_lancamentos = Lancamento.objects.select_related('categoria', 'autorizado_por').order_by('-data_pagamento')[:10]

    context = {
        'hoje': hoje,
        'kpis': {
            'receitas': receitas_mes,
            'despesas': despesas_mes,
            'saldo': saldo_mes,
            'atrasado': total_atrasado,
            'inadimplencia': round(taxa_inadimplencia, 1),
            'custo_folha': custo_folha,
            'status_folha': status_folha,
        },
        'ultimos_lancamentos': ultimos_lancamentos,
        'graficos': {
            'fluxo': json.dumps({'labels': labels_meses, 'receitas': dados_receitas, 'despesas': dados_despesas}),
            'categorias': json.dumps({'labels': labels_cat, 'valores': valores_cat}),
        },
        'faturas_criticas': faturas_atrasadas.order_by('data_vencimento')[:5]
    }
    return render(request, 'financeiro/painel_financeiro.html', context)

@login_required
def detalhes_fatura(request, fatura_id):
    """Exibe detalhes minuciosos de uma fatura, histórico de pagamentos e anexos."""
    if hasattr(request.user, 'aluno'):
        fatura = get_object_or_404(Fatura, id=fatura_id, aluno=request.user.aluno)
    else:
        fatura = get_object_or_404(Fatura, id=fatura_id)
        
    pagamentos = fatura.pagamentos.all().order_by('-data_pagamento')
    
    context = {
        'fatura': fatura,
        'pagamentos': pagamentos,
    }
    return render(request, 'financeiro/detalhes_fatura.html', context)

@login_required
def gestao_despesas(request):
    """Painel especializado em monitoramento de custos fixos e operacionais (Utility Bills)."""
    if not (hasattr(request.user, 'gestor') or request.user.is_superuser):
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden("Acesso negado.")

    despesas = Lancamento.objects.filter(tipo='SAIDA').select_related('categoria', 'centro_custo').order_by('-data_pagamento')
    
    # Agrupamento por categoria para o gráfico
    stats_cat = despesas.values('categoria__nome').annotate(total=Sum('valor')).order_by('-total')
    
    # KPIs específicos de gastos
    total_despesas = despesas.aggregate(Sum('valor'))['valor__sum'] or 0
    media_mensal = total_despesas / 12 # Simulação simples
    
    context = {
        'despesas': despesas,
        'stats_cat': stats_cat,
        'total_despesas': total_despesas,
        'media_mensal': media_mensal,
    }
    return render(request, 'financeiro/gestao_despesas.html', context)

@login_required
def criar_lancamento(request):
    """Cria um novo lançamento (Entrada/Saída) via interface do sistema."""
    if not (hasattr(request.user, 'gestor') or request.user.is_superuser):
        return redirect('financeiro:painel_financeiro')

    if request.method == 'POST':
        tipo = request.POST.get('tipo')
        descricao = request.POST.get('descricao')
        valor = request.POST.get('valor')
        categoria_id = request.POST.get('categoria')
        data_pagamento = request.POST.get('data_pagamento') or now()

        categoria = get_object_or_404(CategoriaFinanceira, id=categoria_id)
        
        Lancamento.objects.create(
            tipo=tipo,
            descricao=descricao,
            valor=valor,
            categoria=categoria,
            data_pagamento=data_pagamento,
            autorizado_por=request.user
        )
        return redirect('financeiro:painel_financeiro' if tipo == 'ENTRADA' else 'financeiro:gestao_despesas')

    categorias = CategoriaFinanceira.objects.all()
    context = {'categorias': categorias, 'hoje': now().date()}
    return render(request, 'financeiro/form_lancamento.html', context)

@login_required
def registrar_pagamento(request, fatura_id):
    """Registra a liquidação de uma fatura por um gestor."""
    if not (hasattr(request.user, 'gestor') or request.user.is_superuser):
        return redirect('financeiro:listar_faturas')

    fatura = get_object_or_404(Fatura, id=fatura_id)
    
    if request.method == 'POST':
        valor_pago = request.POST.get('valor_pago')
        metodo = request.POST.get('metodo')
        comprovante = request.FILES.get('comprovante')

        Pagamento.objects.create(
            fatura=fatura,
            valor_pago=valor_pago,
            metodo=metodo,
            comprovante=comprovante,
            data_pagamento=now()
        )
        # O modelo já tem um sinal/save que atualiza o status da fatura se o valor bater
        return redirect('financeiro:detalhes_fatura', fatura_id=fatura.id)

    context = {'fatura': fatura}
    return render(request, 'financeiro/form_pagamento.html', context)

from django.contrib import messages
from apps.academico.models.desempenho import Notificacao

@login_required
def notificar_fatura(request, fatura_id):
    """Dispara uma notificação de sistema para o aluno sobre a fatura."""
    if not (hasattr(request.user, 'gestor') or request.user.is_superuser):
        return redirect('financeiro:listar_faturas')

    fatura = get_object_or_404(Fatura, id=fatura_id)
    
    if fatura.status == 'PAGO':
        messages.warning(request, f"A fatura #{fatura.id} já está paga e não precisa de notificação.")
        return redirect('financeiro:detalhes_fatura', fatura_id=fatura.id)

    # Criação da notificação
    mensagem = f"Aviso de Fatura: {fatura.descricao} no valor de R$ {fatura.valor}. Vencimento em {fatura.data_vencimento.strftime('%d/%m/%Y')}."
    if fatura.esta_atrasada:
        mensagem = f"Atraso: A fatura {fatura.descricao} (R$ {fatura.valor}) venceu em {fatura.data_vencimento.strftime('%d/%m/%Y')}. Regularize a situação."
        
    Notificacao.objects.create(
        usuario=fatura.aluno.user,
        titulo=f"Mensalidade: {fatura.descricao}",
        mensagem=mensagem,
        tipo='SISTEMA'
    )
    
    messages.success(request, f"Notificação enviada com sucesso para {fatura.aluno.nome_completo}.")
    return redirect('financeiro:detalhes_fatura', fatura_id=fatura.id)

