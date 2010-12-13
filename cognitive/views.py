from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response

from lib.util import *
from cognitive.models import *

from random import randint


def index(request):
    if request.session.get('universe', None) == None:
        request.session['universe'] = Universe()

    return render_to_response('cognitive/index.html', {})

def tick(request):
    universe = request.session.get('universe', None)
    
    if universe == None:
        return ajax_error('Uninitialized universe')
    
    observer = universe.observer
    observer.decide_next_move()
    
    # save
    request.session['universe'] = universe
    
    return ajax_ok({'universe':universe.dump()})

def reset(request):
    if request.session.get('universe', None) != None:
        # Holy shit! Resetting out(?) universe!
        del request.session['universe']
        
    return ajax_ok(None)