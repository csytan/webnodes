from django.conf.urls.defaults import *

urlpatterns = patterns('apps.paypal.views',
    (r'^ipn$', 'ipn'),
)
