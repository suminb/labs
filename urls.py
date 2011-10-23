from django.conf.urls.defaults import *
from django.views.generic.simple import redirect_to
from django.conf import settings

import os

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    #(r'^static/(?P<path>.*)$', 'django.views.static.serve',
    #    {'document_root': settings.STATIC_DOC_ROOT}),
 
    (r'^$', 'default.views.index'),
    (r'^sponsors/?', 'default.views.sponsors'),
    (r'^webthumb/?', 'webthumb.views.resize'),
    
    # Single page apps
    (r'^drivers/?$', 'drivers.views.index'),
    
    #(r'^projectstatus/?', include('projectstatus.urls')),

    (r'^antitheft/?', include('antitheft.urls')),
    (r'^cambridge/?', redirect_to, {'url': '/cmabridge'}),
    (r'^cmabridge/?', include('cmabridge.urls')),
    (r'^chemtalk/?', include('chemtalk.urls')),
    (r'^cognitive/?', include('cognitive.urls')),
    (r'^finance/?', include('finance.urls')),
    (r'^gdfs/?', 'gdfs.views.intro'),
    (r'^hanja/?', include('hanja.urls')),
    (r'^howoldami/?', include('howoldami.urls')),
    (r'^hython/?', 'hython.views.intro'),
    (r'^maps/?', include('maps.urls')),
    (r'^markdown/?', include('markdown.urls')),
    (r'^incubator/?', include('incubator.urls')),
    (r'^rainbowtable/?', include('rainbowtable.urls')),
    (r'^restfuldb/?$', 'restfuldb.views.intro'),
    (r'vct/?', include('vct.urls')),
    
    (r'^training/?', include('training.urls')),
    (r'^sector7/?', include('incubator.urls')),
)
