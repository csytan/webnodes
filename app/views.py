# Django imports
from django.shortcuts import render_to_response
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.core.cache import cache
from django.utils.cache import get_cache_key
from django import forms

from django.utils import simplejson

# Local imports
import reddit
from models import Topic, Comment, Tag, Group

### Helper functions ###
def expire_page(path):
    request = HttpRequest()
    request.path = path
    key = get_cache_key(request)
    cache.delete(key)


### Forms ###
class GroupForm(forms.Form):
    name = forms.CharField(max_length=200)
    url_name = forms.CharField(max_length=100)

class TopicForm(forms.Form):
    title = forms.CharField(max_length=200)
    body = forms.CharField(widget=forms.Textarea)
    tags = forms.CharField()



### Request handlers ###
def groups(request):
    if request.method == 'GET':
        return render_to_response('groups.html', {
            'groups': Group.newest_groups()
        })
        
    elif request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():            
            name = form.cleaned_data['name']
            url_name = form.cleaned_data['url_name']            
            topic = Group.get_or_insert(
                key_name=url_name, 
                name=name
            )
            expire_page('/groups')
            return HttpResponseRedirect('/groups')
    
def groups_new(request):
    return render_to_response('groups_new.html', {
        'form': GroupForm()
    })

def topics(request, group):
    if request.method == 'GET':
        if 'tag' in request.GET:
            tag = request.GET['tag']
            topics = Topic.topics_by_tag(tag, group)
        else:
            topics = Topic.hot_topics(group)
            
        return render_to_response('topics.html', {
            'topics': topics,
            'group_url': group,
            'tags': Tag.top_tags()
        })
        
    elif request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():            
            title = form.cleaned_data['title']
            body = form.cleaned_data['body']
            tags = form.cleaned_data['tags'].split(',')
            tags = [tag.replace(' ', '') for tag in tags]
            
            topic = Topic.create(
                group=group,
                title=title,
                body=body,
                tags=tags
            )
            
            redirect = '/' + group +'/topics/' + str(topic.id)
            expire_page(redirect)
            return HttpResponseRedirect(redirect)
    

def topics_new(request, group):
    return render_to_response('topics_new.html', {
        'form': TopicForm(),
        'group_url': group
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
        topic = comment.topic
        redirect = '/' + topic.group.url_name +'/topics/' + str(topic.id)
        expire_page(redirect)
        return HttpResponseRedirect(redirect)



def reddit_topics(request):
    return render_to_response('reddit_topics.html', {
        'topics': reddit.hot_topics()
    })

def reddit_topic(request, id):
    context = reddit.get_thread_data(id)
    return render_to_response('topic.html', context)

