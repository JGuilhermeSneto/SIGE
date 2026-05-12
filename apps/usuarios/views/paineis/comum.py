from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from ...utils.perfis import get_nome_exibicao, get_foto_perfil, redirect_user


@login_required
def painel_usuarios(request):
    """Redirecionador para os painéis específicos (ponto de entrada geral)."""
    return render(
        request,
        "core/usuarios.html",
        {
            "nome_exibicao": get_nome_exibicao(request.user),
            "foto_perfil_url": get_foto_perfil(request.user),
        },
    )


@login_required
def dashboard_redirect(request):
    """URL central 'dashboard' que redireciona para o painel correto do usuário."""
    target = redirect_user(request.user)
    return redirect(target)
