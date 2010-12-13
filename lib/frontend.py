from django.http import HttpResponse
from django.utils import simplejson as json

def response_ok(payload, default=None):
    return HttpResponse(json.dumps({'status':'ok', 'payload':payload}, default=default), mimetype='text/plain')

def response_error(message):
    return HttpResponse(json.dumps({'status':'error', 'message':message}), mimetype='text/plain')