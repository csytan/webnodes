from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', include('apps.core.urls')),
    (r'^users/', include('apps.users.urls')),
    (r'^forum/', include('apps.forum.urls')),
    (r'^', include('apps.core.urls')),
    
)
