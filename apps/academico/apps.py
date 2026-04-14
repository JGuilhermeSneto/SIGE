"""
Configuração do app Django ``academico``.

O que é: domínio escolar — turmas, disciplinas, notas, frequência, atividades
e relatórios acadêmicos.
"""

from django.apps import AppConfig


class AcademicoConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.academico"
    label = "academico"
