"""
Motor 2 de Apoio à Decisão: Infraestrutura, Ocupação de Espaços e Conservação Patrimonial.

Este módulo realiza diagnósticos determinísticos e gera propostas formais de decisão
para a gestão de ambientes escolares e equipamentos, em conformidade com as diretrizes
do Censo Escolar/INEP e do TCC ELISE (Human-in-the-Loop, LGPD e Explicabilidade).

Zero Alucinação: Todos os cálculos de taxa de ocupação, índice de avaria patrimonial
e dimensionamento de salas são processados exclusivamente pelo Django ORM.
"""

import logging
from typing import Dict, Any, List, Optional
from django.db.models import Count, Q
from django.utils import timezone

from apps.infraestrutura.models.patrimonio import Ambiente, ItemPatrimonio, CategoriaBem, UnidadeEscolar
from apps.academico.models.academico import GradeHorario, Turma
from apps.ia.models import PropostaDecisao

logger = logging.getLogger(__name__)

# Parâmetros Normativos e Pedagógicos de Referência
LIMITE_AVARIA_ALERTA = 0.15      # 15% de itens danificados/inservíveis dispara alerta
CAPACIDADE_ESTIMADA_SALA = 30   # Capacidade média de alunos por sala de aula padrão
TAXA_OCIOSIDADE_ALERTA = 0.50   # 50% de ociosidade dispara recomendação de remanejamento


def diagnosticar_infraestrutura() -> Dict[str, Any]:
    """
    Executa diagnóstico analítico determinístico sobre os ambientes físicos e o patrimônio da instituição.
    
    Retorna métricas consolidadas sobre:
    - Estado de conservação patrimonial por ambiente
    - Ambientes ociosos ou desprovidos de mobiliário
    - Disponibilidade de laboratórios e equipamentos de TI
    - Taxa de avaria física
    """
    ambientes_qs = Ambiente.objects.select_related('unidade').all()
    total_ambientes = ambientes_qs.count()

    total_patrimonio = ItemPatrimonio.objects.count()
    itens_em_bom_estado = ItemPatrimonio.objects.filter(estado_conservacao__in=['NOVO', 'BOM', 'REGULAR']).count()
    itens_avariados = ItemPatrimonio.objects.filter(estado_conservacao__in=['DANIFICADO', 'INSERVIVEL']).count()

    indice_avaria_global = (itens_avariados / total_patrimonio) if total_patrimonio > 0 else 0.0

    detalhes_ambientes = []
    alertas = []
    ambientes_ociosos = []
    ambientes_criticos_avaria = []

    for amb in ambientes_qs:
        itens_amb = ItemPatrimonio.objects.filter(ambiente=amb)
        qtd_total = itens_amb.count()
        qtd_avariados = itens_amb.filter(estado_conservacao__in=['DANIFICADO', 'INSERVIVEL']).count()
        qtd_operacionais = qtd_total - qtd_avariados

        taxa_avaria = (qtd_avariados / qtd_total) if qtd_total > 0 else 0.0

        # Classificação do perfil do ambiente pelo nome
        nome_lower = amb.nome.lower()
        eh_sala_aula = "sala" in nome_lower and "reuniao" not in nome_lower and "professores" not in nome_lower
        eh_lab = "lab" in nome_lower or "informatica" in nome_lower
        eh_biblioteca = "biblio" in nome_lower

        tipo_estimado = "SALA_AULA" if eh_sala_aula else ("LABORATORIO" if eh_lab else ("BIBLIOTECA" if eh_biblioteca else "ADMINISTRATIVO"))

        info_amb = {
            "id": amb.id,
            "nome": amb.nome,
            "tipo_estimado": tipo_estimado,
            "total_itens": qtd_total,
            "itens_operacionais": qtd_operacionais,
            "itens_avariados": qtd_avariados,
            "taxa_avaria_pct": round(taxa_avaria * 100, 1),
            "status": "OPERACIONAL"
        }

        # Verificação de anomalias
        if qtd_total == 0 and (eh_sala_aula or eh_lab):
            info_amb["status"] = "DESPROVIDO_MOBILIARIO"
            ambientes_ociosos.append(info_amb)
            alertas.append({
                "ambiente": amb.nome,
                "severidade": "MEDIA",
                "mensagem": f"Ambiente pedagógico '{amb.nome}' está sem nenhum item de patrimônio/mobiliário cadastrado."
            })
        elif taxa_avaria >= LIMITE_AVARIA_ALERTA:
            info_amb["status"] = "ALERTA_MANUTENCAO"
            ambientes_criticos_avaria.append(info_amb)
            alertas.append({
                "ambiente": amb.nome,
                "severidade": "ALTA",
                "mensagem": f"Ambiente '{amb.nome}' apresenta {info_amb['taxa_avaria_pct']}% de itens danificados/inservíveis ({qtd_avariados} de {qtd_total})."
            })

        detalhes_ambientes.append(info_amb)

    # Análise de alocação de grade e turmas ativas
    grades_qs = GradeHorario.objects.select_related('turma', 'disciplina').all()
    total_aulas_semana = grades_qs.count()
    turmas_com_grade = grades_qs.values('turma_id').distinct().count()

    return {
        "total_ambientes": total_ambientes,
        "total_patrimonio": total_patrimonio,
        "itens_operacionais": itens_em_bom_estado,
        "itens_avariados": itens_avariados,
        "indice_avaria_global_pct": round(indice_avaria_global * 100, 1),
        "total_aulas_semana": total_aulas_semana,
        "turmas_com_grade": turmas_com_grade,
        "ambientes": detalhes_ambientes,
        "ambientes_ociosos": ambientes_ociosos,
        "ambientes_criticos_avaria": ambientes_criticos_avaria,
        "alertas": alertas,
    }


