"""
Configuração do app Django ``comum``.

O que é: recursos compartilhados — formulários base, templatetags e pasta
``static`` com CSS/JS globais do projeto.
"""

from django.apps import AppConfig


class ComumConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.comum"
