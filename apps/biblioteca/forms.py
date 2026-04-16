from django import forms
from .models.biblioteca import Livro, Emprestimo

class LivroForm(forms.ModelForm):
    class Meta:
        model = Livro
        fields = ['titulo', 'autor', 'isbn', 'ano_publicacao', 'editora', 'capa', 'quantidade_total', 'arquivo_digital', 'url_digital']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'input-sige'}),
            'autor': forms.TextInput(attrs={'class': 'input-sige'}),
            'isbn': forms.TextInput(attrs={'class': 'input-sige'}),
            'ano_publicacao': forms.NumberInput(attrs={'class': 'input-sige'}),
            'editora': forms.TextInput(attrs={'class': 'input-sige'}),
            'quantidade_total': forms.NumberInput(attrs={'class': 'input-sige'}),
            'url_digital': forms.URLInput(attrs={'class': 'input-sige', 'placeholder': 'https://...'}),
        }

class EmprestimoForm(forms.ModelForm):
    class Meta:
        model = Emprestimo
        fields = ['livro', 'usuario_aluno', 'usuario_professor', 'data_devolucao_prevista']
        widgets = {
            'livro': forms.Select(attrs={'class': 'select-sige'}),
            'usuario_aluno': forms.Select(attrs={'class': 'select-sige'}),
            'usuario_professor': forms.Select(attrs={'class': 'select-sige'}),
            'data_devolucao_prevista': forms.DateInput(attrs={'class': 'input-sige flatpickr', 'type': 'text'}),
        }
