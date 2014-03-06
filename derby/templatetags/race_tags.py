from django import template

from derby.models import Race, CarAwards

register = template.Library()

@register.assignment_tag
def get_races():
    return Race.objects.all()

@register.assignment_tag
def get_awards():
    return CarAwards.objects.all()
