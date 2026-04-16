from django import forms
from .models.comunicado import Comunicado

class ComunicadoForm(forms.ModelForm):
    class Meta:
        model = Comunicado
        fields = ['titulo', 'conteudo', 'publico_alvo', 'importancia', 'data_expiracao']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'input-sige', 'placeholder': 'Título do aviso'}),
            'conteudo': forms.Textarea(attrs={'class': 'input-sige', 'rows': 4, 'placeholder': 'Descreva o comunicado...'}),
            'publico_alvo': forms.Select(attrs={'class': 'select-sige'}),
            'importancia': forms.Select(attrs={'class': 'select-sige'}),
            'data_expiracao': forms.DateInput(attrs={'class': 'input-sige flatpickr', 'type': 'text'}),
        }
