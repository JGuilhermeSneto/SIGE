"""
Motor 1: Enturmação e Balanceamento de Alunos do ELISE IA.

Responsabilidades do Motor 1:
  1. Análise determinística da distribuição de alunos por turma, série e turno.
  2. Detecção de turmas hiperlotadas (> 30 alunos), sublotadas (< 15 alunos)
     e assimetrias entre turmas paralelas da mesma série (delta >= 8 alunos).
  3. Verificação de distribuição inclusiva de alunos com necessidades especiais (PCD/AEE).
  4. Geração de objetos formais PropostaDecisao (Human-in-the-Loop) com
     justificativa em linguagem natural (Direito à Explicação / Art. 20 LGPD).
  5. Fornecimento de contexto enriquecido para a LLM (Llama 3.1 8B).

Referências no TCC:
  - Seção 1.1 e 2.2 — Desafios de Gestão Escolar e Apoio à Decisão
  - Seção 4.4 — Injeção de Contexto Estruturado
  - Tabela 13 (C2 e C3) — Comparação entre grupos e pedidos de recomendação
"""

import math
import logging
from typing import Dict, Any, List, Optional
from django.db.models import Count, Q

logger = logging.getLogger(__name__)

# Parâmetros pedagógicos de referência (BNCC / Censo Escolar INEP)
CAPACIDADE_MINIMA = 15   # Abaixo disso: risco de déficit operacional
CAPACIDADE_IDEAL = 25    # Tamanho de referência pedagógica
CAPACIDADE_MAXIMA = 30   # Acima disso: hiperlotação
DELTA_DESBALANCEAMENTO = 8  # Diferença mínima entre paralelas que exige remanejamento
MAX_PCD_POR_TURMA = 2    # Diretriz recomendada de suporte inclusivo equilibrado


def diagnosticar_enturmacao(ano: Optional[int] = 2026) -> Dict[str, Any]:
    """
    Realiza o diagnóstico quantitativo rigoroso e determinístico das turmas.
    Retorna métricas consolidadas sem expor nenhum dado pessoal de alunos (LGPD).
    """
    from apps.academico.models.academico import Turma

    qs = Turma.objects.all()
    if ano:
        qs = qs.filter(ano=ano)

    # Coleta turmas com contagem de alunos e contagem de PCDs
    turmas_analisadas = []
    for t in qs.order_by("ano", "nome"):
        total_alunos = t.alunos.filter(status_matricula="ATIVO").count()
        total_pcd = t.alunos.filter(
            status_matricula="ATIVO", possui_necessidade_especial=True
        ).count()

        if total_alunos < CAPACIDADE_MINIMA:
            status_lotacao = "SUBLOTADA"
        elif total_alunos > CAPACIDADE_MAXIMA:
            status_lotacao = "HIPERLOTADA"
        else:
            status_lotacao = "EQUILIBRADA"

        taxa_ocupacao = round((total_alunos / CAPACIDADE_IDEAL) * 100, 1)

        turmas_analisadas.append({
            "id": t.id,
            "nome": t.nome,
            "ano": t.ano,
            "turno": t.turno,
            "total_alunos": total_alunos,
            "total_pcd": total_pcd,
            "status_lotacao": status_lotacao,
            "taxa_ocupacao_percentual": taxa_ocupacao,
        })

    # Agrupamento por série/ano escolar para detecção de desbalanceamento entre paralelas
    # Exemplo: agrupa todas as turmas de '1º Ano' de mesmo turno
    series_agrupadas: Dict[str, List[Dict[str, Any]]] = {}
    for t_data in turmas_analisadas:
        # Extrai chave de agrupamento (ex: '1o Ano_manha_2026')
        prefixo = t_data["nome"].split("(")[0].strip()
        # Normaliza retirando letra 'A' ou 'B'
        for letra in [" A", " B", " C", " D"]:
            if prefixo.endswith(letra):
                prefixo = prefixo[:-len(letra)].strip()
        chave = f"{prefixo}_{t_data['turno']}_{t_data['ano']}"
        series_agrupadas.setdefault(chave, []).append(t_data)

    desbalanceamentos_detectados = []
    for chave, lista_turmas in series_agrupadas.items():
        if len(lista_turmas) >= 2:
            turma_max = max(lista_turmas, key=lambda x: x["total_alunos"])
            turma_min = min(lista_turmas, key=lambda x: x["total_alunos"])
            delta = turma_max["total_alunos"] - turma_min["total_alunos"]

            delta_pcd = abs(turma_max["total_pcd"] - turma_min["total_pcd"])

            if delta >= DELTA_DESBALANCEAMENTO or delta_pcd >= 2:
                desbalanceamentos_detectados.append({
                    "serie_chave": chave,
                    "turma_maior": turma_max,
                    "turma_menor": turma_min,
                    "delta_alunos": delta,
                    "delta_pcd": delta_pcd,
                    "sugestao_remanejamento": math.floor(delta / 2),
                })

    return {
        "ano_referencia": ano,
        "total_turmas_avaliadas": len(turmas_analisadas),
        "turmas": turmas_analisadas,
        "desbalanceamentos": desbalanceamentos_detectados,
        "total_sublotadas": sum(1 for t in turmas_analisadas if t["status_lotacao"] == "SUBLOTADA"),
        "total_hiperlotadas": sum(1 for t in turmas_analisadas if t["status_lotacao"] == "HIPERLOTADA"),
        "total_equilibradas": sum(1 for t in turmas_analisadas if t["status_lotacao"] == "EQUILIBRADA"),
    }


