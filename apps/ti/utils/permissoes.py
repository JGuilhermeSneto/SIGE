"""Regras de acesso à área de TI (permissões Django + grupos)."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractUser


COD_PERM_BASICO = "ti.painel_ti_basico"
COD_PERM_OPERACOES = "ti.painel_ti_operacoes"

GRUPO_TI_OPERADOR = "TI — Operador"
GRUPO_TI_COORDENACAO = "TI — Coordenação"


def usuario_tem_painel_ti(user) -> bool:
    """Usuário ativo com permissão básica de TI ou superusuário."""
    if not getattr(user, "is_authenticated", False) or not getattr(user, "is_active", False):
        return False
    return getattr(user, "is_superuser", False) or user.has_perm(COD_PERM_BASICO)


def usuario_tem_operacoes_ti(user) -> bool:
    """Inclui operações avançadas (integrações, rotinas sensíveis)."""
    if not getattr(user, "is_authenticated", False) or not getattr(user, "is_active", False):
        return False
    return getattr(user, "is_superuser", False) or user.has_perm(COD_PERM_OPERACOES)


def usuario_e_apenas_ti(user) -> bool:
    """
    Perfil exclusivamente TI: sem painéis acadêmicos (gestor/prof/aluno).

    Usado para montar o menu lateral específico da equipe.
    """
    if not usuario_tem_painel_ti(user):
        return False
    if getattr(user, "is_superuser", False):
        return False
    if any(
        hasattr(user, attr)
        for attr in ("gestor", "professor", "aluno", "responsavel")
    ):
        return False
    return True
