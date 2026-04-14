from django import template

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
