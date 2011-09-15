# -*- coding: utf-8 *-*

from django.http import *
from django.shortcuts import render_to_response

from lib.util import Base62
from lib.frontend import response_ok
from cmabridge import translate as cmabridge_translate

def index(request, id='0'):
    r = request.REQUEST
    
    # I probably should've made a custom template tag for this, but I was too lazy.
    description = cmabridge_translate(u'물론 캠브릿지 대학에서 실제로 이런 연구가 진행되었다는 사실이 확인된 적은 없습니다. 다만 이 문구가 인터넷을 통해 퍼지기 시작했기 때문에 앱 이름을 캠브릿지라고 지은것 뿐입니다.')

    return render_to_response('cmabridge/index.html', {'description':description})

def translate(request):
    if 'q' in request.GET:
        # original text to be translated
        query = request.GET['q']
        
        return response_ok({'result': cmabridge_translate(query)})
    
    return HttpResponseBadRequest()