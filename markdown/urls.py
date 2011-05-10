from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^(docs/(?P<id>[0-9A-Za-z]+))?$', 'markdown.views.index'),
    (r'^lookup$', 'markdown.views.lookup'),
)