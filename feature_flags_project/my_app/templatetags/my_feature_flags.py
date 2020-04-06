from django import template

from my_app.my_features import SHOW_AWESOME_TEXT_FEATURE

register = template.Library()


@register.simple_tag
def show_awesome_text() -> bool:
    return SHOW_AWESOME_TEXT_FEATURE.is_enabled()
