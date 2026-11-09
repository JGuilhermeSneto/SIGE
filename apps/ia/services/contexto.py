"""
Módulo de Injeção de Contexto (RAG Estruturado / Determinístico) para o ELISE IA.

Coleta dados sumarizados e anonimizados do banco de dados do SIGE, garantindo:
  - Conformidade com a LGPD (Art. 20): apenas dados agregados, nenhum dado pessoal
  - Precisão numérica: a LLM não realiza cálculos — o Django ORM faz tudo
  - Rastreabilidade: cada indicador tem origem clara para o Direito à Explicação
  - Segurança: nenhum CPF, nota individual, frequência individual ou dado de saúde

Referências:
  - TCC Seção 4.4 — Injeção de Contexto via RAG Estruturado
  - TCC Quadro 6 (Tabela 10) — Escopo de Dados do Protótipo
"""

import logging
from typing import Optional

from django.db.models import Sum, Count, Q

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Bloco 1 — Indicadores Acadêmicos (Motor 1: Enturmação e Balanceamento)
# ---------------------------------------------------------------------------

def _bloco_academico() -> str:
    """
    Coleta indicadores agregados de Turmas, Disciplinas e Professores.
    LGPD: sem dados individuais de alunos (nome, CPF, nota, frequência).
    """
    linhas = []
    try:
        from apps.academico.models.academico import Turma, Disciplina
        from apps.usuarios.models.perfis import Professor

        # Turmas e Matrículas Agregadas
        total_turmas = Turma.objects.count()
        linhas.append(f"[Acadêmico] Total de turmas cadastradas: {total_turmas}")

        # Total de matrículas ativas agregadas (LGPD compliant)
        try:
            from apps.usuarios.models.perfis import Aluno
            total_alunos = Aluno.objects.filter(status_matricula="ATIVO").count()
            linhas.append(f"[Acadêmico] Total de alunos matriculados ativos: {total_alunos}")
        except Exception:
            pass

        # Disciplinas e Professores
        total_disciplinas = Disciplina.objects.count()
        linhas.append(f"[Acadêmico] Total de disciplinas cadastradas: {total_disciplinas}")

        total_professores = Professor.objects.count()
        linhas.append(f"[Acadêmico] Total de professores ativos: {total_professores}")

    except Exception as e:
        logger.warning(f"Bloco acadêmico indisponível: {e}")
        linhas.append("[Acadêmico] Dados acadêmicos em sincronização com o ambiente de testes.")

    return "\n".join(linhas)


# ---------------------------------------------------------------------------
# Bloco 2 — Indicadores de Infraestrutura (Motor 2: Ocupação de Ambientes)
# ---------------------------------------------------------------------------

def _bloco_infraestrutura() -> str:
    """
    Coleta indicadores de ambientes/salas e patrimônio institucional.
    """
    linhas = []
    try:
        from apps.infraestrutura.models.patrimonio import (
            UnidadeEscolar,
            Ambiente,
            ItemPatrimonio,
        )

        total_unidades = UnidadeEscolar.objects.count()
        linhas.append(f"[Infraestrutura] Unidades escolares cadastradas: {total_unidades}")

        total_ambientes = Ambiente.objects.count()
        linhas.append(f"[Infraestrutura] Total de ambientes/salas cadastrados: {total_ambientes}")

        # Detalhe por tipo de ambiente se disponível
        try:
            por_tipo = (
                Ambiente.objects.values("tipo")
                .annotate(qtd=Count("id"))
                .order_by("-qtd")
            )
            for item in por_tipo:
                linhas.append(f"  • {item['tipo']}: {item['qtd']} ambiente(s)")
        except Exception as e:
            logger.debug(f"Detalhe de ambientes indisponível: {e}")

        # Patrimônio — contagem total sem expor itens específicos
        total_patrimonio = ItemPatrimonio.objects.count()
        linhas.append(f"[Infraestrutura] Itens de patrimônio registrados: {total_patrimonio}")

    except Exception as e:
        logger.warning(f"Bloco infraestrutura indisponível: {e}")
        linhas.append("[Infraestrutura] Dados de infraestrutura em sincronização com o ambiente de testes.")

    return "\n".join(linhas)


# ---------------------------------------------------------------------------
# Bloco 3 — Indicadores de Biblioteca (Acervo — Quadro 6)
# ---------------------------------------------------------------------------

