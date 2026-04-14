"""
Filtros de template reutilizáveis (``get_item``, ``has_attr``, ``unlocalize``).

O que é: biblioteca registrada em ``settings.TEMPLATES`` como ``custom_tags``;
permite lógica simples nos HTML sem poluir as views.
"""

from django import template
from apps.usuarios.utils.perfis import get_foto_perfil

register = template.Library()

@register.filter(name='get_item')
def get_item(dictionary, key):
    """
    Retorna o valor de um dicionário para uma dada chave.
    Uso no template: {{ meu_dict|get_item:minha_chave }}
    """
    if dictionary is None:
        return None
    return dictionary.get(key)

@register.filter(name='has_attr')
def has_attr(obj, attr_name):
    """
    Verifica se um objeto possui um determinado atributo.
    Uso no template: {% if user|has_attr:'gestor' %}
    """
    return hasattr(obj, attr_name)

@register.filter(name='unlocalize')
def unlocalize(value):
    """
    Força a exibição de um valor sem formatação de localização (ex: 7.0 em vez de 7,0).
    """
    return str(value)


@register.filter(name="foto_perfil_url")
def foto_perfil_url(user):
    """
    Retorna a URL da foto de perfil do usuário (ou imagem padrão).
    Uso no template: {{ request.user|foto_perfil_url }}
    """
    if not user:
        return None
    return get_foto_perfil(user)
