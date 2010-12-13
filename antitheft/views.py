from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.utils import simplejson as json

from models import *
from lib.frontend import *

#
#
#
def log_list(request):
    pass

#
# Expects HTTP POST key-value pairs:
#
def status_report(request):
    payload = json.loads(request.POST['payload'])
    return response_ok([payload['activeusers'], request.META['REMOTE_ADDR']])
