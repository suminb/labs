from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'maps.views.intro'),
    (r'^getid/(?P<x>\d+)-(?P<y>\d+)-(?P<z>\d+)/(?P<type>.+)$', 'maps.views.getid'),
    (r'^image/(?P<digest>[0-9a-f]{40})$', 'maps.views.image_by_digest'),
    (r'^image/(?P<x>\d+)-(?P<y>\d+)-(?P<z>\d+)/(?P<type>.+)$', 'maps.views.image_by_coordinate'),
    (r'^view/(?P<x>\d+)-(?P<y>\d+)-(?P<z>\d+)/(?P<type>[^/]+)(/(?P<revision>[^/]+))?$', 'maps.views.view'),
    (r'^scan/(?P<x>\d+)-(?P<y>\d+)-(?P<z>\d+)/(?P<type>.+)$', 'maps.views.scan'),
    (r'^status$', 'maps.views.status'),
    (r'^upload$', 'maps.views.upload'),
    (r'^recon$', 'maps.views.recon'),
)
