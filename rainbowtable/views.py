from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response

from lib.frontend import *
#from rainbowtable.models import *

import django.utils.simplejson as json
import base64, binascii
import hashlib
import struct
import re


def index(request):
    return render_to_response('rainbowtable/index.html', {})

def lookup(request):
    query = request.GET['query'].strip()
    
    if re.match('^[0-9A-Fa-f]{32}$', query):
        type = 'md5'
    elif re.match('^[0-9A-Fa-f]{40}$', query):
        type = 'sha1'
    else:
        return response_error('Unsupported format')
    
    try:
        encoded_query = base64.b64encode(binascii.a2b_hex(query))
        if type == 'md5':
            hash = Rainbowtable.objects.get(md5=encoded_query)
        elif type == 'sha1':
            hash = Rainbowtable.objects.get(sha1=encoded_query)
    except Exception:
        return response_error()
        
    return response_ok({'type':type, 'plain':hash.plain})

def add(request):
    plain = request.GET['plain']
    hash = add_single_entry(plain)    
    return response_ok({'id':hash.id,
                 'md5':hashlib.md5(plain).hexdigest(),
                 'sha1':hashlib.sha1(plain).hexdigest(),
                })

def add_single_entry(_plain):
    try:
        hash = Rainbowtable.objects.get(plain=_plain)
        return hash
    except:
        hash = Rainbowtable(plain=_plain)
    
    hash.md5 = base64.b64encode(hashlib.md5(_plain).digest())
    hash.sha1 = base64.b64encode(hashlib.sha1(_plain).digest())
    hash.save()
    
    return hash


def recent(request):
    rows = Rainbowtable.objects.order_by('-id')[:25]
    for row in rows:
        row.md5 = binascii.b2a_hex(base64.b64decode(row.md5, None))
        row.sha1 = binascii.b2a_hex(base64.b64decode(row.sha1, None))
                
    return render_to_response('rainbowtable/recent.html', {'rows':rows})