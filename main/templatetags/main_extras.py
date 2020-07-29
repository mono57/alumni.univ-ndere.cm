from django import template
from main.models import Inscription


register = template.Library()

@register.simple_tag(name='event_register')
def event_register(user, event):
    return str(Inscription.objects.filter(alumni=int(user),event=int(event)).exists())