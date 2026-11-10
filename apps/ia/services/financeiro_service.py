"""
Motor 3 de Apoio à Decisão: Sustentabilidade Financeira de Turmas e Análise de Break-Even.

Este módulo realiza diagnósticos econômicos determinísticos sobre turmas escolares,
analisando receita faturada, recebimentos, faturas a vencer/inadimplência e custo
operacional estimado por turma, para cálculo de ponto de equilíbrio (Break-even).

Conformidade Ética e Legal:
- Zero Alucinação: Todos os cálculos financeiros são executados pelo Django ORM.
- LGPD e Ética Pedagógica: Jamais expõe dados nominais de alunos devedores, apenas
  índices percentuais e valores consolidados agregados por turma.
- Human-in-the-Loop: Recomendações geradas como PropostaDecisao com status PENDENTE.
"""

import logging
from decimal import Decimal
from typing import Dict, Any, List, Optional
from django.db.models import Sum, Count, Q
from django.utils import timezone

from apps.academico.models.academico import Turma
from apps.usuarios.models.perfis import Aluno
from apps.financeiro.models import Fatura
from apps.ia.models import PropostaDecisao

logger = logging.getLogger(__name__)

# Parâmetros Econômicos e Financeiros de Referência
MENSALIDADE_PADRAO = Decimal("500.00")
CUSTO_MENSAL_OPERACIONAL_TURMA = Decimal("7500.00")  # Salários docentes + encargos + manutenção
BREAK_EVEN_ALUNOS = 15                              # Número mínimo de alunos para custo zero (15 * 500 = 7.500)
LIMITE_INADIMPLENCIA_ALERTA = 0.20                 # 20% de inadimplência dispara recomendação preventiva


def diagnosticar_financeiro(ano: int = 2026) -> Dict[str, Any]:
    """
    Executa diagnóstico determinístico de sustentabilidade financeira das turmas do ano letivo.
    
    Calcula:
    - Receita potencial mensal vs custo operacional
    - Ponto de equilíbrio (break-even) de cada turma
    - Histórico e taxa de recebimento/inadimplência agregada
    - Identificação de turmas deficitárias
    """
    turmas_qs = Turma.objects.filter(ano=ano)
    if not turmas_qs.exists():
        turmas_qs = Turma.objects.all()

    total_alunos_ano = 0
    receita_potencial_mensal_total = Decimal("0.00")
    custo_mensal_total = Decimal("0.00")
    turmas_detalhes = []
    turmas_deficitarias = []
    alertas = []

    total_faturado_global = Decimal("0.00")
    total_recebido_global = Decimal("0.00")
    total_pendente_global = Decimal("0.00")

    for turma in turmas_qs:
        alunos_turma = Aluno.objects.filter(turma=turma, status_matricula="ATIVO")
        qtd_alunos = alunos_turma.count()
        total_alunos_ano += qtd_alunos

        receita_mensal = Decimal(str(qtd_alunos)) * MENSALIDADE_PADRAO
        custo_mensal = CUSTO_MENSAL_OPERACIONAL_TURMA
        saldo_mensal = receita_mensal - custo_mensal
        margem_pct = (saldo_mensal / custo_mensal * 100) if custo_mensal > 0 else Decimal("0.00")

        receita_potencial_mensal_total += receita_mensal
        custo_mensal_total += custo_mensal

        # Status de equilíbrio financeiro
        if qtd_alunos < BREAK_EVEN_ALUNOS:
            status_financeiro = "DEFICITARIA"
            deficit_info = {
                "turma_id": turma.id,
                "turma_nome": turma.nome,
                "alunos": qtd_alunos,
                "deficit_mensal": float(abs(saldo_mensal)),
                "alunos_faltantes_breakeven": BREAK_EVEN_ALUNOS - qtd_alunos
            }
            turmas_deficitarias.append(deficit_info)
            alertas.append({
                "turma": turma.nome,
                "severidade": "ALTA",
                "mensagem": (
                    f"Turma '{turma.nome}' opera abaixo do ponto de equilíbrio ({qtd_alunos}/{BREAK_EVEN_ALUNOS} alunos). "
                    f"Déficit operacional estimado em R$ {abs(saldo_mensal):,.2f}/mês."
                )
            })
        elif qtd_alunos >= 25:
            status_financeiro = "SUPERAVITARIA"
        else:
            status_financeiro = "SUSTENTAVEL"

        # Faturas vinculadas aos alunos desta turma
        faturas_turma = Fatura.objects.filter(aluno__turma=turma)
        total_faturado_t = faturas_turma.aggregate(s=Sum("valor"))["s"] or Decimal("0.00")
        total_recebido_t = faturas_turma.filter(status="PAGO").aggregate(s=Sum("valor"))["s"] or Decimal("0.00")
        total_pendente_t = faturas_turma.filter(status="PENDENTE").aggregate(s=Sum("valor"))["s"] or Decimal("0.00")

        total_faturado_global += total_faturado_t
        total_recebido_global += total_recebido_t
        total_pendente_global += total_pendente_t

        taxa_inadimplencia = float(total_pendente_t / total_faturado_t) if total_faturado_t > 0 else 0.0

        if taxa_inadimplencia >= LIMITE_INADIMPLENCIA_ALERTA and total_faturado_t > 0:
            alertas.append({
                "turma": turma.nome,
                "severidade": "MEDIA",
                "mensagem": (
                    f"Turma '{turma.nome}' apresenta taxa de inadimplência/pendência de {round(taxa_inadimplencia*100, 1)}% "
                    f"(R$ {total_pendente_t:,.2f} pendentes)."
                )
            })

        turmas_detalhes.append({
            "id": turma.id,
            "nome": turma.nome,
            "turno": turma.turno,
            "alunos_ativos": qtd_alunos,
            "receita_mensal_estimada": float(receita_mensal),
            "custo_mensal_estimado": float(custo_mensal),
            "saldo_mensal_estimado": float(saldo_mensal),
            "margem_pct": round(float(margem_pct), 1),
            "status_financeiro": status_financeiro,
            "faturado_total": float(total_faturado_t),
            "recebido_total": float(total_recebido_t),
            "pendente_total": float(total_pendente_t),
            "taxa_inadimplencia_pct": round(taxa_inadimplencia * 100, 1)
        })

    saldo_mensal_global = receita_potencial_mensal_total - custo_mensal_total
    taxa_inadimplencia_global = (float(total_pendente_global / total_faturado_global) * 100) if total_faturado_global > 0 else 0.0

    return {
        "ano_referencia": ano,
        "total_turmas": len(turmas_detalhes),
        "total_alunos_ativos": total_alunos_ano,
        "mensalidade_referencia": float(MENSALIDADE_PADRAO),
        "break_even_alunos_por_turma": BREAK_EVEN_ALUNOS,
        "receita_mensal_projetada": float(receita_potencial_mensal_total),
        "custo_mensal_projetado": float(custo_mensal_total),
        "saldo_mensal_operacional": float(saldo_mensal_global),
        "total_faturado_acumulado": float(total_faturado_global),
        "total_recebido_acumulado": float(total_recebido_global),
        "total_pendente_acumulado": float(total_pendente_global),
        "taxa_inadimplencia_global_pct": round(taxa_inadimplencia_global, 1),
        "turmas": turmas_detalhes,
        "turmas_deficitarias": turmas_deficitarias,
        "alertas": alertas
    }


