#from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response

def index(request):
    return render_to_response('default/index.html', {})
    
def sponsors(request):
    return render_to_response('default/sponsors.html', {})

#def signin(request, authroized_users=()):
#    user = users.get_current_user()
#
#    if user:
#        if authroized_users and user.email() in authoized_users:
#        pass
#        
#    return HttpResponseUnauthorized('Access denied') 