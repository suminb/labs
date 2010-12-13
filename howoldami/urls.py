from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'howoldami.views.index'),
    (r'^results$', 'howoldami.views.results'),
    (r'^people/list$', 'howoldami.views.people_list'),
    (r'^person/add$', 'howoldami.views.person_add'),
    (r'^person/edit/(?P<key>[0-9A-Za-z_-]+)$', 'howoldami.views.person_edit'),
    (r'^person/view/(?P<key>[0-9A-Za-z_-]+)$', 'howoldami.views.person_view'),
    (r'^export$', 'howoldami.views.export'),
)
