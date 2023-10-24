from django import template

register = template.Library()

curse_words = [
    'редиска',
    'мандарин',
    'банан',
    'флюгегенхаймен',
    ]


@register.filter()
def censor(value):
    if not isinstance(value, str):
        raise ValueError('The censor filter only applies to string variables.')
    for word in curse_words:
        value = value.replace(word, '*' * len(word))
        value = value.replace(word.capitalize(), '*' * len(word))
    return value
