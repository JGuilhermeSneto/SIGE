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
