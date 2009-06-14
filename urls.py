from django.conf.urls.defaults import *

urlpatterns = patterns('apps',
    (r'^$', 'forums.views.index'),
    (r'^new_forum$', 'forums.views.new_forum'),

    (r'^users/login$', 'users.views.users_login'),
    (r'^users/register$', 'users.views.users_new'),
    (r'^users/logout$', 'users.views.users_logout'),
    (r'^users/(.+)$', 'forums.views.user'),
    
    (r'^(.+)/new_topic$', 'forums.views.topics_new'),
    
    (r'^reddit$', 'forums.views.reddit_topics'),
    (r'^reddit/(.+)$', 'forums.views.reddit_topic'),
    (r'^(.+)/(\d+)$', 'forums.views.topic'),
    (r'^(.+)/(\d+)/edit$', 'forums.views.topic_edit'),
    (r'^(.+)$', 'forums.views.topics'),
)
