#!/usr/bin/env python

import os, sys
import re
import json

from django.core.management import setup_environ

sys.path.append(os.getenv('HOME') + '/workspace/devsite')
sys.path.append(os.getenv('HOME') + '/Documents/workspace/devsite')
import settings
setup_environ(settings)

from math import *
from time import *
from urllib import *
from urllib2 import *
from base64 import *
from multiprocessing import Pool

from maps.models import *
from lib.util import *

server_url = 'http://labs.sumin.us/maps/'
processor_count = 2
timeout = 10
	
def get_filelist(dir):
	filelist = []
	pattern = re.compile('^(lyrs=)|(v=)')
	
	print 'Looking for map tiles...'
	for root, subdirs, files in os.walk(dir):
		for file in files:
			if pattern.match(file):
				filelist.append(root+'/'+file)
				
	return filelist


def process_file(filename, m):
	if os.path.getsize(filename) <= 0:
		print 'Found a file size of zero (%s @(%s, %s, %s)). Skipping.' % (m['type'], m['x'], m['y'], m['z'])
		return -1

	#u = urlopen(server_url + 'getid/%s-%s-%s/%s' % (m['x'], m['y'], m['z'], m['type']))
	#r = json.loads(u.read())
	
	#tile = r['results']
	
	#if r['status'] == 'ok':
	#	if tile['id'] == 0:
	#		upload(filename, server_url + 'upload', m)
	#	else:
	#		print 'Conflict found (%d). Ignoring...' % tile['id']
	#else:
	#	tile['id'] = 0
	
	return upload(filename, server_url + 'upload', m)


def process_files(filelist):
	print 'Processing %d tiles...' % len(filelist)
	for filename in filelist:
		digest = digest_file(filename)
		metadata = parse_filename(os.path.basename(filename))
		metadata['digest'] = digest
	
		filestat = os.stat(filename)
		metadata['date'] = filestat.st_mtime
		metadata['size'] = filestat.st_size
		
		print 'Processing tile %s @(%s, %s, %s)' % (metadata['type'], metadata['x'], metadata['y'], metadata['z'])
		process_file(filename, metadata)
		
		# removing file when done
		os.remove(filename)
		filelist.remove(filename)


def upload(filename, url, metadata):
	m = metadata
	
	file = open(filename, 'rb')
	filecontent = file.read()

	if filecontent.find('<html>') != -1:
		print 'Not supported message (%s @(%s, %s, %s)). Skipping.' % (m['type'], m['x'], m['y'], m['z'])
		return False
		
	filecontent = b64encode(filecontent)

	params = {'file':filecontent, 'metadata':json.dumps(m), 'checksum':None}
	checksum = sha1('%s-%s-%s-%s-%s-%s' % (m['x'], m['y'], m['z'], m['type'], m['size'], m['digest']))
	params['checksum'] = checksum
	params = urlencode(params)
	
	try:
		u = urlopen(url, params)
	except HTTPError, error:
		print "error: code=%s message=%s" % (error.code, error.msg)
		#print error.read()
		#exit(0)
		return False
	except:
		return False
	
	r = json.loads(u.read())
	if r['results']:
		print r['results']
	
	return True	
	

def partial_list(list, n):
	m = len(list)
	pl = []
	for i in range(0, n):
		p = float(m)/n
		pl.append(list[int(i*p) : int(i*p+p)])
	

	return pl


if __name__ == '__main__':
	rootdir = sys.argv[1]
	
	while True:
		filelist = get_filelist(rootdir)
		print '%d tiles have found' % len(filelist)
		n = len(filelist)
		
		if n > 0:
			timeout = 10
			for pfl in partial_list(filelist, int(ceil(n/256.0))):
				pool = Pool(processes=processor_count)
				pool.map(process_files, partial_list(pfl, processor_count))
		else:
			print 'Sleeping for %d seconds' % timeout
			sleep(timeout)
			timeout = int(timeout * 1.25)


