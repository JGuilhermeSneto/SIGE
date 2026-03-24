from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


<<<<<<< HEAD
from django import template

register = template.Library()


=======
>>>>>>> b8aef382adc558a120b5f300463536a3c6df9e01
@register.filter
def has_attr(obj, attr):
    return hasattr(obj, attr)
