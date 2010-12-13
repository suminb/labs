from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'chemtalk.views.index'),
    (r'^lookup$', 'chemtalk.views.lookup'),
)