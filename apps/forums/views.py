# Django imports
from django.shortcuts import render_to_response
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.core.cache import cache
from django.utils.cache import get_cache_key
from django import forms
from django.utils import simplejson
from django.contrib.auth.decorators import login_required

# Local imports
import reddit
import yahoosearch
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
    name = forms.CharField(max_length=50, label='Name, shown in URL')
    
    def clean_name(self):
        name = self.cleaned_data['name']
        if not name:
            raise forms.ValidationError('Enter a name for your forum')
        if name != slugify(name):
            raise forms.ValidationError('Forum names may only contain letters, numbers, dashes and underscores.')
        return name
        
        
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

def topics(request, forum):
    #forum = Forum.get_by_key_name('webnodes')
    return render_to_response('topics.html', {
        'forum': forum,
        'sidebar': """
Links
------------
- [Start a forum](/new_forum)
- [Browse proggit](/reddit)

        """,
        'topics': Topic.recent_topics(forum)
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
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/users/login?next=' + request.path)
        parent_id = request.POST['parent_id']
        parent = Comment.get_by_id(int(parent_id))
        parent.add_reply(
            author=request.user.username, 
            body=request.POST['body']
        )
        expire_page('/topics/' + id)
    topic = Topic.get_by_id(int(id))
    return render_to_response('topic.html', {
        'topic': topic,
        'forum': forum,
        'comments': topic.comments,
        'graph': simplejson.dumps(topic.comment_graph),
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


def reddit_topics(request):
    return render_to_response('topics.html', {
        'topics': reddit.hot_topics(),
        'forum': 'reddit'
    }, context_instance=RequestContext(request))

def reddit_topic(request, id):
    data = reddit.get_thread_data(id)
    data['forum'] = 'reddit'
    return render_to_response('topic.html', data,
        context_instance=RequestContext(request))

def search(request, forum):
    data = yahoosearch.search(request.GET['query'], 
        site='http://webnodes.org/' + forum)
    return render_to_response('search.html', {
        'data': data,
    }, context_instance=RequestContext(request))

def user(request, username):
    return render_to_response('user.html', {
        'comments': Comment.get_by_username(username),
    }, context_instance=RequestContext(request))