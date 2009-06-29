from django.conf.urls.defaults import *

urlpatterns = patterns('apps',
    (r'^$', 'forums.views.index'),
    (r'^new_forum$', 'forums.views.new_forum'),

    (r'^users/login$', 'users.views.users_login'),
    (r'^users/logout$', 'users.views.users_logout'),
    (r'^users/(.+)$', 'forums.views.user'),
    
    (r'^(.+)/new_topic$', 'forums.views.topics_new'),
    (r'^(.+)/search$', 'forums.views.search'),
    (r'^(.+)/edit$', 'forums.views.edit_forum'),
    
    (r'^(.+)/(\d+)$', 'forums.views.topic'),
    (r'^(.+)/(\d+)/edit$', 'forums.views.topic_edit'),
    (r'^(.+)$', 'forums.views.topics'),
)
