from django.db import transaction
from ..models import Fatura, Pagamento, AcordoFinanceiro, ParcelaAcordo
from datetime import timedelta
from django.utils import timezone


class FinanceiroService:
    @staticmethod
    @transaction.atomic
    def registrar_pagamento(
        fatura_id, valor, metodo, comprovante=None, transacao_id=None
    ):
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
            data_pagamento=timezone.now(),
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
            data_vencimento=data_vencimento,
        )

    @staticmethod
    @transaction.atomic
    def criar_acordo(aluno, fatura_ids, numero_parcelas, valor_com_desconto, observacoes=""):
        """
        Consolida faturas atrasadas em um novo acordo de parcelamento.
        """
        faturas = Fatura.objects.filter(id__in=fatura_ids, aluno=aluno)
        valor_total_original = sum(f.valor for f in faturas)

        # 1. Criar o Acordo
        acordo = AcordoFinanceiro.objects.create(
            aluno=aluno,
            valor_total_original=valor_total_original,
            valor_com_desconto=valor_com_desconto,
            numero_parcelas=numero_parcelas,
            observacoes=observacoes
        )
        acordo.faturas_originais.set(faturas)

        # 2. Cancelar faturas originais (ou marcar como renegociadas)
        faturas.update(status="CANCELADO")

        # 3. Gerar as parcelas
        valor_parcela = valor_com_desconto / numero_parcelas
        data_base = timezone.now().date()

        for i in range(numero_parcelas):
            ParcelaAcordo.objects.create(
                acordo=acordo,
                valor=valor_parcela,
                data_vencimento=data_base + timedelta(days=30 * (i + 1)),
                status="PENDENTE"
            )

        return acordo
