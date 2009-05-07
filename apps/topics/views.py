# Django imports
from django.shortcuts import render_to_response
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.template import RequestContext

from django.core.cache import cache
from django.utils.cache import get_cache_key
from django import forms

from django.utils import simplejson

# Local imports
import reddit
from models import Topic, Comment, Tag


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
    tags = forms.CharField(required=False)


### Request handlers ###
def topics(request):
    return render_to_response('topics.html', {
        'topics': Topic.hot_topics(),
        'tags': Tag.top_tags()
    }, context_instance=RequestContext(request))

def topics_by_tag(request, tag):
    return render_to_response('topics.html', {
        'topics': Topic.topics_by_tag(tag),
        'tags': Tag.top_tags()
    }, context_instance=RequestContext(request))

def topics_new(request):
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            tags = form.cleaned_data['tags'].replace(' ', '').split(',')
            topic = Topic.create(
                author=request.user.username,
                title=form.cleaned_data['title'],
                body=form.cleaned_data['body'],
                tags=[tag for tag in tags if tag]
            )
            
            redirect = '/topics/' + str(topic.id)
            expire_page(redirect)
            return HttpResponseRedirect(redirect)
    else:
        form = TopicForm()
    
    return render_to_response('topics_new.html', {
        'form': form
    }, context_instance=RequestContext(request))

def topic(request, id):
    topic = Topic.get_by_id(int(id))
    comments, graph = topic.comment_graph()
    return render_to_response('topic.html', {
        'comments': comments,
        'graph': simplejson.dumps(graph),
        'root': topic.root_id
    }, context_instance=RequestContext(request))
    
def comments(request):
    if request.method == 'POST':
        parent_id = request.POST['parent_id']
        parent = Comment.get_by_id(int(parent_id))
        comment = parent.add_reply(
            author=request.user.username, 
            body=request.POST['body']
        )
        topic = comment.topic
        redirect = '/topics/' + str(topic.id)
        expire_page(redirect)
        return HttpResponseRedirect(redirect)



def reddit_topics(request):
    return render_to_response('topics.html', {
        'topics': reddit.hot_topics(),
        'reddit': True
    }, context_instance=RequestContext(request))

def reddit_topic(request, id):
    data = reddit.get_thread_data(id)
    data['reddit'] = True
    return render_to_response('topic.html', data,
        context_instance=RequestContext(request))

