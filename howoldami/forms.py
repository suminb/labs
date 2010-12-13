from django import forms
from google.appengine.ext.db import djangoforms
from datetime import date
from models import *

class UserInfoForm(forms.Form):
    name = forms.CharField(label='Your Name', max_length=100)
    birthdate = forms.DateField(label='Your Birthday', initial=date.today)

class PersonEditForm(djangoforms.ModelForm):
    name = forms.CharField(label='', max_length=255)
    description = forms.CharField(widget=forms.Textarea, required=False)
    birthdate = forms.DateField(label='Date of Birth', initial=date.today)
    deathdate = forms.DateField(label='Date of Death', required=False)
    sex = forms.ChoiceField(choices=(('female','Female'), ('male','Male'), ('na', 'N/A')))
    images = forms.CharField(widget=forms.Textarea, required=False)
    links = forms.CharField(widget=forms.Textarea, required=False)
    #group = db.ReferenceProperty()
    
    class Meta:
        model = Person
        exclude = ['group']
