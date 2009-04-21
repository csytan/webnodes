from django.conf.urls.defaults import *

urlpatterns = patterns('app.views',
#   (r'^(.*)/topics'),
#   (r'^$', 'topics'),
#   (r'^topics$', 'topics'),
#   (r'^topics/new$', 'topics_new'),
#   (r'^topics/(\d+)$', 'topic'),
    (r'^$', 'topics'),
    (r'^topics$', 'topics'),
    (r'^topics/new$', 'topics_new'),
    (r'^topics/(\d+)$', 'topic'),
    (r'^comments$', 'comments'),
    (r'^reddit$', 'reddit_topics'),
    (r'^reddit/(.+)$', 'reddit_topic')
)
