import re

from django import template
from django.template import defaultfilters

register = template.Library()

@register.filter(name='timeago')
def timeago(value, arg=None):
    timesince = defaultfilters.timesince(value, arg)
    return timesince.split(',')[0] + ' ago'
timeago.safe = False


urlfinder = re.compile('^(http:\/\/\S+)')
urlfinder2 = re.compile('\s(http:\/\/\S+)')
@register.filter('urlify_markdown')
def urlify_markdown(value):
    value = urlfinder.sub(r'<\1>', value)
    return urlfinder2.sub(r' <\1>', value)
