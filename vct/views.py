from google.appengine.api import users
#from google.appengine.ext.webapp.util import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.forms.models import inlineformset_factory

from models import *
from forms import *

def intro(request):
    return render_to_response('vct/intro.html', {})

def questions(request):
    if request.method == 'POST':
        form = QuestionnaireForm(request.POST)
        return render_to_response('vct/questions.html', {'form':form})
    else:
        form = QuestionnaireForm()
        return render_to_response('vct/questions.html', {'form':form})
    
def session(request):
    question = Question.all()[1]

    choices = map(lambda x: db.get(x), question.choices)
        
    return render_to_response('vct/session.html', {'question':question, 'choices':choices})

def choice_list(request):
    user = users.get_current_user()
    q = Choice.all()
    
    choices = q.fetch(100)
    return render_to_response('vct/choice_list.html',
                               {'user':user,
                                'logout_url':users.create_logout_url('/vct'),
                                'choices':choices})

def choice_edit(request, key):
    user = users.get_current_user()
    if request.method == 'POST':
        form = ChoiceForm(request.POST, instance=db.get(key) if key else None)
        
        if form.is_valid():
            entity = form.save(commit=True)
            
            return HttpResponseRedirect('/vct/choice/list')

    else:
        if key == None:
            form = ChoiceForm()
        else:
            choice = db.get(key)
            form = ChoiceForm(instance=choice)
            
    return render_to_response('vct/choice_edit.html',
                              {'user':user,
                               'logout_url':users.create_logout_url('/vct'),
                               'form':form})
    
def question_list(request):
    user = users.get_current_user()
    q = Question.all()
    entries = q.fetch(100)
    return render_to_response('vct/question_list.html',
                               {'user':user,
                                'logout_url':users.create_logout_url('/vct'),
                                'entries':entries})

def question_edit(request, key):
    user = users.get_current_user()
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=db.get(key) if key else None)
        
        if form.is_valid():
            entity = form.save(commit=True)
            
            return HttpResponseRedirect('/vct/question/list')
    else:
        form = QuestionForm(instance=db.get(key) if key != None else None)
        #QuestionFormSet = inlineformset_factory(Question, Choice, form=QuestionForm)
        #form = QuestionFormSet(instance=db.get(key) if key != None else None)
            
    return render_to_response('vct/question_edit.html',
                              {'user':user,
                               'logout_url':users.create_logout_url('/vct'),
                               'form':form})

def vehicle_list(request):
    user = users.get_current_user()
    q = Vehicle.all()
    
    vehicles = q.fetch(100)
    return render_to_response('vct/vehicle_list.html',
                               {'user':user,
                                'logout_url':users.create_logout_url('/vct'),
                                'vehicles':vehicles})

def vehicle_edit(request, key):
    user = users.get_current_user()
    if request.method == 'POST':
        form = VehicleForm(request.POST, instance=db.get(key) if key else None)
        
        if form.is_valid():
            entity = form.save(commit=False)
            entity.owner = user
            entity.put()
            
            return HttpResponseRedirect('/vct/vehicle/list')
    else:
        if key == None:
            form = VehicleForm()
        else:
            vehicle = Vehicle.get(key)
            form = VehicleForm(instance=vehicle)
            
    return render_to_response('vct/vehicle_edit.html',
                              {'user':user,
                               'logout_url':users.create_logout_url('/vct'),
                               'form':form})
    
def vehicle_import(request):
    pass

def vehicle_export(request):
    pass