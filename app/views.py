# Django imports
from django.shortcuts import render_to_response
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.core.cache import cache
from django.utils.cache import get_cache_key
from django import forms

from django.utils import simplejson

# Local imports
import reddit
from models import Topic, Comment

### Helper functions ###
def expire_page(path):
    request = HttpRequest()
    request.path = path
    key = get_cache_key(request)
    cache.delete(key)


### Forms ###
class TopicForm(forms.Form):
    title = forms.CharField(max_length=200)
    body = forms.CharField(max_length=500)




### Request handlers ###
def topics(request):
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            body = form.cleaned_data['body']
            topic = Topic.create(title=title, body=body)
            return HttpResponseRedirect('/topics/' + str(topic.id))
    else:
        form = TopicForm()
        
    return render_to_response('topics.html', {
        'topics': Topic.hot_topics(),
        'form': form
    })
    
def topic(request, id):
    topic = Topic.get_by_id(int(id))
    comments, graph = topic.get_comments()
    return render_to_response('topic.html', {
        'comments': comments,
        'graph': simplejson.dumps(graph),
        'root': topic.root_id
    })

def comments(request):
    if request.method == 'POST':
        parent_id = request.POST['parent_id']
        parent = Comment.get_by_id(int(parent_id))
        comment = Comment.create(
            parent=parent,
            topic=parent.topic,
            body=request.POST['body']
        )
        return HttpResponseRedirect('/topics/' + str(parent.topic.id))
        

def reddit_topics(request):
    return render_to_response('topics.html', {
        'topics': reddit.hot_topics()
    })

def reddit_topic(request, id):
    context = reddit.get_thread_data(id)
    return render_to_response('topic.html', context)

