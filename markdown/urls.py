from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^(?P<id>\d+)?$', 'markdown.views.index'),
    (r'^lookup$', 'markdown.views.lookup'),
)