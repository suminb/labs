from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'antitheft.views.index'),
    (r'^statusreport$', 'antitheft.views.status_report'),
)
