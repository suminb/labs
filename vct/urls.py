from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'vct.views.intro'),
    (r'^questions', 'vct.views.questions'),
    (r'^session', 'vct.views.session'),
    (r'^result', 'vct.views.result'),
    
    # admin pages
    (r'^choice/list', 'vct.views.choice_list'),
    (r'^choice/(add|edit/(?P<key>[0-9A-Za-z_-]+))', 'vct.views.choice_edit'),
    (r'^question/list', 'vct.views.question_list'),
    (r'^question/(add|edit/(?P<key>[0-9A-Za-z_-]+))', 'vct.views.question_edit'),
    (r'^vehicle/list', 'vct.views.vehicle_list'),
    (r'^vehicle/(add|edit/(?P<key>[0-9A-Za-z_-]+))', 'vct.views.vehicle_edit'), # add or edit
    #(r'^vct/add$', 'finance.views.account_edit'),
)
