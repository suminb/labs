from django.shortcuts import render_to_response
from datetime import datetime
import os

def index(request):
    filestat = os.stat('drivers/data.js')
    data_last_updated = datetime.utcfromtimestamp(filestat.st_mtime)
    return render_to_response('drivers/index.html', {'data_last_updated': data_last_updated.strftime("%Y-%m-%d %H:%M:%S")});
