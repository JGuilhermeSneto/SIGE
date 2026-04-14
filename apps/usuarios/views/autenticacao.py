"""
Views de sessão: login, logout e mensagens de feedback.

O que é: usa ``LoginForm`` para autenticar por e-mail e encaminha o usuário
ao painel correto via ``redirect_user``.
"""

from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from ..forms.autenticacao import LoginForm
from ..utils.perfis import redirect_user

def login_view(request):
    """
    Realiza a autenticação do usuário utilizando o LoginForm.
    Redireciona para o painel apropriado em caso de sucesso.
    """
    if request.user.is_authenticated:
        return redirect(redirect_user(request.user))

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Limpa mensagens antigas da sessão para não acumular
            list(messages.get_messages(request))
            messages.success(request, "Login bem-sucedido!")
            
            return redirect(redirect_user(user))
    else:
        form = LoginForm()

    return render(request, "auth/login.html", {"form": form})


def logout_view(request):
    """Encerra a sessão do usuário e redireciona para o login."""
    logout(request)
    # A mensagem de logout foi removida daqui, pois a animação no frontend já informa o usuário,
    # prevenindo que a mensagem fique acumulada para o próximo login.
    return redirect("login")
