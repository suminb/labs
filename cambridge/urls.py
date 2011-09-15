from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # 0z is a prefix for base62
    (r'^(?P<id>0z[0-9A-Za-z]+)?$', 'cambridge.views.index'),
    (r'^translate$', 'cambridge.views.lookup'),
)