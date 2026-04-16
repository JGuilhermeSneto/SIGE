from django import forms
from .models.patrimonio import ItemPatrimonio, MovimentacaoEstoque, ItemEstoque

class ItemPatrimonioForm(forms.ModelForm):
    class Meta:
        model = ItemPatrimonio
        fields = ['tombamento', 'nome', 'categoria', 'unidade', 'estado_conservacao', 'data_aquisicao', 'valor_aquisicao']
        widgets = {
            'tombamento': forms.TextInput(attrs={'class': 'input-sige'}),
            'nome': forms.TextInput(attrs={'class': 'input-sige'}),
            'categoria': forms.Select(attrs={'class': 'select-sige'}),
            'unidade': forms.Select(attrs={'class': 'select-sige'}),
            'estado_conservacao': forms.Select(attrs={'class': 'select-sige'}),
            'data_aquisicao': forms.DateInput(attrs={'class': 'input-sige flatpickr', 'type': 'text'}),
            'valor_aquisicao': forms.NumberInput(attrs={'class': 'input-sige', 'step': '0.01'}),
        }

class MovimentacaoEstoqueForm(forms.ModelForm):
    class Meta:
        model = MovimentacaoEstoque
        fields = ['item', 'unidade', 'tipo', 'quantidade', 'justificativa']
        widgets = {
            'item': forms.Select(attrs={'class': 'select-sige'}),
            'unidade': forms.Select(attrs={'class': 'select-sige'}),
            'tipo': forms.Select(attrs={'class': 'select-sige'}),
            'quantidade': forms.NumberInput(attrs={'class': 'input-sige'}),
            'justificativa': forms.TextInput(attrs={'class': 'input-sige', 'placeholder': 'Motivo da movimentação'}),
        }
