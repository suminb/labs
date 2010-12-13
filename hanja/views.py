from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response

from lib.frontend import *
from hanja.dict import *

def index(request):
    return render_to_response('hanja/index.html', {})

def lookup(request):
    if request.method == 'POST':
        post = request.POST
        query = post['query']
        result = ''.join(map(lambda x: table[x] if x in table else x, query))

        return response_ok(result)
    else:
        return response_error('Invalid request')
