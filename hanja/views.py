 # -*- coding: utf-8

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response

from lib.frontend import *
from hanja.dict import *

def index(request):
    return HttpResponseRedirect('http://hanja.suminb.com')
#    r = request.REQUEST
#    return render_to_response('hanja/index.html',
#        {'query': r['q']} if 'q' in r else '')

def lookup(request):
    if 'q' in request.REQUEST:
        query = request.REQUEST['q']
        result = ''.join(map(lambda x: table[x] if x in table else x, query))

        return response_ok(result)
    else:
        return response_error('Invalid request')
