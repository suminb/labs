#from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from lib.frontend import *

def intro(request):
    return render_to_response('training/intro.html', {})

def weather(request):
    return response_ok({'current_temperture':42,
                        'highest_temperature':43,
                        'lowest_temperature':30})
    
def contact_list(request):
    return response_ok([
        {'firstname':'Apple Store',
         'lastname':None,
         'phone':{'work':'1-800-692-7753'}},
        {'firstname':'Chase Online Banking',
         'lastname':None,
         'phone':{'work':'1-877-242-7372'}},
        {'firstname':'Steve',
         'lastname':'Jobs',
         'phone':{'mobile':'1-408-996-1010',
                  'work':'1-800-694-7466'},
         'email':{'work':'steve@mac.com'},
         'website':'http://homepage.mac.com/steve/Resume.html',
         'address':{'work':'1 Infinite Loop, Cupertino, CA 95014'}},
        {'firstname':'Jeff',
         'lastname':'Bezos',
         'occupation':'CEO of Amazon.com',
         'birthdate':'1964-01-12'}
        ])