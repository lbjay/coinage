from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^apps/collector/?', include('collector.urls')),
    (r'^apps/coinop/?', include('coinop.urls')),
    # Example:
    # (r'^coinage/', include('coinage.foo.urls')),

    # Uncomment this for admin:
    (r'^apps/admin/', include('django.contrib.admin.urls')),
)

urlpatterns = patterns('url2ctxo.views',
    (r'^apps/url2ctxo/bookmarklet', 'bookmarklet'),
    (r'^apps/url2ctxo/?', 'url2ctxo'),
)

