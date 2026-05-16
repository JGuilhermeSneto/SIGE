from django.db.models import Sum, Count, Q
from django.utils import timezone
from .models import Fatura, Pagamento, AcordoFinanceiro, Lancamento

class FinanceiroSelectors:
    @staticmethod
    def get_inadimplentes_detalhado():
        """
        Retorna lista de alunos com faturas atrasadas e o montante total.
        """
        hoje = timezone.now().date()
        faturas_atrasadas = Fatura.objects.filter(
            status="PENDENTE",
            data_vencimento__lt=hoje
        ).select_related('aluno', 'aluno__turma')

        # Agrupar por aluno para o relatório
        inadimplentes = {}
        for fatura in faturas_atrasadas:
            aluno_id = fatura.aluno.id
            if aluno_id not in inadimplentes:
                inadimplentes[aluno_id] = {
                    "aluno": fatura.aluno,
                    "total_devido": 0,
                    "qtd_faturas": 0,
                    "vencimento_mais_antigo": fatura.data_vencimento
                }
            
            inadimplentes[aluno_id]["total_devido"] += fatura.valor
            inadimplentes[aluno_id]["qtd_faturas"] += 1
            if fatura.data_vencimento < inadimplentes[aluno_id]["vencimento_mais_antigo"]:
                inadimplentes[aluno_id]["vencimento_mais_antigo"] = fatura.data_vencimento

        return sorted(inadimplentes.values(), key=lambda x: x["total_devido"], reverse=True)

    @staticmethod
    def get_resumo_caixa_mes(mes, ano):
        """
        Retorna totais de entradas e saídas do mês.
        """
        lancamentos = Lancamento.objects.filter(
            data_pagamento__month=mes,
            data_pagamento__year=ano
        )

        receitas = lancamentos.filter(tipo="ENTRADA").aggregate(total=Sum('valor'))['total'] or 0
        despesas = lancamentos.filter(tipo="SAIDA").aggregate(total=Sum('valor'))['total'] or 0

        return {
            "receitas": receitas,
            "despesas": despesas,
            "saldo": receitas - despesas
        }
