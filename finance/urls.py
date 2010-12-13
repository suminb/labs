from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'finance.views.intro'),
    (r'^transaction/list', 'finance.views.transaction_list'),
    (r'^transaction/(add|edit/(?P<key>[0-9A-Za-z_-]+))', 'finance.views.transaction_edit'), # add or edit
    (r'^account/add$', 'finance.views.account_edit'),
)
