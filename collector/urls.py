from django.conf.urls.defaults import *

urlpatterns = patterns('collector.views',
    (r'^site/?$', 'sitelist'),
    (r'^site/(?P<site>[a-z]+)/?$', 'site'),
    (r'^site/(?P<site>[a-z]+)/log/?', 'ctxolog'),
    (r'^engine/?$', 'engine'),
)
