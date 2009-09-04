# Django imports
from django.shortcuts import render_to_response
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.core.cache import cache
from django.utils.cache import get_cache_key
from django import forms
from django.contrib.auth.decorators import login_required

# Local imports
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
def topics(request, author):
    next = request.GET.get('next')
    topics, next = Topic.topics_by_author(author, next)
    return render_to_response('topics.html', {
        'topics': topics,
        'next': next
    }, context_instance=RequestContext(request))

@login_required
def topics_new(request, author):
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = Topic(
                author=request.user.username,
                title=form.cleaned_data['title'],
                body=form.cleaned_data['body']
            )
            topic.put()
            redirect = '/'+ author + '/' + str(topic.id)
            expire_page(redirect)
            return HttpResponseRedirect(redirect)
    else:
        form = TopicForm()
    
    return render_to_response('basic_form.html', {
        'form': form,
        'title': 'Start a topic'
    }, context_instance=RequestContext(request))

def topic(request, id):
    if request.method == 'POST':
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/users/login?next=' + request.path)
        
        parent_id = request.POST['reply_to']
        if not parent_id:
            parent_id = id
        
        parent = Comment.get_by_id(int(parent_id))
        parent.add_reply(
            author=request.user.username, 
            body=request.POST['body']
        )
        expire_page('/topics/' + id)
    
    topic = Topic.get_by_id(int(id))
    return render_to_response('topic.html', {
        'topic': topic
    }, context_instance=RequestContext(request))


