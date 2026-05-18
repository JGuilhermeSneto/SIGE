from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from ...models.perfis import Gestor
from ...forms.perfis import GestorForm
from ...utils.perfis import get_nome_exibicao, get_foto_perfil
from django.core.exceptions import ValidationError
from .helpers import exibir_erros_formulario


def pode_gerenciar_gestores(u):
    return u.is_superuser or (
        hasattr(u, "gestor") and u.gestor.cargo in ("diretor", "vice_diretor")
    )


@login_required
@user_passes_test(pode_gerenciar_gestores)
def cadastrar_editar_gestor(request, gestor_id=None):
    """Dashboard Gestão."""
    gestor = get_object_or_404(Gestor, id=gestor_id) if gestor_id else None
    if request.method == "POST":
        form = GestorForm(request.POST, request.FILES, instance=gestor, request=request)
        if form.is_valid():
            try:
                gestor_obj = form.save()
                messages.success(request, f"{gestor_obj.nome_completo} processado!")
                return redirect("listar_gestores")
            except ValidationError as e:
                for msg in e.messages:
                    messages.error(request, msg)
            except Exception as e:
                messages.error(request, f"Erro ao salvar: {str(e)}")
        else:
            exibir_erros_formulario(request, form)
    else:
        form = GestorForm(instance=gestor, request=request)
    return render(
        request,
        "gestor/cadastrar_gestor.html",
        {
            "form": form,
            "gestor": gestor,
            "nome_exibicao": get_nome_exibicao(request.user),
            "foto_perfil_url": get_foto_perfil(request.user),
        },
    )


@login_required
@user_passes_test(pode_gerenciar_gestores)
def listar_gestores(request):
    """Lista gestores."""
    query = request.GET.get("q", "")
    gestores = Gestor.objects.select_related("user").all()
    if query:
        gestores = gestores.filter(nome_completo__icontains=query)
    return render(
        request,
        "gestor/listar_gestores.html",
        {
            "gestores": gestores,
            "query": query,
            "nome_exibicao": get_nome_exibicao(request.user),
            "foto_perfil_url": get_foto_perfil(request.user),
        },
    )


@login_required
@user_passes_test(pode_gerenciar_gestores)
def excluir_gestor(request, gestor_id):
    """Remove gestor."""
    gestor = get_object_or_404(Gestor, id=gestor_id)
    try:
        if gestor.user:
            gestor.user.delete()
        else:
            gestor.delete()
        messages.success(request, "Gestor removido.")
    except Exception as e:
        messages.error(request, f"Erro ao remover gestor: {str(e)}")
    return redirect("listar_gestores")
