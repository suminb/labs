from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'rainbowtable.views.index'),
    #(r'^lookup$', 'rainbowtable.views.lookup'),
    #(r'^add$', 'rainbowtable.views.add'),
    #(r'^recent$', 'rainbowtable.views.recent'),
)
