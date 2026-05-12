from django import template

from apps.ti.utils.permissoes import (
    usuario_e_apenas_ti,
    usuario_tem_operacoes_ti,
    usuario_tem_painel_ti,
)

register = template.Library()


@register.filter(name="pode_menu_ti")
def pode_menu_ti(user) -> bool:
    """Exibe entradas de menu da área de TI."""
    if not getattr(user, "is_authenticated", False):
        return False
    return usuario_tem_painel_ti(user)


@register.filter(name="apenas_perfil_ti")
def apenas_perfil_ti(user) -> bool:
    """Menu lateral compacto só para equipe TI (sem gestor/prof/aluno)."""
    if not getattr(user, "is_authenticated", False):
        return False
    return usuario_e_apenas_ti(user)


@register.filter(name="pode_ti_operacoes")
def pode_ti_operacoes(user) -> bool:
    """Link para página de operações avançadas."""
    if not getattr(user, "is_authenticated", False):
        return False
    return usuario_tem_operacoes_ti(user)