def gerar_propostas_enturmacao(ano: Optional[int] = 2026, persistir: bool = True, usuario=None) -> List[Any]:
    """
    Executa o motor heurístico de apoio à decisão, gerando recomendações
    estruturadas e registrando objetos PropostaDecisao no banco (Human-in-the-Loop).
    """
    from apps.ia.models import PropostaDecisao

    diagnostico = diagnosticar_enturmacao(ano=ano)
    propostas_criadas = []

    # 1. Propostas de balanceamento entre turmas paralelas desiguais
    for item in diagnostico["desbalanceamentos"]:
        t_max = item["turma_maior"]
        t_min = item["turma_menor"]
        qtd_transferir = item["sugestao_remanejamento"]
        novo_max = t_max["total_alunos"] - qtd_transferir
        novo_min = t_min["total_alunos"] + qtd_transferir

        titulo = f"Balanceamento de Turmas: {t_max['nome']} e {t_min['nome']}"
        texto_diagnostico = (
            f"Assimetria identificada entre turmas da mesma série: "
            f"'{t_max['nome']}' possui {t_max['total_alunos']} alunos (com {t_max['total_pcd']} PCDs), "
            f"enquanto '{t_min['nome']}' possui {t_min['total_alunos']} alunos (com {t_min['total_pcd']} PCDs). "
            f"Diferença atual de {item['delta_alunos']} alunos."
        )
        sugestao = (
            f"Recomenda-se remanejar {qtd_transferir} estudantes da turma '{t_max['nome']}' "
            f"para a turma '{t_min['nome']}'. "
            f"Após o remanejamento, ambas as turmas ficarão equilibradas com {novo_max} e {novo_min} alunos. "
            f"Recomenda-se incluir ao menos 1 aluno com necessidade especial no remanejamento para equalizar o suporte pedagógico."
        )
        justificativa = (
            f"Direito à Explicação (Art. 20 LGPD): O remanejamento fundamenta-se nos parâmetros do "
            f"Censo Escolar e diretrizes da BNCC para assegurar turmas com até {CAPACIDADE_MAXIMA} alunos. "
            f"A medida alivia a sobrecarga docente na turma '{t_max['nome']}', otimiza a ocupação física "
            f"da sala da turma '{t_min['nome']}' e distribui uniformemente a demanda de AEE (Atendimento Educacional Especializado)."
        )
        impacto = {
            "turma_origem_id": t_max["id"],
            "turma_destino_id": t_min["id"],
            "qtd_transferir": qtd_transferir,
            "lotacao_projetada_origem": novo_max,
            "lotacao_projetada_destino": novo_min,
            "equilibrio_pcd": True,
        }
        descricao_completa = f"{texto_diagnostico}\n\nSUGESTÃO TÉCNICA:\n{sugestao}"
        payload_proposta = {
            "acao": "REMANEJAR_ALUNOS",
            "turma_origem_id": t_max["id"],
            "turma_destino_id": t_min["id"],
            "qtd_transferir": qtd_transferir,
            "lotacao_projetada_origem": novo_max,
            "lotacao_projetada_destino": novo_min,
            "ano_letivo": ano,
            "impacto": impacto,
        }

        if persistir:
            # Evita duplicatas se já houver proposta idêntica pendente
            proposta, _ = PropostaDecisao.objects.get_or_create(
                tipo="ENTURMACAO",
                titulo=titulo,
                status="PENDENTE",
                defaults={
                    "descricao": descricao_completa,
                    "justificativa": justificativa,
                    "dados_proposta": payload_proposta,
                }
            )
            propostas_criadas.append(proposta)
        else:
            propostas_criadas.append({
                "titulo": titulo,
                "descricao": descricao_completa,
                "justificativa": justificativa,
                "dados_proposta": payload_proposta,
            })

    # 2. Alertas de turmas sublotadas (abaixo de 15 alunos) sem paralela para unificação
    for t_data in diagnostico["turmas"]:
        if t_data["status_lotacao"] == "SUBLOTADA":
            # Verifica se já foi tratada em desbalanceamento
            ja_tratada = any(
                t_data["id"] in [item["turma_maior"]["id"], item["turma_menor"]["id"]]
                for item in diagnostico["desbalanceamentos"]
            )
            if not ja_tratada:
                titulo = f"Alerta de Sublotação Operacional: {t_data['nome']}"
                texto_diagnostico = (
                    f"A turma '{t_data['nome']}' possui apenas {t_data['total_alunos']} alunos matriculados "
                    f"(taxa de ocupação: {t_data['taxa_ocupacao_percentual']}% da capacidade ideal de {CAPACIDADE_IDEAL} alunos)."
                )
                sugestao = (
                    f"Avaliar ações de captação de matrículas no período letivo ou planejamento de unificação com turno alternativo, "
                    f"visto que turmas com menos de {CAPACIDADE_MINIMA} alunos elevam substancialmente o custo fixo por estudante."
                )
                justificativa = (
                    f"Direito à Explicação (Art. 20 LGPD): O indicador de sustentabilidade acadêmica requer "
                    f"ao menos {CAPACIDADE_MINIMA} matrículas por turma para amortizar o custo de folha docente da disciplina. "
                    f"A turma atual opera com déficit relativo de capacidade."
                )
                payload_alerta = {
                    "acao": "ALERTA_SUBLOTACAO",
                    "turma_id": t_data["id"],
                    "alunos_atuais": t_data["total_alunos"],
                    "deficit_minimo": CAPACIDADE_MINIMA - t_data["total_alunos"],
                }
                descricao_alerta = f"{texto_diagnostico}\n\nSUGESTÃO TÉCNICA:\n{sugestao}"

                if persistir:
                    proposta, _ = PropostaDecisao.objects.get_or_create(
                        tipo="ENTURMACAO",
                        titulo=titulo,
                        status="PENDENTE",
                        defaults={
                            "descricao": descricao_alerta,
                            "justificativa": justificativa,
                            "dados_proposta": payload_alerta,
                        }
                    )
                    propostas_criadas.append(proposta)
                else:
                    propostas_criadas.append({
                        "titulo": titulo,
                        "descricao": descricao_alerta,
                        "justificativa": justificativa,
                        "dados_proposta": payload_alerta,
                    })

    return propostas_criadas


