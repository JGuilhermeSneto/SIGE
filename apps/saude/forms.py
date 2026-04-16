from django import forms
from .models.ficha_medica import FichaMedica, RegistroVacina, AtestadoMedico

class FichaMedicaForm(forms.ModelForm):
    class Meta:
        model = FichaMedica
        exclude = ['aluno']
        widgets = {
            'tipo_sanguineo': forms.Select(attrs={'class': 'select-sige'}),
            'alergias': forms.Textarea(attrs={'class': 'input-sige', 'rows': 3, 'placeholder': 'Ex: Amendoim, Penicilina...'}),
            'medicamentos_continuos': forms.Textarea(attrs={'class': 'input-sige', 'rows': 2}),
            'detalhes_pcd': forms.TextInput(attrs={'class': 'input-sige'}),
            'contato_emergencia_nome': forms.TextInput(attrs={'class': 'input-sige'}),
            'contato_emergencia_fone': forms.TextInput(attrs={'class': 'input-sige'}),
            'observacoes_medicas': forms.Textarea(attrs={'class': 'input-sige', 'rows': 3}),
        }

class RegistroVacinaForm(forms.ModelForm):
    class Meta:
        model = RegistroVacina
        fields = ['nome_vacina', 'data_dose', 'lote']
        widgets = {
            'nome_vacina': forms.TextInput(attrs={'class': 'input-sige'}),
            'data_dose': forms.DateInput(attrs={'class': 'input-sige flatpickr', 'type': 'text'}),
            'lote': forms.TextInput(attrs={'class': 'input-sige'}),
        }

class AtestadoForm(forms.ModelForm):
    class Meta:
        model = AtestadoMedico
        fields = ['data_inicio', 'data_fim', 'arquivo', 'descricao']
        widgets = {
            'data_inicio': forms.DateInput(attrs={'class': 'input-sige flatpickr', 'type': 'text'}),
            'data_fim': forms.DateInput(attrs={'class': 'input-sige flatpickr', 'type': 'text'}),
            'arquivo': forms.FileInput(attrs={'class': 'input-sige'}),
            'descricao': forms.Textarea(attrs={'class': 'input-sige', 'rows': 3, 'placeholder': 'Descreva o motivo (opcional)'}),
        }

class AtestadoAnaliseForm(forms.ModelForm):
    class Meta:
        model = AtestadoMedico
        fields = ['status', 'comentario_gestor']
        widgets = {
            'status': forms.Select(attrs={'class': 'select-sige'}),
            'comentario_gestor': forms.Textarea(attrs={'class': 'input-sige', 'rows': 3, 'placeholder': 'Motivo da aprovação ou rejeição'}),
        }
