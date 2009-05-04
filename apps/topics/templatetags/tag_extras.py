from django import template
from django.template import defaultfilters

register = template.Library()

@register.filter(name='timeago')
def timeago(value, arg=None):
    timesince = defaultfilters.timesince(value, arg)
    return timesince.split(',')[0] + ' ago'
timeago.safe = False