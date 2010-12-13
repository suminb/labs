#from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
#import django.utils.simplejson as json

#from base64 import *
#from datetime import datetime
#from random import randint

#from lib.frontend import *
#from lib.util import *
#from maps.recon import download as recon_download
#from maps.recon import upload as recon_upload
#from models import *

def intro(request):
    return render_to_response('maps/intro.html', {})

# def status(request):
#     return response_ok(MapTile.objects.count())
# 
# 
# def getid(request, x, y, z, type):
#     try:
#         tile = MapTile.objects.filter(x=x, y=y, z=z, type=type).order_by('-revision')
#         if len(tile) > 0:
#             tile = tile[0]
#         else:
#             return response_ok({'id':0})
# 
#     except Exception as e:
#         return response_error(e)
#     
#     return response_ok({'id':tile.id, 'digest':tile.digest})
# 
# def image_by_digest(request, digest):
#     try:
#         image = MapImage.objects.get(digest=digest)
#         return HttpResponse(image.data, mimetype="image/jpeg")
#     except MapImage.DoesNotExist:
#         raise Http404
#     except Exception as e:
#         return response_error(e.message)
#         
# def image_by_coordinate(request, x, y, z, type, revision=0):
#     try:
#         tile = MapTile.objects.filter(x=x, y=y, z=z, type=type).order_by('-revision')[0]
#         image = MapImage.objects.get(digest=tile.digest)
#         return HttpResponse(image.data, mimetype="image/jpeg")
#     except MapTile.DoesNotExist:
#         raise Http404
#     except MapImage.DoesNotExist:
#         raise Http404
#     except Exception as e:
#         return response_error(e.message)
# 
# 
# def view(request, x, y, z, type, revision):
#     n = 4
#     x = int(x)
#     y = int(y)
# 
#     # empty n*n matrix
#     tiles = [[0 for i in range(n)] for j in range(n)]
# 
#     for yi in xrange(y-(n/2), y+(n/2)):
#         for xi in xrange(x-(n/2), x+(n/2)):
#             try:
#                 tile = MapTile.objects.filter(x=xi, y=yi, z=z, type=type).order_by('-revision')[0]
#                 tiles[yi-(y-(n/2))][xi-(x-(n/2))] = tile
#             except:
#                 tiles[yi-(y-(n/2))][xi-(x-(n/2))] = None
# 
#     return render_to_response('maps/view.html', {'x':x, 'y':y, 'z':z, 'type':type, 'tiles':tiles})
#     
# # Scans a single tile
# def scan(request, x, y, z, type):
#     n = 4
#     s = 'Galileo'[:randint(1, 6)]
# 
#     if type == 's':
#         r = 63 # revision
#         url = 'http://khm%d.google.com/kh/v=%d&x=%s&y=%s&z=%s&s=%s' % (randint(0, 3), r, x, y, z, s)
#     elif type == 'm':
#         r = 128 # revision
#         url = 'http://mt%d.google.com/vt/lyrs=%s@%d&hl=en&src=api&x=%s&y=%s&z=%s&s=%s' % (randint(0, 3), type, r, x, y, z, s)
#     elif type == 't':
#         r = 125
#         url = 'http://mt%d.google.com/vt/lyrs=t@125,r@128&hl=en&src=api&x=%s&y=%s&z=%s&s=%s' % (randint(0, 3), x, y, z, s)
#     else:
#         return response_error('Unknown type')
# 
#     try:
#         metadata = {'x':x, 'y':y, 'z':z, 'type':type, 'revision':str(r)}    
#         image = recon_download(url)
#         recon_upload(image, 'http://labs.sumin.us/maps/upload', metadata)
#     except Exception as e:
#         print e
#                 
#     return response_ok({'x':x, 'y':y, 'z':z, 'type':type})
# 
# def upload(request):
#     if request.method == 'POST':
#         post = request.POST
#         filecontent = b64decode(post['file'])
#         m = json.loads(post['metadata'])
#         
#         digest = sha1(filecontent)
#         checksum = sha1('%s-%s-%s-%s-%d-%s' % (m['x'], m['y'], m['z'], m['type'], m['size'], digest))
# 
#         if checksum != post['checksum']:
#             return response_error('Invalid checksum')
#         
#         tile = None
#         try:
#             tile = MapTile.objects.get(x=m['x'], y=m['y'], z=m['z'], type=m['type'], revision=m['revision'])
#             return response_ok('Conflict found (%d, %d-%d-%d/%s). Ignoring...' % (tile.id, tile.x, tile.y, tile.z, tile.type))
# 
#         except MapTile.DoesNotExist as e:
#             tile = MapTile(date=datetime.fromtimestamp(m['date']), type=m['type'], revision=m['revision'], x=m['x'], y=m['y'], z=m['z'], digest=m['digest'])
#             tile.save()
#             
#             image = MapImage(digest=m['digest'], data=filecontent)
#             image.save()
# 
#         return response_ok(tile.id)
#     else:
#         return response_error('Invalid access')
# 
# 
# def recon(request):
#     return render_to_response('maps/recon.html', {})
