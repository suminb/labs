from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'cognitive.views.index'),
    (r'^tick$', 'cognitive.views.tick'),
    (r'^reset$', 'cognitive.views.reset'),
)