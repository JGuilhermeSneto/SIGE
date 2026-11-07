"""
Camada de Serviços do Módulo de Inteligência Artificial do ELISE.
"""
from .llm_service import perguntar, verificar_disponibilidade_llm, PROMPT_SISTEMA
from .contexto import montar_contexto

__all__ = [
    "perguntar",
    "verificar_disponibilidade_llm",
    "PROMPT_SISTEMA",
    "montar_contexto",
]
