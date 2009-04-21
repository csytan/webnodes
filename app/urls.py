from django.conf.urls.defaults import *

urlpatterns = patterns('app.views',
    (r'^$', 'groups'),
    (r'^groups/new$', 'groups_new'),
    (r'^groups$', 'groups'),
    (r'^(.+)/topics/new$', 'topics_new'),
    (r'^(.+)/topics$', 'topics'),
    (r'^.+/topics/(\d+)$', 'topic'),
    (r'^comments$', 'comments'),
    (r'^reddit$', 'reddit_topics'),
    (r'^reddit/(.+)$', 'reddit_topic'),

    (r'^(.+)$', 'topics'),
)
