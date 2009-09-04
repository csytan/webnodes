from django.conf.urls.defaults import *

urlpatterns = patterns('apps.users.views',
    (r'^sign_in$', 'sign_in'),
    (r'^sign_up$', 'sign_up'),
    (r'^sign_out$', 'sign_out'),
)
