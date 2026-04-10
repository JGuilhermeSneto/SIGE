from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
@register.filter
def has_attr(obj, attr):
    return hasattr(obj, attr)
@register.filter
def replace_chars(value, arg):
    """Substitui caracteres em uma string. Uso: {{ val|replace_chars:"_, " }}"""
    if len(arg.split(',')) != 2:
        return value
    old, new = arg.split(',')
    return value.replace(old, new)
