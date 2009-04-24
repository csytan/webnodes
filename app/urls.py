from django.conf.urls.defaults import *

urlpatterns = patterns('app.views',
    (r'^$', 'topics'),
    (r'^topics$', 'topics'),
    (r'^topics/new$', 'topics_new'),
    (r'^topics/(\d+)$', 'topic_by_id'),
    (r'^topics/(http:\/\/.+)$', 'topic_by_url'),
    (r'^comments$', 'comments'),
    (r'^reddit$', 'reddit_topics'),
    (r'^reddit/(.+)$', 'reddit_topic')
)
