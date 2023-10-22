from django import template

register = template.Library()


@register.filter(name='multiply')
def multiply(value, arg):
    return str(value) * arg


@register.filter(name='censor')
def censor(value):
    words_for_cens = ['lorem', 'ipsum', 'sed', 'nulla']
    value = str(value)
    for i in words_for_cens:
        lenght = len(i)
        value = value.replace(i, '*' * lenght)
    return value


@register.filter(name='get_parent_uri')
def get_parent_uri(value):
    return value[:-1][::-1].split('/', 1)[1][::-1]
