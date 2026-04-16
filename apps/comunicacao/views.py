from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models.comunicado import Comunicado
from .forms import ComunicadoForm
from apps.usuarios.utils.perfis import is_super_ou_gestor, get_nome_exibicao, get_foto_perfil

@login_required
@user_passes_test(is_super_ou_gestor)
def listar_comunicados(request):
    """Lista todos os comunicados para gestão administrativa."""
    query = request.GET.get('q', '').strip()
    comunicados = Comunicado.objects.all().order_by('-data_publicacao')
    
    if query:
        comunicados = comunicados.filter(titulo__icontains=query)
        
    return render(request, 'comunicacao/listar_comunicados.html', {
        'comunicados': comunicados,
        'nome_exibicao': get_nome_exibicao(request.user),
        'foto_perfil_url': get_foto_perfil(request.user),
    })

@login_required
@user_passes_test(is_super_ou_gestor)
def cadastrar_editar_comunicado(request, pk=None):
    """Cria ou edita um comunicado institucional."""
    comunicado = get_object_or_404(Comunicado, pk=pk) if pk else None
    
    if request.method == "POST":
        form = ComunicadoForm(request.POST, instance=comunicado)
        if form.is_valid():
            novo_comunicado = form.save(commit=False)
            if not pk:
                novo_comunicado.autor = request.user
            novo_comunicado.save()
            messages.success(request, "Comunicado salvo com sucesso!")
            return redirect('listar_comunicados_gestao')
    else:
        form = ComunicadoForm(instance=comunicado)
        
    return render(request, 'comunicacao/form_comunicado.html', {
        'form': form,
        'editando': bool(pk),
        'nome_exibicao': get_nome_exibicao(request.user),
        'foto_perfil_url': get_foto_perfil(request.user),
    })

@login_required
@user_passes_test(is_super_ou_gestor)
def excluir_comunicado(request, pk):
    """Exclui um comunicado após confirmação."""
    comunicado = get_object_or_404(Comunicado, pk=pk)
    if request.method == "POST":
        comunicado.delete()
        messages.success(request, "Comunicado excluído!")
        return redirect('listar_comunicados_gestao')
    return render(request, 'comunicacao/confirmar_exclusao.html', {'item': comunicado})
