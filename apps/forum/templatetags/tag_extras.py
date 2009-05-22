import re
import urllib
import hashlib

from django import template
from django.template import defaultfilters
from django.utils import safestring

register = template.Library()


@register.filter(name='timeago')
def timeago(value, arg=None):
    timesince = defaultfilters.timesince(value, arg)
    return timesince.split(',')[0] + ' ago'
timeago.is_safe = True


urlfinder = re.compile('^(http:\/\/\S+)')
urlfinder2 = re.compile('\s(http:\/\/\S+)')
@register.filter('markdownify')
def markdownify(value):
    import feedparser
    import markdown2
    value = urlfinder.sub(r'<\1>', value)
    value = urlfinder2.sub(r' <\1>', value)
    html = markdown2.markdown(value)
    safe_html = feedparser._sanitizeHTML(html, 'utf-8')
    return safestring.mark_safe(safe_html)
markdownify.is_safe = True


@register.filter('gravatar')
def gravatar(email, size=20, default='wavatar'):
    if not email: return default
    params = urllib.urlencode({
        'gravatar_id': hashlib.md5(email).hexdigest(),
        'default': default,
        'size': str(size)
    })
    return "http://www.gravatar.com/avatar.php?" + params