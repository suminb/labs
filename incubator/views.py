from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response

from lib.frontend import *
from incubator.models import *
from base64 import encodestring, decodestring
from hashlib import md5
from time import time
from urllib import unquote
from urllib2 import *

import json
import re
import os, sys


def webarchive(request):
    get = request.REQUEST
    
    out = '/tmp/webarchive-' + request.session.session_key
    timeout = 30000 # ms

    if 'url' in get:
        url = unquote(get['url']) # possible security problem!
    else:
        return response_error('No URL is specified')

    screensize = get['screensize'] if 'screensize' in get else '1024x768'

    format = 'html'
    if 'format' in get:
        format = get['format']
        
    store = True if 'store' in get and get['store'] != '0' else False
    
    try:
        # look for an old archive
        webarchive = Webarchive.objects.get(url=url, format=format)
        data = decodestring(webarchive.data)
    except Webarchive.DoesNotExist:
        code = cutycapt(url, out, format)
    
        if code == 0:
            data = open(out, 'r').read()
        else:
            return response_error('Could not render the page')
    
        if store:    
            webarchive = Webarchive(url=url, format=format, data=encodestring(data))
            webarchive.save()
        
    if format in format_mimetype_map:
        return HttpResponse(data, mimetype=format_mimetype_map[format])
    else:
        return response_error('Unrecognized format')
    
def webarchive_thumbnail(request):
    get = request.GET
    
    url = None
    if 'url' in get:
        url = unquote(get['url'].strip())
    else:
        return response_error('No URL is specified')
    
    if not Url.is_valid_url(url):
        return response_error('Not a valid URL')
    
    if not 'size' in get:
        return response_error('Size must be specified')
    
    size = None
    if get['size'] in ('80', '128', '256', '512'):
        size = int(get['size'])
    else:
        return response_error('Invalid size')
    
    format = get['format'] if 'format' in get and get['format'] in ('png', 'jpeg') else 'png'

    url = Url.insert_if_dne(url)
    
    try:
        thumbnail = WebarchiveThumbnail.objects.get(url=url, size=size, format=format)
    except WebarchiveThumbnail.DoesNotExist:
        tmpfilename = '/tmp/webarchive' + md5(url.url).hexdigest()
        code = cutycapt(url.url, tmpfilename, 'png')
        
        if code == 0:
            thumbnail_filename = tmpfilename + '.thumb'
            make_thumbnail(tmpfilename, thumbnail_filename, (size, size), format)
        else:
            return response_error('Could not render the page')
        
        thumbnail_data = open(thumbnail_filename, 'r').read()
    
        thumbnail = WebarchiveThumbnail(url=url, size=str(size), format=format, thumbnail=encodestring(thumbnail_data))
        thumbnail.save()
        
        os.remove(tmpfilename)
        os.remove(thumbnail_filename)
    
    return HttpResponse(decodestring(thumbnail.thumbnail), mimetype=format_mimetype_map[format])


###############################################################################

def youtube(request):
    return render_to_response('incubator/youtube/index.html')

def youtube_getinfo(request):
    post = request.REQUEST
    
    if not 'url' in post or len(post['url'].strip()) == 0:
        return response_error('No URL is specified')
    
    url = post['url'].strip()
    
    if not re.match('^http://www.youtube.com/watch?', url):
        return response_error('Not a valid YouTube video URL')
  
    req = Request(url)
    req.add_header('Accept', 'application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5')
    req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_2; en-us) AppleWebKit/531.21.8 (KHTML, like Gecko) Version/4.0.4 Safari/531.21.10')
    
    try:
        page = urlopen(req)

        if page.code == 303:
            response_error('This video is unavailable')
        
        content = page.read()
    except:
        return response_error('Could not open the page')
    
    # Record the URL
    Url.insert_if_dne(url)

    r = re.search('\'SWF_ARGS\':([ ]|.)+', content)
    if r is None:
        return response_error('Malformed content')
    
    data = json.loads(content[r.start()+12:r.end()-1])
    fmt_url_map = unquote(data['fmt_url_map'])
    fmt_url_map = map(lambda x: x.split('|'), fmt_url_map.split(','))
    
    # Retrieve meta data
    try:
        r = re.search('<meta name="title" content=".*"\/?>', content)
        title = content[r.start()+28:r.end()-2]
        
        r = re.search('<meta name="description" content=".*"\/?>', content)
        description = content[r.start()+34:r.end()-2]
    except:
        return response_error('Malformed content')
    
    return response_ok({'title':title, 'description':description, 'fmt_url_map':fmt_url_map})


###############################################################################

from random import randint

def generate_mines(width, height, number_of_mines):
	# mines = [[0]*width]*height
	# Sadly, the above doesn't work because it puts the identical reference
	# to the first dimension elements.
	
	mines = [0]*height
	mines = map(lambda x: [0]*width, mines)
	
	n = 0
	while(n < number_of_mines):
		x = randint(0, width-1)
		y = randint(0, height-1)
		if mines[y][x] == 0:
			mines[y][x] = 1
			n += 1
	
	return mines
	
def count_mines(mines):
	counts = [0]*len(mines)
	counts = map(lambda x: [0]*len(x), mines)
	
	in_bounds = lambda i, j: i >= 0 and i < len(mines) and j >= 0 and j < len(mines[i])
	
	for i, row in enumerate(mines):
		for j, col in enumerate(row):
			if col != 0:
				if in_bounds(i-1, j-1): counts[i-1][j-1] += 1
				if in_bounds(i-1, j): counts[i-1][j] += 1
				if in_bounds(i-1, j+1): counts[i-1][j+1] += 1
				if in_bounds(i, j-1): counts[i][j-1] += 1
				if in_bounds(i, j+1): counts[i][j+1] += 1
				if in_bounds(i+1, j-1): counts[i+1][j-1] += 1
				if in_bounds(i+1, j): counts[i+1][j] += 1
				if in_bounds(i+1, j+1): counts[i+1][j+1] += 1
		
	return counts

def minesweeper(request):
	return render_to_response('incubator/minesweeper/index.html')

def minesweeper_init(request):
	request.session['board'] = generate_mines(10, 10, 15)
	return response_ok(request.session['board'])
	
def minesweeper_mines(request):
	return response_ok(request.session['board'] if 'board' in request.session else None)
	
def minesweeper_click(request, x, y):
	# use recursion
	return response_ok([[0,0], [1,0]])