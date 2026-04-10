from django import forms
from .base import BaseModelForm
from ..models import Turma, Disciplina, Professor

class TurmaForm(BaseModelForm):
    """Formulário para Turma."""
    class Meta:
        model = Turma
        fields = ["nome", "turno", "ano"]
        
    def clean(self):
        cleaned_data = super().clean()
        nome = cleaned_data.get("nome")
        ano = cleaned_data.get("ano")
        
        # Validação de duplicidade
        qs = Turma.objects.filter(nome=nome, ano=ano)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
            
        if qs.exists():
            raise forms.ValidationError("Já existe uma turma com este nome para o ano informado.")
            
        return cleaned_data

class DisciplinaForm(BaseModelForm):
    """Formulário para Disciplina."""
    class Meta:
        model = Disciplina
        fields = ["nome", "professor", "turma"]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Opcional: filtrar professores se necessário
        self.fields["professor"].queryset = Professor.objects.select_related("user").all()

    def clean(self):
        cleaned_data = super().clean()
        nome = cleaned_data.get("nome")
        turma = cleaned_data.get("turma")
        
        if nome and turma:
            qs = Disciplina.objects.filter(nome=nome, turma=turma)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError(f"A disciplina '{nome}' já está cadastrada para esta turma.")
        
        return cleaned_data
