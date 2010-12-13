from django.db import models

import re
import os
import Image

class Url(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField()
    url = models.TextField()
    
    @staticmethod
    def is_valid_url(url):
        return re.match('^((ht|f)tp(s?)\:\/\/|~/|/)?([\w]+:\w+@)?([a-zA-Z]{1}([\w\-]+\.)+([\w]{2,5}))(:[\d]{1,5})?((/?\w+/?)+|/?)(\w+\.[\w]{3,4})?((\?\w+=\w+)?(&\w+=\w+)*)?$', url.strip())
    
    @staticmethod
    def insert_if_dne(url):
        try:
            u = Url.objects.get(url=url)
        except Url.DoesNotExist:
            u = Url(url=url)
            u.save()
            
        return u
    
    class Meta:
        db_table = u'url'

class Webarchive(models.Model):
    id = models.IntegerField(primary_key=True)
    timestamp = models.DateTimeField()
    url = models.TextField()
    format = models.CharField(max_length=12)
    thumbnail = models.TextField(blank=True)
    data = models.TextField(blank=True)
    class Meta:
        db_table = u'webarchive'
        
class WebarchiveThumbnail(models.Model):
    id = models.IntegerField(primary_key=True)
    timestamp = models.DateTimeField()
    url = models.ForeignKey(Url)
    size = models.CharField(max_length=9)
    format = models.CharField(max_length=12)
    thumbnail = models.TextField()
    class Meta:
        db_table = u'webarchive_thumbnail'



format_mimetype_map = {
	'html': 'text/html',
    'png': 'image/png',
    'jpeg': 'image/jpeg',
    'pdf': 'application/pdf',
}

#
# Auxiliary functions
#
def is_executable(path):
    return os.path.exists(path) and os.access(path, os.X_OK)

def cutycapt(url, out, format, timeout=30000):
    if is_executable('/usr/bin/xvfb-run'):
        xvfb = 'xvfb-run --server-args="-screen 0, 1024x1024x24"'
    else:
        xvfb = ''

    return os.system('%s cutycapt --url="%s" --out="%s" --out-format=%s --max-wait=%d --min-width=1024' % (xvfb, url, out, format, timeout))

# size must be a tuple
# format must be one of 'png' or 'jpeg'
def make_thumbnail(infile, outfile, size, format):
    im = Image.open(infile)
    w, h = im.size
    if w > h:
        im = im.crop((w/2 - h/2, 0, w/2 + h/2, h)) 
    else:
        im = im.crop((0, 0, w, w))
    im.thumbnail(size, Image.ANTIALIAS)
    im.save(outfile, format)
