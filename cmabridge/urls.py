from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # 0z is a prefix for base62
    (r'^(?P<id>0z[0-9A-Za-z]+)?$', 'cmabridge.views.index'),
    (r'^translate$', 'cmabridge.views.translate'),
)