def gerar_propostas_financeiro(ano: int = 2026, persistir: bool = True, usuario: Optional[Any] = None) -> List[PropostaDecisao]:
    """
    Gera propostas deliberativas formais com base no diagnóstico econômico,
    garantindo que o gestor tenha clareza do impacto de cada decisão.
    
    Status inicial estritamente PENDENTE.
    """
    diag = diagnosticar_financeiro(ano=ano)
    propostas_geradas = []

    # Proposta 1: Equilíbrio financeiro para turmas deficitárias
    for t_def in diag["turmas_deficitarias"]:
        titulo = f"Plano de Sustentabilidade Financeira - {t_def['turma_nome']}"
        descricao = (
            f"Diagnóstico: A turma '{t_def['turma_nome']}' conta com apenas {t_def['alunos']} alunos matriculados, "
            f"estando {t_def['alunos_faltantes_breakeven']} alunos abaixo do ponto de equilíbrio econômico "
            f"({BREAK_EVEN_ALUNOS} alunos).\n"
            f"Déficit mensal estimado: R$ {t_def['deficit_mensal']:,.2f}/mês.\n"
            f"Recomendação: Avaliar a fusão da turma com turma correlata do mesmo turno/ano "
            f"ou intensificar campanha de matrículas para atingir o contingente mínimo viável."
        )
        justificativa = (
            f"A manutenção de turmas isoladas com menos de {BREAK_EVEN_ALUNOS} alunos onera a folha docente "
            f"sem a cobertura correspondente da receita de mensalidades, comprometendo a sustentabilidade "
            f"orçamentária da mantenedora escolar."
        )
        dados = {
            "turma_id": t_def["turma_id"],
            "turma_nome": t_def["turma_nome"],
            "alunos_atuais": t_def["alunos"],
            "breakeven_meta": BREAK_EVEN_ALUNOS,
            "deficit_mensal": t_def["deficit_mensal"],
            "acao_sugerida": "FUSAO_OU_CAPTACAO"
        }

        if persistir:
            prop, criada = PropostaDecisao.objects.get_or_create(
                tipo="FINANCEIRO",
                titulo=titulo,
                defaults={
                    "descricao": descricao,
                    "justificativa": justificativa,
                    "dados_proposta": dados,
                    "status": "PENDENTE"
                }
            )
            propostas_geradas.append(prop)
        else:
            propostas_geradas.append(PropostaDecisao(
                tipo="FINANCEIRO",
                titulo=titulo,
                descricao=descricao,
                justificativa=justificativa,
                dados_proposta=dados,
                status="PENDENTE"
            ))

    # Proposta 2: Ação de cobrança preventiva para taxas de inadimplência elevadas
    if diag["taxa_inadimplencia_global_pct"] >= (LIMITE_INADIMPLENCIA_ALERTA * 100):
        titulo = f"Política de Cobrança Preventiva e Mitigação de Inadimplência ({ano})"
        descricao = (
            f"Diagnóstico: A taxa agregada de pendência/inadimplência atingiu {diag['taxa_inadimplencia_global_pct']}%, "
            f"totalizando R$ {diag['total_pendente_acumulado']:,.2f} a receber.\n"
            f"Recomendação: Implementação de régua de comunicação automatizada com lembretes prévios ao "
            f"vencimento e campanhas de negociação amigável para débitos pendentes."
        )
        justificativa = (
            f"Manter o fluxo de caixa saudável é essencial para o cumprimento da folha de pagamento "
            f"dos docentes e investimentos contínuos na infraestrutura pedagógica."
        )
        dados = {
            "ano": ano,
            "taxa_inadimplencia_pct": diag["taxa_inadimplencia_global_pct"],
            "total_pendente": diag["total_pendente_acumulado"],
            "acao_sugerida": "REGUA_COBRANCA_PREVENTIVA"
        }

        if persistir:
            prop, criada = PropostaDecisao.objects.get_or_create(
                tipo="FINANCEIRO",
                titulo=titulo,
                defaults={
                    "descricao": descricao,
                    "justificativa": justificativa,
                    "dados_proposta": dados,
                    "status": "PENDENTE"
                }
            )
            propostas_geradas.append(prop)
        else:
            propostas_geradas.append(PropostaDecisao(
                tipo="FINANCEIRO",
                titulo=titulo,
                descricao=descricao,
                justificativa=justificativa,
                dados_proposta=dados,
                status="PENDENTE"
            ))

    return propostas_geradas


