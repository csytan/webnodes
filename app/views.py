# Django imports
from django.shortcuts import render_to_response
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
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
    url = forms.CharField(max_length=400)
    body = forms.CharField(widget=forms.Textarea)
    tags = forms.CharField()



### Request handlers ###
def topics(request):
    if request.method == 'GET':
        if 'tag' in request.GET:
            tag = request.GET['tag']
            topics = Topic.topics_by_tag(tag)
            
        return render_to_response('topics.html', {
            'topics': Topic.hot_topics(),
            'tags': Tag.top_tags()
        })

def topics_by_tag(request, tag):
    return render_to_response('topics.html', {
        'topics': Topic.topics_by_tag(tag),
        'tags': Tag.top_tags()
    })

def topics_new(request):
    if request.method == 'GET':
        return render_to_response('topics_new.html', {
            'form': TopicForm()
        })
        
    elif request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid(): 
            tags = form.cleaned_data['tags'].split(',')
            tags = [tag.replace(' ', '') for tag in tags]
            
            topic = Topic.create(
                url=form.cleaned_data['url'],
                title=form.cleaned_data['title'],
                body=form.cleaned_data['body'],
                tags=tags
            )
            
            redirect = '/topics/' + str(topic.id)
            expire_page(redirect)
            return HttpResponseRedirect(redirect)

def topic_by_url(request, url):
    topic = Topic.get_by_url(url)
    comments, graph = topic.comment_graph()
    return render_to_response('topic.html', {
        'comments': comments,
        'graph': simplejson.dumps(graph),
        'root': topic.root_id
    })

def topic_by_id(request, id):
    topic = Topic.get_by_id(int(id))
    comments, graph = topic.comment_graph()
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
        topic = comment.topic
        redirect = '/topics/' + str(topic.id)
        expire_page(redirect)
        return HttpResponseRedirect(redirect)



def reddit_topics(request):
    return render_to_response('reddit_topics.html', {
        'topics': reddit.hot_topics()
    })

def reddit_topic(request, id):
    context = reddit.get_thread_data(id)
    return render_to_response('topic.html', context)

