from django.conf.urls.defaults import *

urlpatterns = patterns('apps.core.views',
    (r'^$', 'index'),
    (r'^jobs$', 'translator_jobs'),
    (r'^jobs/(\d+)$', 'translator_job'),
)
