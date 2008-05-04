from django.conf.urls.defaults import *

urlpatterns = patterns('coinop.views',
    (r'^engine/?$', 'engine'),
    (r'^resreg/?$', 'resolver_lookup'),
)
