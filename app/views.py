# Django imports
from django.shortcuts import render_to_response
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.core.cache import cache
from django.utils.cache import get_cache_key

# Local imports
import reddit
import models
from lib import feedparser

### Helper functions ###
def expire_page(path):
    request = HttpRequest()
    request.path = path
    key = get_cache_key(request)
    cache.delete(key)

### Request handlers ###
def topics(request):
    feedparser._sanitizeHTML('<div><script>alert("hi");</script></div>', 'utf-8')
    
def topic(request, id):
    pass


def reddit_topics(request):
    return render_to_response('topics.html', {
        'topics': reddit.hot_topics()
    })

def reddit_topic(request, id):
    context = reddit.get_thread_data(id)
    return render_to_response('topic.html', context)

