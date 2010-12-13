from google.appengine.api import users
from google.appengine.ext.db import djangoforms
from django import forms
from datetime import date
from models import *

class AccountForm(djangoforms.ModelForm):
    class Meta:
        model = Account
        exclude = ('owner')

class TransactionForm(djangoforms.ModelForm):
    currency = forms.ChoiceField(choices=(('usd', 'USD'), ('krw', 'KRW'), ('jpn', 'JPN')))
    
    # TODO: This isn't working. Needs to be revised.
    def __init__(self, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        
        # By looking at the source code of google.appengine.ext.db.djangoforms
        # at http://code.google.com/p/googleappengine/source/browse/trunk/google/appengine/ext/db/djangoforms.py?spec=svn41&r=41
        # I figured it must be .query instead of .queryset.
        self.fields['account'].query = Account.all().filter('owner =', users.get_current_user())
    
    class Meta:
        model = Transaction
        exclude = ('owner')