def montar_contexto_motor_enturmacao(ano: Optional[int] = 2026) -> str:
    """
    Gera o bloco analítico determinístico específico do Motor 1
    para injeção de contexto RAG no modelo Llama 3.1 8B.
    """
    diag = diagnosticar_enturmacao(ano=ano)
    linhas = [
        f"--- MOTOR 1: DIAGNÓSTICO DE ENTURMAÇÃO E BALANCEAMENTO ({ano or 'TODOS OS ANOS'}) ---",
        f"Turmas analisadas: {diag['total_turmas_avaliadas']} | Equilibradas: {diag['total_equilibradas']} | "
        f"Sublotadas: {diag['total_sublotadas']} | Hiperlotadas: {diag['total_hiperlotadas']}",
        "",
        "Detalhamento por Turma (Nome | Turno | Alunos | PCDs | Status):"
    ]

    for t in diag["turmas"]:
        linhas.append(
            f"  • {t['nome']} | {t['turno']} | {t['total_alunos']} aluno(s) | "
            f"{t['total_pcd']} PCD(s) | Status: {t['status_lotacao']}"
        )

    if diag["desbalanceamentos"]:
        linhas.append("")
        linhas.append("Assimetrias Críticas Detectadas entre Turmas Paralelas:")
        for d in diag["desbalanceamentos"]:
            t_max = d["turma_maior"]
            t_min = d["turma_menor"]
            linhas.append(
                f"  ⚠️ Assimetria de {d['delta_alunos']} alunos: '{t_max['nome']}' ({t_max['total_alunos']} alunos, {t_max['total_pcd']} PCDs) "
                f"vs '{t_min['nome']}' ({t_min['total_alunos']} alunos, {t_min['total_pcd']} PCDs). "
                f"Recomendação técnica: remanejar {d['sugestao_remanejamento']} alunos."
            )

    linhas.append("--- FIM DO DIAGNÓSTICO DO MOTOR 1 ---")
    return "\n".join(linhas)
