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
    # for word in curse_words:
    #     value = value.replace(word, '*' * len(word))
    #     value = value.replace(word.capitalize(), '*' * len(word))
    # return value
    words = value.split()
    result = []
    for word in words:
        if word in curse_words:
            result.append(word[0] + "*" * (len(word) - 2) + word[-1])
        else:
            result.append(word)
    return " ".join(result)
