"""Quem pode ver o dashboard de segurança e quem pode executar ações (Shield)."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractUser


def pode_ver_dashboard_seguranca(user: AbstractUser) -> bool:
    """Superusuário, gestor (perfil) ou membro TI com permissão básica."""
    if not user.is_authenticated or not user.is_active:
        return False
    if user.is_superuser:
        return True
    if hasattr(user, "perfil") and getattr(user, "perfil", None) == "gestor":
        return True
    from apps.ti.utils.permissoes import usuario_tem_painel_ti

    return usuario_tem_painel_ti(user)


def pode_executar_acoes_seguranca(user: AbstractUser) -> bool:
    """Bloquear IP, manutenção, limpar logs, alterar bugs — TI coordenação ou gestores."""
    if not user.is_authenticated or not user.is_active:
        return False
    if user.is_superuser:
        return True
    if hasattr(user, "perfil") and getattr(user, "perfil", None) == "gestor":
        return True
    from apps.ti.utils.permissoes import usuario_tem_operacoes_ti

    return usuario_tem_operacoes_ti(user)
