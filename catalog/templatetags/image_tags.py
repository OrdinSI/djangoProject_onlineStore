from django import template

register = template.Library()


@register.simple_tag()
def image_tag(data):
    if data:
        return f'/media/{data}'
    return '#'

