from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response

from models import *

from lib.frontend import *
from lib.markdown2 import markdown

def index(request, id=None):
    r = request.REQUEST
    
    if id != None:
        document = MarkdownDocument.get_by_id(int(id))
    else:
        document = None
    
    return render_to_response('markdown/index.html', {
        'id': id,
        'document': document,
        'query': r['q'] if 'q' in r else ''})

def lookup(request):
    if 'q' in request.REQUEST:
        query = request.REQUEST['q']
        result = markdown(query, extras=('footnotes', 'code-color',))
        
        id = None
        if query != '':
            document = MarkdownDocument(ip = request.META['REMOTE_ADDR'], content=query)
            document.put()
            
            id = document.key().id()
            
        return response_ok({'id':id, 'result':result})
    else:
        return response_error('Invalid request')
