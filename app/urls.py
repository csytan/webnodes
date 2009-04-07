from django.conf.urls.defaults import *

urlpatterns = patterns('app.views',
    (r'^$', 'reddit_topics'),
    (r'^reddit$', 'reddit_topics'),
    (r'^reddit/(.+)$', 'reddit_topic')
)
