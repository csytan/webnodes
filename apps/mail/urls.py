from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'core.urls'),

    (r'^users/sign_in$', 'users.views.sign_in'),
    (r'^users/sign_up$', 'users.views.sign_up'),
    (r'^users/sign_out$', 'users.views.sign_out'),
    
    (r'^mail/post$', 'mail.views.handle_mail'),
    
    (r'^topics/(\d+)$', 'core.views.topic'),
    (r'^topics/(\d+)/edit$', 'core.views.topic_edit'),
    
    (r'^(.+)/new$', 'core.views.topics_new'),
    (r'^(.+)/search$', 'core.views.search'),
    (r'^(.+)$', 'core.views.topics'),
)