def montar_contexto_motor_financeiro(ano: int = 2026) -> str:
    """
    Monta bloco sintetizado de contexto para RAG do Motor 3.
    Contém apenas indicadores agregados e métricas de equilíbrio econômico.
    """
    diag = diagnosticar_financeiro(ano=ano)

    linhas = [
        f"### DIAGNÓSTICO DO MOTOR 3 (SUSTENTABILIDADE FINANCEIRA DE TURMAS - {ano}):",
        f"- Mensalidade de Referência: R$ {diag['mensalidade_referencia']:,.2f} | Custo Operacional por Turma: R$ {float(CUSTO_MENSAL_OPERACIONAL_TURMA):,.2f}",
        f"- Ponto de Equilíbrio (Break-Even): {diag['break_even_alunos_por_turma']} alunos/turma",
        f"- Projeção Mensal Global: Receita R$ {diag['receita_mensal_projetada']:,.2f} | Custo R$ {diag['custo_mensal_projetado']:,.2f} | Saldo R$ {diag['saldo_mensal_operacional']:,.2f}",
        f"- Acumulado Faturado: R$ {diag['total_faturado_acumulado']:,.2f} | Recebido: R$ {diag['total_recebido_acumulado']:,.2f} | Pendente: R$ {diag['total_pendente_acumulado']:,.2f} ({diag['taxa_inadimplencia_global_pct']}% pendente)",
        "- Sustentabilidade por Turma:"
    ]

    for t in diag["turmas"]:
        linhas.append(
            f"  * {t['nome']} ({t['turno']}): {t['alunos_ativos']} alunos - Receita R$ {t['receita_mensal_estimada']:,.2f} | Custo R$ {t['custo_mensal_estimado']:,.2f} | Margem: {t['margem_pct']}% - Status: {t['status_financeiro']}"
        )

    if diag["alertas"]:
        linhas.append("- Alertas do Motor Financeiro:")
        for al in diag["alertas"]:
            linhas.append(f"  * [{al['severidade']}] {al['mensagem']}")

    return "\n".join(linhas)

