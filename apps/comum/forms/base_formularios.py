"""
Formulários base reutilizáveis no SIGE.

O que é: ``BaseModelForm`` injeta ``request`` no ``__init__`` para forms que
precisam do usuário logado (padrão comum em apps ``usuarios``/``academico``).
"""

from django import forms


class BaseModelForm(forms.ModelForm):
    """Formulário base para modelos ligados ao usuário autenticado."""
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
