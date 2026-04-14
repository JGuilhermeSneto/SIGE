"""
Espelho local do ``BaseModelForm`` do app ``comum`` (form + ``request``).

O que é: mesma ideia do ``apps.comum.forms.base_formularios`` para forms
acadêmicos que precisam do usuário logado no ``__init__``.
"""

from django import forms


class BaseModelForm(forms.ModelForm):
    """Formulário base para os models vinculados a um usuário."""
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
