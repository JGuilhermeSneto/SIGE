from django.db import transaction
from ..models.patrimonio import SaldoEstoque, MovimentacaoEstoque

class EstoqueService:
    @staticmethod
    @transaction.atomic
    def processar_movimentacao_estoque(movimentacao):
        """
        Processa uma instância de movimentação já criada (pelo form.save())
        e atualiza o saldo do estoque.
        """
        saldo, _ = SaldoEstoque.objects.get_or_create(
            item=movimentacao.item,
            unidade=movimentacao.unidade,
            defaults={'quantidade': 0}
        )
        
        if movimentacao.tipo == 'ENTRADA':
            saldo.quantidade += movimentacao.quantidade
        else:
            if saldo.quantidade < movimentacao.quantidade:
                # Opcional: Você pode querer validar isso no Form também
                pass
            saldo.quantidade -= movimentacao.quantidade
            
        saldo.save()
        return saldo

    @staticmethod
    @transaction.atomic
    def registrar_movimentacao(item, unidade, tipo, quantidade, justificativa=""):
        """
        Registra uma movimentação e atualiza o saldo do estoque de forma atômica.
        """
        # Cria o registro da movimentação
        movimentacao = MovimentacaoEstoque.objects.create(
            item=item,
            unidade=unidade,
            tipo=tipo,
            quantidade=quantidade,
            justificativa=justificativa
        )
        
        # Atualiza o saldo
        saldo, created = SaldoEstoque.objects.get_or_create(
            item=item,
            unidade=unidade,
            defaults={'quantidade': 0}
        )
        
        if tipo == 'ENTRADA':
            saldo.quantidade += quantidade
        else:
            if saldo.quantidade < quantidade:
                raise ValueError("Saldo insuficiente para realizar a saída.")
            saldo.quantidade -= quantidade
            
        saldo.save()
        return movimentacao
