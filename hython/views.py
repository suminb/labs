from django.http import *
from django.shortcuts import render_to_response

from lib.frontend import *

def intro(request):
    return render_to_response('hython/intro.html', {})