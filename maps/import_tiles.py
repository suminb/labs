#!/usr/bin/env python

import os, sys
import re

from django.core.management import setup_environ

sys.path.append(os.getenv('HOME') + '/workspace/labs')
sys.path.append(os.getenv('HOME') + '/Development/workspace/labs')
import settings
setup_environ(settings)

from datetime import datetime
from maps.models import *
from maps.recon import upload, parse_metadata

def get_filelist(dir):
    filelist = []
    pattern = re.compile('^(lyrs=[hmt]@\d+&)|(v=\d+)')
    
    print 'Looking for map tiles...'
    for root, subdirs, files in os.walk(dir):
        for file in files:
            if pattern.match(file):
                filelist.append(root+'/'+file)
                
    return filelist

def process_files(filelist):
    print 'Processing tiles...'
    for filename in filelist:
        try:
            digest = digest_file(filename)
            metadata = parse_metadata(os.path.basename(filename))
            metadata['digest'] = digest

            filestat = os.stat(filename)
            metadata['date'] = datetime.fromtimestamp(filestat.st_mtime)
            metadata['size'] = filestat.st_size
    
            print 'Processing tile %s@%s (%s, %s, %s)' % (metadata['type'], metadata['revision'], metadata['x'], metadata['y'], metadata['z'])
            if digest == 'a04d1a144428407c0b7d1fa8420d281da74da8b8':
                print 'Transparent hover image. Skipping...'
            else:
                upload(open(filename, 'rb').read(), 'http://labs.sumin.us/maps/upload', metadata)
    
            # removing file when done
            os.remove(filename)
            filelist.remove(filename)
        except:
            print 'Oops, something is gone wrong (%s)' % filename
        
# puts file content into the database
def convert_file(filename):
    digest = filename.split('/')[-1]
    print 'Processing %s' % digest
    filecontent = open(filename, 'rb').read()
    
    if filecontent.find('<html>') != -1:
        print 'HTML content found. Image discarded.'
    else:
        image = MapImage(digest=digest, data=filecontent)
        image.save()
        
    os.remove(filename)

# relocating files...
#pattern = re.compile('^[0-9a-z]{40}$')
#for root, subdirs, files in os.walk('/Volumes/dev.sumin.us/data/maps/tiles/'):
#    for file in files:
#        if pattern.match(file):
#            dest = create_subdirectories(root+'/'+file, file)
#            print "%s -> %s" % (root+'/'+file, dest)
#            #os.rename(root+'/'+file, dest)
#sys.exit(0)

#def relocate_files():
#    for tile in MapTile.objects.all():
#        d = tile.digest
#        d = [d[0:2], d[2:4], d[4:6], d[:], d[:], d[:], d[:], d[:]]
#        dest = '/Volumes/dev.sumin.us/data/maps/tiles/' + tile.digest

rootdir = sys.argv[1]
while True:
   filelist = get_filelist(rootdir)
   if filelist == []: break
   print '%d tiles have found' % len(filelist)
   process_files(filelist)

# pattern = re.compile('^[0-9a-z]{40}$')
# for root, subdirs, files in os.walk(sys.argv[1]):
#     for file in files:
#         if pattern.match(file):
#             convert_file(root+'/'+file)
