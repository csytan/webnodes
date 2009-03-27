# Django imports
from django.shortcuts import render_to_response
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.core.cache import cache
from django.utils.cache import get_cache_key

# Local imports
import reddit


### Helper functions ###
def expire_page(path):
    request = HttpRequest()
    request.path = path
    key = get_cache_key(request)
    cache.delete(key)

### Request handlers ###
def reddit_topics(request):
    return render_to_response('topics.html', {
        'topics': reddit.hot_topics()
    })

def reddit_thread(request, id):
    context = reddit.get_thread_data(id)
    return render_to_response('thread.html', context)

