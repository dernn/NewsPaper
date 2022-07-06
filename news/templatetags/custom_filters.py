from django import template

register = template.Library()

SWEAR_WORDS = {
    'unexpected',
    'gained—well',
    'whether',
    'baggins',
    'hobbit',
    'something',
    'редиска',

}


@register.filter()
def censor(value):
    try:
        censored_text = ''
        for word in value.split():
            if word.strip('.,:;!?').lower() in SWEAR_WORDS:
                censored_text += word[0] + '*' * len(word[1:-1]) + word[-1] + ' '
            else:
                censored_text += word + ' '
        return censored_text
    except AttributeError as e:
        return f'{e} (string only)'
