"""
Rotas de login, logout e fluxo de redefinição de senha (e-mail + token).

O que é: ``urlpatterns`` expostas na raiz do site junto com ``perfis``.
Usa views genéricas do ``django.contrib.auth`` para reset de senha.
"""

from django.contrib.auth import views as auth_views
from django.urls import path
from ..views import autenticacao

urlpatterns = [
    # Autenticação
    path("login/", autenticacao.login_view, name="login"),
    path("logout/", autenticacao.logout_view, name="logout"),
    
    # Reset de Senha
    path(
        "senha/resetar/",
        auth_views.PasswordResetView.as_view(
            template_name="auth/password_reset.html",
            email_template_name="auth/password_reset_email.html",
            subject_template_name="auth/password_reset_subject.txt",
            success_url="/senha/resetar/enviado/",
        ),
        name="password_reset",
    ),
    path(
        "senha/resetar/enviado/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="auth/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "senha/resetar/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="auth/password_reset_confirm.html",
            success_url="/senha/resetar/completo/",
        ),
        name="password_reset_confirm",
    ),
    path(
        "senha/resetar/completo/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="auth/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
