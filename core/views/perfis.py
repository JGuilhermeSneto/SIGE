from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from ..forms import EditarPerfilForm
from ..utils import get_user_profile, get_foto_perfil, get_nome_exibicao, redirect_user

@login_required
def editar_perfil(request):
    """Gerencia a atualização de dados do próprio usuário."""
    user   = request.user
    perfil = get_user_profile(user)

    form = EditarPerfilForm(request.POST or None, request.FILES or None, instance=user)

    if request.method == "POST":
        if form.is_valid():
            user = form.save(commit=False)
            nova_senha = form.cleaned_data.get("nova_senha")
            if nova_senha:
                user.set_password(nova_senha)
                update_session_auth_hash(request, user)

            user.save()

            foto = request.FILES.get("foto")
            if perfil and foto:
                perfil.foto = foto
                perfil.save()

            messages.success(request, "Perfil atualizado com sucesso!")
            return redirect(redirect_user(user))
        else:
            messages.error(request, "Erro ao atualizar perfil. Verifique os campos abaixo.")

    foto_atual = perfil.foto.url if perfil and getattr(perfil, "foto", None) else None

    return render(
        request,
        "core/editar_perfil.html",
        {
            "form":            form,
            "perfil":          perfil,
            "foto_atual":      foto_atual,
            "foto_perfil_url": get_foto_perfil(user),
            "nome_exibicao":   get_nome_exibicao(user),
        },
    )


@login_required
def remover_foto_perfil(request):
    """Remove a foto de perfil do usuário."""
    perfil = get_user_profile(request.user)

    if not perfil:
        messages.error(request, "Nenhum perfil associado ao usuário.")
        return redirect("editar_perfil")

    if getattr(perfil, "foto", None):
        perfil.foto.delete(save=False)
        perfil.foto = None
        perfil.save()
        messages.success(request, "Foto removida com sucesso!")
    else:
        messages.info(request, "Você não possui uma foto de perfil cadastrada.")

    return redirect("editar_perfil")
