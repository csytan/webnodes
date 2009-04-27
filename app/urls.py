from django.conf.urls.defaults import *

urlpatterns = patterns('app.views',
    (r'^$', 'topics'),
    (r'^topics/(\d+)$', 'topic'),
    (r'^topics/new$', 'topics_new'),
    (r'^comments$', 'comments'),
    (r'^reddit$', 'reddit_topics'),
    (r'^reddit/(.+)$', 'reddit_topic'),
    (r'^(.+)$', 'topics_by_tag'),
)
