from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

from .models.patrimonio import ItemPatrimonio
from .forms import ItemPatrimonioForm, MovimentacaoEstoqueForm
from .selectors import InfraSelector
from .services import InfraService
from apps.usuarios.utils.perfis import is_super_ou_gestor, get_nome_exibicao, get_foto_perfil

@login_required
@user_passes_test(is_super_ou_gestor)
def painel_infraestrutura(request):
    """Dashboard de Gestão de Infraestrutura utilizando Pattern Selector."""
    query = request.GET.get('q', '').strip()
    
    # Busca todos os dados via Selector
    context_data = InfraSelector.get_painel_data(query_text=query)
    
    # Adiciona dados de contexto de perfil
    context_data.update({
        'nome_exibicao': get_nome_exibicao(request.user),
        'foto_perfil_url': get_foto_perfil(request.user),
    })

    return render(request, 'infraestrutura/painel_infra.html', context_data)

@login_required
@user_passes_test(is_super_ou_gestor)
def cadastrar_editar_patrimonio(request, pk=None):
    """Cria ou edita um item de patrimônio."""
    item = get_object_or_404(ItemPatrimonio, pk=pk) if pk else None
    
    if request.method == "POST":
        form = ItemPatrimonioForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Item de patrimônio salvo com sucesso!")
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
    """Registra entrada ou saída de itens utilizando Pattern Service."""
    if request.method == "POST":
        form = MovimentacaoEstoqueForm(request.POST)
        if form.is_valid():
            movimentacao = form.save()
            
            # Delega a lógica de negócio para o Service
            InfraService.processar_movimentacao_estoque(movimentacao)
            
            messages.success(request, f"Movimentação de {movimentacao.item.nome} processada com sucesso!")
            return redirect('painel_infraestrutura')
    else:
        form = MovimentacaoEstoqueForm()
        
    return render(request, 'infraestrutura/form_movimentacao.html', {
        'form': form,
        'nome_exibicao': get_nome_exibicao(request.user),
        'foto_perfil_url': get_foto_perfil(request.user),
    })
