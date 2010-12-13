from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'training.views.intro'),
    (r'^weather$', 'training.views.weather'),
    (r'^contact/list$', 'training.views.contact_list'),
)
