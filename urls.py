from django.conf.urls.defaults import *

urlpatterns = patterns('apps',
    (r'^$', 'forum.views.index'),
    (r'^new_group$', 'forum.views.groups_new'),

    (r'^users/login$', 'users.views.users_login'),
    #(r'^users/register$', 'users.views.users_register'),
    (r'^users/logout$', 'users.views.users_logout'),
    
    (r'^(.+)/new_topic$', 'forum.views.topics_new'),
    (r'^reddit$', 'forum.views.reddit_topics'),
    (r'^reddit/(.+)$', 'forum.views.reddit_topic'),
    (r'^(.+)/(\d+)$', 'forum.views.topic'),
    (r'^(.+)/(\d+)/edit$', 'forum.views.topic_edit'),
    (r'^(.+)/\d+/(\d+)/edit$', 'forum.views.comment_edit'),
    (r'^(.+)$', 'forum.views.topics'),
)
