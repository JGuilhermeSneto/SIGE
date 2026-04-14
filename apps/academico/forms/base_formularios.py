from django import forms

class BaseModelForm(forms.ModelForm):
    """Formulário base para os models vinculados a um usuário."""
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
