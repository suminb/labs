from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response

from models import *
from lib.frontend import *

from random import randint
import re

def index(request):
    examples = (
        '1,109-12,43-20,15,://,13-18,13-81,5,16,.,16,92,62-16,53,7,.,92,51-5,/,6,2,109,13,19', # http://labs.sumin.us/chemtalk
        '16,92,100-9,53,7 70^-1,2-1,8,7', # sumin byeon
        '63,41,53,81-13 71,23,16 6,2,109,13,19', # eunbit luvs chemtalk
        '92 37-5,8,6,19,!', # u rock!
        '20-6,5,48,26^-1,80^-1,53,j,19,13-18,61-15,102,15,114-79,38^-1,109-25,92,23,74,54-2,39,30-7', # abcdefghijklmnopqrstuvwxyz
    )
    return render_to_response('chemtalk/index.html', {'example':examples[randint(0, len(examples)-1)]})

def lookup(request):
    if request.method == 'POST':
        post = request.POST
        query = post['query'].strip().lower()
        
        if is_chemtalk_language(query):
            result = forward_lookup(query)
        else:
            result = reverse_lookup(query)
        
        return response_ok(result)
    else:
        return response_error('Invalid request')

