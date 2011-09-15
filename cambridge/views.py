# -*- coding: utf-8 *-*

from django.http import *
from django.shortcuts import render_to_response

from lib.util import Base62
from cambridge import translate

def index(request, id='0'):
    r = request.REQUEST
    
    description = translate(u'물론 캠브릿지 대학에서 이런 연구가 진행되었다는 사실이 확인된 적은 없습니다. 다만 이 문구가 인터넷을 통해 퍼지기 시작했기 때문에 앱 이름을 캠브릿지라고 지은것 뿐입니다.')

    return render_to_response('cambridge/index.html', {'description':description})    
    
#    return render_to_response('markdown/index.html', {
#        'id': id,
#        'query': r['q'] if 'q' in r else ''})