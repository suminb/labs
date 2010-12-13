import sys, os
import re

from random import seed, randint

filename = sys.argv[1]
file = open(filename, 'r')
content = file.read()
file.close()

# Takes a URL of a tile image and breaks it into key-value pairs
def kv_pairs(content):
	sub = content

	m = re.search('<img src=http://mt[0-3].google.com/vt/lyrs=[^>]+', sub)
	sub = content[m.start():m.end()]

	m = re.search('lyrs', sub)
	sub = sub[m.start():]

	kv = {}
	for pair in sub.split('&amp;'):
		pair = pair.split('=')
		kv[pair[0]] = pair[1]
		
	return kv
	
# Returns a range to visit based on the given coordinate
def regions(x, y, w=5, h=3):
	r = []
	for i in xrange(y-h/2, y+(h-h/2)):
		for j in xrange(x-w/2, x+(w-w/2)):
			r.append((i, j))
	return r
	
def visit(lyrs, x, y, z, si):
	mt = randint(0, 3)
	hl = 'en'
	s = 'Galileo'
	
	url = 'http://mt%d.google.com/vt/lyrs=%s&hl=%s&x=%d&y=%d&z=%d&s=%s' % (mt, lyrs, hl, x, y, z, s[:(si % len(s))+1])
	
	print 'Visiting', url
	
i = 0
for r in regions(100, 200):
	visit('m@114', r[0], r[1], 10, i)
	i += 1




