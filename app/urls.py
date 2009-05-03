from django.conf.urls.defaults import *

urlpatterns = patterns('app.views',
    (r'^$', 'topics'),
    (r'^topics/new$', 'topics_new'),
    (r'^topics/(.+)$', 'topic'),
    (r'^comments$', 'comments'),
    (r'^reddit$', 'reddit_topics'),
    (r'^reddit/(.+)$', 'reddit_topic'),
    (r'^users/login$', 'users_login'),
    (r'^(.+)$', 'topics_by_tag'),
)
