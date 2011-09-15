from django.template.response import TemplateResponse
from django.http import *

from lib.util import Base62


def index(request, id='0'):
    r = request.REQUEST

    return TemplateResponse(request, 'index.html', {})    
    
#    return render_to_response('markdown/index.html', {
#        'id': id,
#        'query': r['q'] if 'q' in r else ''})