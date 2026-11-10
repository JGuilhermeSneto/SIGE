"""
Camada de Serviços do Módulo de Inteligência Artificial do ELISE.
Engloba o serviço de inferência LLM (Ollama), injeção de contexto (RAG)
e os 3 motores de apoio à decisão orientados ao TCC.
"""
from .llm_service import perguntar, verificar_disponibilidade_llm, PROMPT_SISTEMA
from .contexto import montar_contexto, montar_contexto_resumo, detectar_tipo_pergunta

# Motor 1: Enturmação e Balanceamento
from .enturmacao_service import (
    diagnosticar_enturmacao,
    gerar_propostas_enturmacao,
    montar_contexto_motor_enturmacao,
)

# Motor 2: Infraestrutura e Ocupação de Salas
from .infraestrutura_service import (
    diagnosticar_infraestrutura,
    gerar_propostas_infraestrutura,
    montar_contexto_motor_infraestrutura,
)

# Motor 3: Sustentabilidade Financeira de Turmas
from .financeiro_service import (
    diagnosticar_financeiro,
    gerar_propostas_financeiro,
    montar_contexto_motor_financeiro,
)

__all__ = [
    "perguntar",
    "verificar_disponibilidade_llm",
    "PROMPT_SISTEMA",
    "montar_contexto",
    "montar_contexto_resumo",
    "detectar_tipo_pergunta",
    # Motor 1
    "diagnosticar_enturmacao",
    "gerar_propostas_enturmacao",
    "montar_contexto_motor_enturmacao",
    # Motor 2
    "diagnosticar_infraestrutura",
    "gerar_propostas_infraestrutura",
    "montar_contexto_motor_infraestrutura",
    # Motor 3
    "diagnosticar_financeiro",
    "gerar_propostas_financeiro",
    "montar_contexto_motor_financeiro",
]
