from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import F, Count, Sum, Q
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models.patrimonio import ItemPatrimonio, ItemEstoque, MovimentacaoEstoque, SaldoEstoque
from .forms import ItemPatrimonioForm, MovimentacaoEstoqueForm
from apps.usuarios.utils.perfis import is_super_ou_gestor, get_nome_exibicao, get_foto_perfil

@login_required
@user_passes_test(is_super_ou_gestor)
def painel_infraestrutura(request):
    """Dashboard de Gestão de Infraestrutura (Patrimônio e Estoque)."""
    query = request.GET.get('q', '').strip()
    
    patrimonios = ItemPatrimonio.objects.all().select_related('categoria', 'unidade').order_by('-data_aquisicao')
    saldos_estoque = SaldoEstoque.objects.all().select_related('item', 'unidade').order_by('item__nome')
    
    if query:
        # Filtra patrimônios por nome ou tombamento
        from django.db.models import Q
        patrimonios = patrimonios.filter(Q(nome__icontains=query) | Q(tombamento__icontains=query))
        # Filtra saldos por nome do item
        saldos_estoque = saldos_estoque.filter(item__nome__icontains=query)
    
    # Métricas para o Dashboard Premium (Padrão SUAP/Financeiro)
    from django.db.models import Sum
    from .models.patrimonio import Ambiente, ManutencaoBem
    
    valor_total = patrimonios.aggregate(total=Sum('valor_aquisicao'))['total'] or 0
    manutencoes_abertas = ManutencaoBem.objects.filter(data_realizacao__isnull=True).count()
    total_ambientes = Ambiente.objects.count()
    
    metricas = {
        'total_patrimonio': patrimonios.count(),
        'valor_investido': valor_total,
        'manutencoes_pendentes': manutencoes_abertas,
        'total_ambientes': total_ambientes,
        'itens_criticos': saldos_estoque.filter(quantidade__lte=F('item__estoque_minimo')).count(),
        'total_itens_estoque': saldos_estoque.aggregate(total=Sum('quantidade'))['total'] or 0,
        'estado_bom': patrimonios.filter(estado_conservacao__in=['NOVO', 'BOM']).count(),
        'estado_regular': patrimonios.filter(estado_conservacao='REGULAR').count(),
        'estado_precario': patrimonios.filter(estado_conservacao__in=['DANIFICADO', 'INSERVIVEL']).count(),
    }

    # Dados para Gráficos de Infraestrutura
    import json
    dist_estado = {
        'labels': ['Novo/Bom', 'Regular', 'Danificado/Inservível'],
        'data': [
            patrimonios.filter(estado_conservacao__in=['NOVO', 'BOM']).count(),
            patrimonios.filter(estado_conservacao='REGULAR').count(),
            patrimonios.filter(estado_conservacao__in=['DANIFICADO', 'INSERVIVEL']).count()
        ]
    }
    
    # Categorias mais comuns
    categorias_qs = ItemPatrimonio.objects.values('categoria__nome').annotate(total=Count('id')).order_by('-total')[:5]
    dist_categorias = {
        'labels': [c['categoria__nome'] for c in categorias_qs],
        'data': [c['total'] for c in categorias_qs]
    }

    return render(request, 'infraestrutura/painel_infra.html', {
        'patrimonios': patrimonios,
        'saldos_estoque': saldos_estoque,
        'metricas': metricas,
        'dist_estado_json': json.dumps(dist_estado),
        'dist_categorias_json': json.dumps(dist_categorias),
        'nome_exibicao': get_nome_exibicao(request.user),
        'foto_perfil_url': get_foto_perfil(request.user),
    })

@login_required
@user_passes_test(is_super_ou_gestor)
def cadastrar_editar_patrimonio(request, pk=None):
    """Cria ou edita um item de patrimônio."""
    item = get_object_or_404(ItemPatrimonio, pk=pk) if pk else None
    if request.method == "POST":
        form = ItemPatrimonioForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Item de patrimônio salvo!")
            return redirect('painel_infraestrutura')
    else:
        form = ItemPatrimonioForm(instance=item)
        
    return render(request, 'infraestrutura/form_patrimonio.html', {
        'form': form,
        'editando': bool(pk),
        'nome_exibicao': get_nome_exibicao(request.user),
        'foto_perfil_url': get_foto_perfil(request.user),
    })

@login_required
@user_passes_test(is_super_ou_gestor)
def registrar_movimentacao_estoque(request):
    """Registra entrada ou saída de itens de consumo."""
    if request.method == "POST":
        form = MovimentacaoEstoqueForm(request.POST)
        if form.is_valid():
            mov = form.save()
            # Lógica manual de atualização de saldo (espelhando o que está no Admin para consistência)
            saldo, _ = SaldoEstoque.objects.get_or_create(item=mov.item, unidade=mov.unidade)
            if mov.tipo == 'ENTRADA':
                saldo.quantidade += mov.quantidade
            else:
                saldo.quantidade -= mov.quantidade
            saldo.save()
            
            messages.success(request, f"Movimentação de {mov.item.nome} registrada com sucesso!")
            return redirect('painel_infraestrutura')
    else:
        form = MovimentacaoEstoqueForm()
        
    return render(request, 'infraestrutura/form_movimentacao.html', {
        'form': form,
        'nome_exibicao': get_nome_exibicao(request.user),
        'foto_perfil_url': get_foto_perfil(request.user),
    })
