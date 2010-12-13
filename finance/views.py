from google.appengine.api import users
#from google.appengine.ext.webapp.util import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

from models import *
from forms import *

def login_required(function=None, redirect_to='/', alc=None):
    def wrapper(function, *args, **kw):
        user = users.get_current_user()
        
        if user is not None:
            return function
        else:
            return lambda r: HttpResponseRedirect(users.create_login_url(redirect_to))

    return wrapper

def intro(request):
    if users.get_current_user() is not None:
        return HttpResponseRedirect('/finance/transaction/list')
    else:
        return render_to_response('finance/intro.html', {'login_url': users.create_login_url('/finance/transaction/list')})

@login_required('/finance/transaction/list')
def transaction_list(request):
    user = users.get_current_user()
    q = Transaction.all()
    q.filter('owner =', user)
    q.order('-timestamp')
    
    transactions = q.fetch(100)
    return render_to_response('finance/transaction_list.html',
                               {'user':user,
                                'logout_url':users.create_logout_url('/finance'),
                                'transactions':transactions})

@login_required('/finance/transaction/edit')
def transaction_edit(request, key=None):
    user = users.get_current_user()
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=db.get(key) if key else None)
        
        if form.is_valid():
            entity = form.save(commit=False)
            entity.owner = user
            entity.put()
            
            return HttpResponseRedirect('/finance')
        else:
            print 'Invalid form'
    else:
        if key == None:
            form = TransactionForm()
        else:
            transaction = Transaction.get(key)
            form = TransactionForm(instance=transaction)
            
    return render_to_response('finance/transaction_edit.html',
                              {'user':user,
                               'logout_url':users.create_logout_url('/finance'),
                               'form':form})

@login_required('/finance/transaction/import')
def transaction_import(request):
    user = users.get_current_user()
    if request.method == 'POST':
        pass
    
    else:
        return render_to_response('finance/transaction_import.html')

@login_required('/finance/account/edit')
def account_edit(request, key=None):
    user = users.get_current_user()
    if request.method == 'POST':
        form = AccountForm(request.POST)
        
        if form.is_valid():
            entity = form.save(commit=False)
            entity.owner = user
            entity.put()
            
            return HttpResponseRedirect('/finance')
        else:
            pass
    else:
        form = AccountForm(request.POST)

    return render_to_response('finance/account_edit.html', {'form':form})