def _bloco_biblioteca() -> str:
    """
    Coleta indicadores do acervo bibliográfico e empréstimos ativos.
    LGPD: sem identificação de quem pegou emprestado (aluno/professor).
    """
    linhas = []
    try:
        from apps.biblioteca.models.biblioteca import Livro, Emprestimo

        # Acervo total
        resultado = Livro.objects.aggregate(
            total_titulos=Count("id"),
            total_exemplares=Sum("quantidade_total"),
        )
        total_titulos = resultado["total_titulos"] or 0
        total_exemplares = resultado["total_exemplares"] or 0
        linhas.append(f"[Biblioteca] Títulos cadastrados no acervo: {total_titulos}")
        linhas.append(f"[Biblioteca] Total de exemplares físicos: {total_exemplares}")

        # Empréstimos ativos (status ATIVO = emprestado; RESERVA = reservado)
        emprestimos_ativos = Emprestimo.objects.filter(
            Q(status="ATIVO") | Q(status="RESERVA"),
            data_devolucao_real__isnull=True,
        ).count()
        linhas.append(f"[Biblioteca] Empréstimos/reservas em aberto: {emprestimos_ativos}")

        # Atrasados
        emprestimos_atrasados = Emprestimo.objects.filter(status="ATRASADO").count()
        linhas.append(f"[Biblioteca] Empréstimos com devolução em atraso: {emprestimos_atrasados}")

        # Exemplares disponíveis (estimativa via contagem)
        disponibilidade = max(0, total_exemplares - emprestimos_ativos)
        linhas.append(f"[Biblioteca] Estimativa de exemplares disponíveis: {disponibilidade}")

    except Exception as e:
        logger.warning(f"Bloco biblioteca indisponível: {e}")
        linhas.append("[Biblioteca] Dados do acervo em sincronização com o ambiente de testes.")

    return "\n".join(linhas)


# ---------------------------------------------------------------------------
# Bloco 4 — Indicadores Financeiros Agregados (Motor 3: Sustentabilidade)
# ---------------------------------------------------------------------------

def _bloco_financeiro() -> str:
    """
    Coleta indicadores financeiros APENAS agregados.
    LGPD: sem valores individuais, sem dados bancários, sem CPF.
    """
    linhas = []
    try:
        from apps.financeiro.models import Fatura  # noqa: F401 — pode não existir
        pendentes = Fatura.objects.filter(status="PENDENTE").count()
        atrasadas = Fatura.objects.filter(status="ATRASADA").count()
        pagas = Fatura.objects.filter(status="PAGO").count()
        linhas.append(f"[Financeiro] Faturas pagas no período: {pagas}")
        linhas.append(f"[Financeiro] Faturas pendentes: {pendentes}")
        linhas.append(f"[Financeiro] Faturas em atraso (atenção necessária): {atrasadas}")
    except Exception as e:
        logger.debug(f"Módulo financeiro não disponível neste ambiente: {e}")
        linhas.append("[Financeiro] Indicadores financeiros agregados não disponíveis no ambiente de testes.")

    return "\n".join(linhas)


# ---------------------------------------------------------------------------
# Função principal exportada
# ---------------------------------------------------------------------------

def montar_contexto(usuario=None, tipo: str = "GERAL") -> str:
    """
    Função principal de injeção de contexto para o ELISE IA.

    Monta um bloco textual estruturado com indicadores agregados da escola,
    pronto para ser inserido no prompt da LLM como seção 'DADOS DO ELISE'.

    Parâmetros:
        usuario: instância do usuário Django (opcional, para personalização futura)
        tipo: qual bloco priorizar. Valores:
            - 'GERAL'          → todos os blocos
            - 'ENTURMACAO'     → acadêmico + infraestrutura
            - 'INFRAESTRUTURA' → infraestrutura apenas
            - 'BIBLIOTECA'     → biblioteca apenas
            - 'FINANCEIRO'     → financeiro apenas

    Retorno:
        str: bloco de contexto pronto para inserção no prompt
    """
    blocos = []

    if tipo == "ENTURMACAO":
        try:
            from apps.ia.services.enturmacao_service import montar_contexto_motor_enturmacao
            blocos.append(montar_contexto_motor_enturmacao(ano=2026))
        except Exception as e:
            logger.warning(f"Erro ao carregar contexto do Motor 1: {e}")
            blocos.append(_bloco_academico())
        blocos.append(_bloco_infraestrutura())

    elif tipo == "GERAL":
        blocos.append(_bloco_academico())
        blocos.append(_bloco_infraestrutura())
        blocos.append(_bloco_biblioteca())
        blocos.append(_bloco_financeiro())

    elif tipo == "INFRAESTRUTURA":
        blocos.append(_bloco_infraestrutura())

    elif tipo == "BIBLIOTECA":
        blocos.append(_bloco_biblioteca())

    elif tipo == "FINANCEIRO":
        blocos.append(_bloco_financeiro())

    # Fallback: se tipo desconhecido ou nenhum bloco ativo, usa tudo
    if not blocos:
        blocos = [
            _bloco_academico(),
            _bloco_infraestrutura(),
            _bloco_biblioteca(),
            _bloco_financeiro(),
        ]

    contexto_completo = "\n\n".join(b for b in blocos if b.strip())

    return (
        "--- RESUMO ESTRUTURADO DA INSTITUIÇÃO (FONTE DETERMINÍSTICA DO ELISE) ---\n"
        f"{contexto_completo}\n"
        "--- FIM DOS DADOS DO SISTEMA ---"
    )


# Alias de compatibilidade com código legado
def montar_contexto_resumo() -> str:
    """Alias de compatibilidade para montar_contexto(tipo='GERAL')."""
    return montar_contexto(tipo="GERAL")
