from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response

from models import *

from lib.util import Base62
from lib.frontend import *
from lib.markdown2 import markdown

def index(request, id='0'):
    r = request.REQUEST
    
    return render_to_response('markdown/index.html', {
        'id': id,
        'query': r['q'] if 'q' in r else ''})

def lookup(request):
    if 'q' in request.REQUEST:
        query = request.REQUEST['q']
        result = markdown(query, extras=('footnotes', 'code-color',))
        
        id = 0 # null
        if query != '':
            document = MarkdownDocument(ip = request.META['REMOTE_ADDR'], content=query)
            document.put()
            
            id = document.key().id()
            
        return response_ok({'id':Base62.encode(id), 'result':result})
    elif 'id' in request.REQUEST:
        id = request.REQUEST['id']
        document = MarkdownDocument.get_by_id(Base62.decode(id))
        rendered = markdown(document.content, extras=('footnotes', 'code-color',))
        
        return response_ok({'id':id, 'raw':document.content, 'rendered':rendered})
        
    else:
        return response_error('Invalid request')
