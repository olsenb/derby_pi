from django import template

from derby.models import Race

register = template.Library()

@register.assignment_tag
def get_races():
    return Race.objects.all()