def gerar_propostas_infraestrutura(persistir: bool = True, usuario: Optional[Any] = None) -> List[PropostaDecisao]:
    """
    Gera propostas deliberativas formais (Human-in-the-Loop) para a gestão escolar,
    fundamentadas no Direito à Explicação (Art. 20 LGPD).
    
    Todas as propostas iniciam estritamente com status PENDENTE.
    """
    diag = diagnosticar_infraestrutura()
    propostas_geradas = []

    # Proposta 1: Manutenção corretiva de itens danificados em salas de aula
    for amb_critico in diag["ambientes_criticos_avaria"]:
        titulo = f"Manutenção Patrimonial e Substituição de Itens - {amb_critico['nome']}"
        descricao = (
            f"Diagnóstico: O ambiente '{amb_critico['nome']}' possui {amb_critico['itens_avariados']} "
            f"itens patrimoniais classificados como DANIFICADO ou INSERVÍVEL, correspondendo a "
            f"{amb_critico['taxa_avaria_pct']}% do seu acervo físico.\n"
            f"Recomendação: Abertura imediata de ordem de serviço para manutenção preventiva/corretiva "
            f"dos equipamentos danificados ou substituição por mobiliário da reserva técnica."
        )
        justificativa = (
            f"Em conformidade com as diretrizes do Censo Escolar/INEP quanto às condições de infraestrutura "
            f"pedagógica e segurança do ambiente escolar, manter taxas de avaria superiores a {int(LIMITE_AVARIA_ALERTA*100)}% "
            f"compromete o bem-estar dos alunos e a durabilidade do patrimônio institucional."
        )
        dados = {
            "ambiente_id": amb_critico["id"],
            "ambiente_nome": amb_critico["nome"],
            "total_itens": amb_critico["total_itens"],
            "itens_avariados": amb_critico["itens_avariados"],
            "taxa_avaria_pct": amb_critico["taxa_avaria_pct"],
            "acao_sugerida": "MANUTENCAO_OU_SUBSTITUICAO"
        }

        if persistir:
            prop, criada = PropostaDecisao.objects.get_or_create(
                tipo="INFRAESTRUTURA",
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
                tipo="INFRAESTRUTURA",
                titulo=titulo,
                descricao=descricao,
                justificativa=justificativa,
                dados_proposta=dados,
                status="PENDENTE"
            ))

    # Proposta 2: Ativação e equipagem de salas de aula ociosas
    for amb_ocioso in diag["ambientes_ociosos"]:
        titulo = f"Equipagem e Ativação de Sala Ociosa - {amb_ocioso['nome']}"
        descricao = (
            f"Diagnóstico: O ambiente '{amb_ocioso['nome']}' está cadastrado como espaço pedagógico, "
            f"porém consta com 0 itens de patrimônio/mobiliário vinculados no inventário.\n"
            f"Recomendação: Alocar carteiras, mesa de professor e quadro a partir de transferências "
            f"do almoxarifado ou aquisição planejada, permitindo a utilização da sala para divisão de turmas."
        )
        justificativa = (
            f"A subutilização de espaço físico em períodos letivos ativos gera sobrecarga nas salas em funcionamento. "
            f"A ativação deste espaço proporciona maior flexibilidade para acolhimento de turmas desdobradas."
        )
        dados = {
            "ambiente_id": amb_ocioso["id"],
            "ambiente_nome": amb_ocioso["nome"],
            "acao_sugerida": "EQUIPAGEM_MOBILIARIO"
        }

        if persistir:
            prop, criada = PropostaDecisao.objects.get_or_create(
                tipo="INFRAESTRUTURA",
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
                tipo="INFRAESTRUTURA",
                titulo=titulo,
                descricao=descricao,
                justificativa=justificativa,
                dados_proposta=dados,
                status="PENDENTE"
            ))

    return propostas_geradas


def montar_contexto_motor_infraestrutura() -> str:
    """
    Monta bloco de contexto compacto para RAG do Motor 2.
    Contém dados agregados e determinísticos sobre infraestrutura para injeção no prompt da LLM.
    """
    diag = diagnosticar_infraestrutura()

    linhas = [
        "### DIAGNÓSTICO DO MOTOR 2 (INFRAESTRUTURA E CONSERVAÇÃO PATRIMONIAL):",
        f"- Ambientes Cadastrados: {diag['total_ambientes']} unidades | Total de Bens Inventariados: {diag['total_patrimonio']}",
        f"- Bens em Operação Adequada: {diag['itens_operacionais']} | Bens Danificados/Inservíveis: {diag['itens_avariados']} ({diag['indice_avaria_global_pct']}% de avaria global)",
        "- Situação dos Ambientes Físicos:"
    ]

    for amb in diag["ambientes"]:
        linhas.append(
            f"  * {amb['nome']}: {amb['total_itens']} itens ({amb['itens_operacionais']} operacionais, {amb['itens_avariados']} avariados - {amb['taxa_avaria_pct']}% avaria) - Status: {amb['status']}"
        )

    if diag["alertas"]:
        linhas.append("- Alertas do Motor de Infraestrutura:")
        for al in diag["alertas"]:
            linhas.append(f"  * [{al['severidade']}] {al['mensagem']}")

    return "\n".join(linhas)

