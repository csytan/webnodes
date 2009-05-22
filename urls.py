from django.conf.urls.defaults import *

urlpatterns = patterns('apps',
    (r'^$', 'forum.views.groups'),
    (r'^groups_new$', 'forum.views.groups_new'),


    (r'^reddit$', 'forum.views.reddit_topics'),
    (r'^reddit/(.+)$', 'forum.views.reddit_topic'),
    (r'^users/login$', 'users.views.users_login'),
    (r'^users/register$', 'users.views.users_register'),
    (r'^users/logout$', 'users.views.users_logout'),
    
    (r'^(.+)/new_topic$', 'forum.views.topics_new'),
    (r'^(.+)/(\d+)$', 'forum.views.topic'),
    (r'^(.+)$', 'forum.views.topics'),
)
