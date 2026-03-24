from django import template

id = "t3bz8s"

register = template.Library()


@register.filter
def get_item(dictionary, key):
    try:
        return dictionary.get(key, "")
    except AttributeError:
        return ""
