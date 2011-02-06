from django.http import HttpResponse
from google.appengine.api import images
from urllib2 import urlopen

def resize(request):
    url = request.GET['url']
    f = urlopen(url)
    image = f.read()
    f.close()
    
    thumbnail = images.resize(image, 512, 512)
    
    return HttpResponse(thumbnail, mimetype="image/jpeg")