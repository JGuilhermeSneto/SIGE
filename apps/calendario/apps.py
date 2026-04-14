"""
Configuração do app Django ``calendario``.

O que é: calendário acadêmico, eventos e telas associadas à visualização
mensal/anual para os usuários do SIGE.
"""

from django.apps import AppConfig


class CalendarioConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.calendario"
    label = "calendario"
