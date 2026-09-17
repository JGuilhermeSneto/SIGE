"""
Configuração do app Django ``usuarios``.

O que é: registro do aplicativo que concentra autenticação, perfis (aluno,
professor, gestor) e painéis principais da ELISE.
"""

from django.apps import AppConfig


class UsuariosConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.usuarios"
    label = "usuarios"
