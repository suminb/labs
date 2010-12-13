from django.http import *
from django.shortcuts import render_to_response
from google.appengine.api import users

from lib.frontend import *
from lib.util import *
from models import *
from forms import *

authroized_editors = (
    'suminb@gmail.com',
    'ibbycho@gmail.com',
)

def index(request):
    form = UserInfoForm()
    return render_to_response('howoldami/index.html', {'form':form})
    
def results(request, mimetype='text/html'):
    if request.method == 'GET':
        form = UserInfoForm(request.GET)
        people = None
        name = None
        if form.is_valid():
            name = form.cleaned_data['name']
            birthdate = form.cleaned_data['birthdate']
            people = Person.fetch_by_birthdate(birthdate.year, birthdate.month, birthdate.day, 3)
    
        if mimetype == 'application/json':
            return response_ok([p.to_dict() for p in people])
        else:
            return render_to_response('howoldami/results.html', {'form':form, 'people':people, 'name':name, 'birthdate':birthdate})
    else:
        return HttpResponseBadRequest()
    
def people_list(request, page=0, mimetype='text/html'):
    user = users.get_current_user()

    if not user:
        return HttpResponseRedirect(users.create_login_url('/howoldami/people/list'))
    else:
        if user.email() in authroized_editors:
            logout_url = users.create_logout_url('/howoldami')
        else:
            return HttpResponseUnauthorized('Access denied')
        
    if 'page' in request.GET:
        page = int(request.GET['page'])
    if 'mimetype' in request.GET:
        mimetype = request.GET['mimetype']
    
    people = Person.fetch_page(page, 10) # 10 people per page
    
    if mimetype == 'application/json':
        return response_ok([p.to_dict() for p in people])
    else:
        return render_to_response('howoldami/people_list.html', {'user':user, 'page':page, 'people':people})

def person_add(request):
    user = users.get_current_user()

    if not user:
        return HttpResponseRedirect(users.create_login_url('/howoldami/person/edit/%s' % key))
    else:
        if user.email() in authroized_editors:
            logout_url = users.create_logout_url('/howoldami')
        else:
            return HttpResponseUnauthorized('Access denied')
            
    if request.method == 'POST':
        form = PersonEditForm(request.POST)
        if form.is_valid():
            person = Person(name = form.cleaned_data['name'],
                            description = form.cleaned_data['description'],
                            birthdate = form.cleaned_data['birthdate'],
                            deathdate = form.cleaned_data['deathdate'],
                            sex = form.cleaned_data['sex'],
                            images = form.cleaned_data['images'].split('\n'),
                            links = form.cleaned_data['links'].split('\n'))
            person.put()
            return HttpResponseRedirect('/howoldami/people/list')
    else:
        form = PersonEditForm()
        
    return render_to_response('howoldami/person_edit.html', {'user':user, 'form':form})

def person_view(request, key):
    try:
        person = Person.get(key)
        return render_to_response('howoldami/person_view.html', {'person':person})
    except:
        return HttpResponseServerError('Could not find the person')

def person_edit(request, key):
    user = users.get_current_user()
    if not user:
        return HttpResponseRedirect(users.create_login_url('/howoldami/people/list'))
    else:
        if user.email() in authroized_editors:
            logout_url = users.create_logout_url('/howoldami')
        else:
            return HttpResponseUnauthorized('Access denied')

    if request.method == 'POST':
        form = PersonEditForm(request.POST)
        if form.is_valid():
            person = Person.get(key)
            person.name = form.cleaned_data['name']
            person.description = form.cleaned_data['description']
            person.birthdate = form.cleaned_data['birthdate']
            person.deathdate = form.cleaned_data['deathdate']
            person.sex = form.cleaned_data['sex']
            person.images = form.cleaned_data['images'].split('\n')
            person.links = form.cleaned_data['links'].split('\n')
            person.put()
    else:
        person = Person.get(key)
        form = PersonEditForm(instance=person)
    return render_to_response('howoldami/person_edit.html', {'user':user, 'logout_url':logout_url, 'form':form})

def export(request):
    user = users.get_current_user()
    if not user:
        return HttpResponseRedirect(users.create_login_url('/howoldami/export'))
    else:
        if user.email() in authroized_editors:
            logout_url = users.create_logout_url('/howoldami')
        else:
            return HttpResponseUnauthorized('Access denied')
        
    return response_ok([p.to_dict() for p in Person.all()])