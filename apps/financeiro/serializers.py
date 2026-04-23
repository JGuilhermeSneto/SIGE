from rest_framework import serializers
from .models import Fatura, Pagamento

class PagamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pagamento
        fields = '__all__'

class FaturaSerializer(serializers.ModelSerializer):
    pagamentos = PagamentoSerializer(many=True, read_only=True)
    atrasada = serializers.BooleanField(source='esta_atrasada', read_only=True)

    class Meta:
        model = Fatura
        fields = [
            'id', 'aluno', 'descricao', 'valor', 'data_vencimento', 
            'status', 'link_pagamento', 'pagamentos', 'atrasada', 
            'created_at'
        ]
