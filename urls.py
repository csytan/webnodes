from django.conf.urls.defaults import *

urlpatterns = patterns('apps',
    (r'^$', 'topics.views.topics'),
    (r'^topics/new$', 'topics.views.topics_new'),
    (r'^topics/(\d+)$', 'topics.views.topic'),
    (r'^reddit$', 'topics.views.reddit_topics'),
    (r'^reddit/(.+)$', 'topics.views.reddit_topic'),
    (r'^users/login$', 'users.views.users_login'),
    (r'^users/register$', 'users.views.users_register'),
    (r'^users/logout$', 'users.views.users_logout'),
    (r'^(.+)$', 'topics.views.topics_by_tag'),
)
