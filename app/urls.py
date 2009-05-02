from django.conf.urls.defaults import *

urlpatterns = patterns('app.views',
    (r'^$', 'topics'),
    (r'^topics/new$', 'topics_new'),
    (r'^topics/(.+)$', 'topic'),
    (r'^comments$', 'comments'),
    (r'^reddit$', 'reddit_topics'),
    (r'^reddit/(.+)$', 'reddit_topic'),
    (r'^users/new$', 'users_new'),
    (r'^(.+)$', 'topics_by_tag'),
)
