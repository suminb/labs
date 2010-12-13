from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response

def index(request):
    rows = [
        {'name':'Devsite',
         'last_update':'Half an hour ago',
         'status':'OK'
        },
        {'name':'Fart',
         'last_update':'5 hours ago',
         'status':'OK, Server restart requested'
        }
    ]
    return render_to_response('projectstatus/index.html', {'rows':rows})
