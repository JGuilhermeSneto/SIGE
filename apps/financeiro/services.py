from django.db import transaction
from .models import Fatura, Pagamento
from django.utils import timezone

class FinanceiroService:
    @staticmethod
    @transaction.atomic
    def registrar_pagamento(fatura_id, valor, metodo, comprovante=None, transacao_id=None):
        """
        Registra um pagamento e atualiza o status da fatura.
        """
        fatura = Fatura.objects.get(id=fatura_id)
        
        pagamento = Pagamento.objects.create(
            fatura=fatura,
            valor_pago=valor,
            metodo=metodo,
            comprovante=comprovante,
            transacao_id=transacao_id,
            data_pagamento=timezone.now()
        )
        
        return pagamento

    @staticmethod
    def gerar_fatura_mensal(aluno, descricao, valor, data_vencimento):
        """
        Gera uma nova fatura para um aluno.
        """
        return Fatura.objects.create(
            aluno=aluno,
            descricao=descricao,
            valor=valor,
            data_vencimento=data_vencimento
        )
