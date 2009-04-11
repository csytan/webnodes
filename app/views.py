# Django imports
from django.shortcuts import render_to_response
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.core.cache import cache
from django.utils.cache import get_cache_key
from django import forms

from django.utils import simplejson

# Local imports
#import reddit
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
    body = forms.CharField(widget=forms.Textarea)




### Request handlers ###
def topics(request):
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            body = form.cleaned_data['body']
            topic = Topic.create(title=title, body=body)
            redirect = '/topics/' + str(topic.id)
            expire_page(redirect)
            return HttpResponseRedirect(redirect)
    
    return render_to_response('topics.html', {
        'topics': Topic.hot_topics()
    })
    
def topics_new(request):
    return render_to_response('topics_new.html', {
        'form': TopicForm()
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
        comment = parent.add_reply(request.POST['body'])
        return HttpResponseRedirect('/topics/' + str(comment.topic.id))
        

def reddit_topics(request):
    return render_to_response('reddit_topics.html', {
        'topics': reddit.hot_topics()
    })

def reddit_topic(request, id):
    context = reddit.get_thread_data(id)
    return render_to_response('topic.html', context)

