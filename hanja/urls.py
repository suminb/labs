from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'hanja.views.index'),
    (r'^lookup$', 'hanja.views.lookup'),
)