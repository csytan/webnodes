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
    body = forms.CharField(widget=forms.Textarea)
    tags = forms.CharField()




### Request handlers ###
def topics(request):
    if request.method == 'GET':
        if 'tags' in request.GET:
            tags = request.GET['tags']
            tags = [tag.replace(' ', '') for tag in tags.split(',')]
            topics = Topic.topics_by_tags(tags)
        else:
            topics = Topic.hot_topics()
            
        return render_to_response('topics.html', {
            'topics': topics,
            'tags': Tag.top_tags()
        })
        
    elif request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            body = form.cleaned_data['body']
            tags = form.cleaned_data['tags'].split(',')
            tags = [tag.replace(' ', '') for tag in tags]
            
            topic = Topic.create(title=title, body=body, tags=tags)
            
            redirect = '/topics/' + str(topic.id)
            expire_page(redirect)
            return HttpResponseRedirect(redirect)
    

    
def topics_new(request):
    return render_to_response('topics_new.html', {
        'form': TopicForm()
    })
    
def topic(request, id):
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
        return HttpResponseRedirect('/topics/' + str(comment.topic.id))
        

def reddit_topics(request):
    return render_to_response('reddit_topics.html', {
        'topics': reddit.hot_topics()
    })

def reddit_topic(request, id):
    context = reddit.get_thread_data(id)
    return render_to_response('topic.html', context)

