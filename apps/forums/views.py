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
from models import Forum, Topic, Comment

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

class ForumForm(forms.Form):
    title = forms.CharField(max_length=100)
    name = forms.CharField(max_length=50, help_text='a short name for your forum. no spaces or symbols.')
    
    def clean_name(self):
        name = self.cleaned_data['name']
        if not name:
            raise forms.ValidationError('Enter a name for your forum')
        if name != slugify(name):
            raise forms.ValidationError('Forum names may only contain letters, numbers, dashes and underscores.')
        return name
        

class ForumEditForm(forms.Form):
    title = forms.CharField(max_length=100)
    sidebar = forms.CharField(widget=forms.Textarea,
        help_text='This will be displayed in your forum sidebar.  Markdown is used for formatting.')

### Request handlers ###
def index(request):
    return topics(request, 'webnodes')

@login_required
def new_forum(request):
    if request.method == 'POST':
        form = ForumForm(request.POST)
        if form.is_valid():
            forum = Forum.get_or_insert(
                key_name=form.cleaned_data['name'],
                title=form.cleaned_data['title']
            )
            return HttpResponseRedirect('/' + forum.name)
    else:
        form = ForumForm()
    
    return render_to_response('basic_form.html', {
        'form': form,
        'title': 'Start a forum | webnodes'
    }, context_instance=RequestContext(request))


def edit_forum(request, forum):
    if request.method == 'POST':
        form = ForumEditForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/' + forum.name)
    else:
        form = ForumEditForm()
    
    return render_to_response('basic_form.html', {
        'form': form,
        'title': 'Edit forum | webnodes'
    }, context_instance=RequestContext(request))

def topics(request, forum):
    #forum = Forum.get_by_key_name('webnodes')
    next = request.GET.get('next')
    topics, next = Topic.recent_topics(forum, next)
    return render_to_response('topics.html', {
        'forum': forum,
        'topics': topics,
        'next': next
    }, context_instance=RequestContext(request))

@login_required
def topics_new(request, forum):
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            assert Forum.get_by_key_name(forum)
            topic = Topic(
                author=request.user.username,
                forum=forum,
                title=form.cleaned_data['title'],
                body=form.cleaned_data['body']
            )
            topic.put()
            redirect = '/'+ forum + '/' + str(topic.id)
            expire_page(redirect)
            return HttpResponseRedirect(redirect)
    else:
        form = TopicForm()
    
    return render_to_response('basic_form.html', {
        'form': form,
        'title': 'Start a topic | ' + forum
    }, context_instance=RequestContext(request))

def topic(request, forum, id):
    if request.method == 'POST':
        if 'reply_to' in request.POST:
            if not request.user.is_authenticated():
                return HttpResponseRedirect('/users/login?next=' + request.path)
            parent_id = request.POST['reply_to']
            parent = Comment.get_by_id(int(parent_id))
            parent.add_reply(
                author=request.user.username, 
                body=request.POST['body']
            )
            expire_page('/topics/' + id)
    
    topic = Topic.get_by_id(int(id))
    topic.load_replies()
    return render_to_response('topic.html', {
        'topic': topic,
        'forum': forum
    }, context_instance=RequestContext(request))


def topic_edit(request, forum, id):
    topic = Topic.get_by_id(int(id))
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic.edit()
            redirect = '/'+ forum + '/' + str(topic.id)
            expire_page(redirect)
            return HttpResponseRedirect(redirect)
    else:
        form = TopicForm()
    
    return render_to_response('basic_form.html', {
        'form': form
    }, context_instance=RequestContext(request))

def search(request, forum):
    return render_to_response('search.html', {
        'query': request.GET['query'],
        'forum': forum
    }, context_instance=RequestContext(request))

def user(request, username):
    return render_to_response('user.html', {
        'comments': Comment.get_by_username(username),
    }, context_instance=RequestContext(request))

