from django.http import *
from django.shortcuts import render_to_response
from google.appengine.api import users

def index(request):
    return render_to_response('incubator/sector7.html', {'login_url':users.create_login_url('/sector7/auth')})

def auth(request):
    user = users.get_current_user()

    if user and user.email() in ('suminb@gmail.com'):
        logout_url = users.create_logout_url('/sector7')
        return HttpResponse('...')
        
    return HttpResponseUnauthorized('Access denied') 