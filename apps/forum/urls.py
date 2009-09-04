from django.conf.urls.defaults import *

urlpatterns = patterns('apps.forum.views',
    (r'^$', 'topics'),
    (r'^(\d+)$', 'topic'),
    (r'^(\d+)/edit$', 'topic_edit'),
    (r'^new$', 'topics_new'),
    (r'^search$', 'search'),
)
