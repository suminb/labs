from google.appengine.api import users
from google.appengine.ext.db import djangoforms
from appengine_django.models import BaseModel

from django import forms

from datetime import date
from models import *

class ListPropertyChoice(forms.MultipleChoiceField):

    def clean(self, value):
        """ extending the clean method to work with GAE keys """
        new_value = super(ListPropertyChoice, self).clean(value)
        key_list = []
        for k in new_value:
            key_list.append(BaseModel.get(k).key())
        return key_list
    
class ChoiceForm(djangoforms.ModelForm):
    tags = forms.MultipleChoiceField(choices=(('sporty', 'Sporty'),
                                              ('comfortable', 'Comfortable'),
                                              ('luxury', 'Luxury'),
                                              ('affordable', 'Affordable'),
                                              ('feminine', 'Feminine'),
                                              ('masculine', 'Masculine'),
                                              ('ecofriendly', 'Eco-friendly'),
                                             ),
                                     widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Choice
        exclude = ('counts')
        
class QuestionForm(djangoforms.ModelForm):
    choices = ListPropertyChoice(choices=[(e.key(), e.name) for e in db.Query(Choice)])
    class Meta:
        model = Question
        widgets = {
            'choices': forms.Select,
        }

class VehicleForm(djangoforms.ModelForm):
    type = forms.ChoiceField(choices=(('sedan', 'Sedan'), ('hatchback', 'Hatchback'),
                                      ('coupe', 'Coupe'), ('convertible', 'Convertible'),
                                      ('suv', 'SUV'), ('crossover', 'Crossover'),
                                      ('wagon', 'Wagon'),
                                      ('van', 'Van/Minivan'),
                                      ('pickup', 'Pickup')))
    
    class Meta:
        model = Vehicle
        exclude = ()


class QuestionnaireForm(djangoforms.ModelForm):
    
    age = forms.IntegerField()
    type_of_phone = forms.ChoiceField(choices=(('iphone', 'iPhone'),
                                               ('blackberry', 'BlackBerry'),
                                               ('android', 'Android'),
                                               ('flip', 'Flip phone'),
                                               ('', 'Something else')))
    gender = forms.ChoiceField(choices=(('female', 'Female'),
                                        ('male', 'Male')))
#    income = forms.ChoiceField(choices=(('20000', 'Under $20,000'),
#                                        ('30000', 'Under $30,000'),
#                                        ('50000', 'Under $50,000'),
#                                        ('90000', 'Under $90,000'),
#                                        ('-1', 'Over $150,000')
#                                        )) 
    income = forms.IntegerField()
    
    class Meta:
        model = Questionnaire
        exclude = ('timestamp', 'raw_data')