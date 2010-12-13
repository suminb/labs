#!/usr/bin/env python

import os, sys
import re

from django.core.management import setup_environ

sys.path.append(os.getenv('HOME') + '/workspace/devsite')
sys.path.append(os.getenv('HOME') + '/Development/workspace/devsite')
import settings
setup_environ(settings)

from datetime import datetime
from maps.models import *

def process_entry(entry):
    if re.match('^[a-z]@[0-9]+$', entry.type):
        tr = entry.type.split('@')
        entry.type = tr[0]
        entry.revision = tr[1]
        entry.save()
        print '(type, revision)@%d = (%s, %s)' % (entry.id, entry.type, entry.revision)
    elif re.match('^[0-9]+$', entry.type):
        entry.revision = entry.type
        entry.type = 's'
        entry.save()
        print '(type, revision)@%d = (%s, %s)' % (entry.id, entry.type, entry.revision)
    elif re.match('^(w2p|kr1p?|app)[.][0-9]+$', entry.type):
        tr = entry.type.split('.')
        entry.type = tr[0]
        entry.revision = tr[1]
        entry.save()
        print '(type, revision)@%d = (%s, %s)' % (entry.id, entry.type, entry.revision)
    elif re.match('^([hmysp]|w2p|kr1p?|app)$', entry.type):
        pass
    else:
        print 'Unknown entry type %s (%d)' % (entry.type, entry.id)
        sys.exit(1)
        
def process_all():
    for i in xrange(733, 1000+1):
        for entry in MapTile.objects.all()[i*10000:(i+1)*10000]:
            process_entry(entry)
        


#MapTile.objects.filter(type='app.115').update(type='app', revision='115')

#MapTile.objects.filter(type='w2p.114').update(type='w2p', revision='114')

#MapTile.objects.filter(type='kr1.11').update(type='kr1', revision='11')
#MapTile.objects.filter(type='kr1p.11').update(type='kr1p', revision='11')

#MapTile.objects.filter(type='m@114').update(type='m', revision='114')
#MapTile.objects.filter(type='m@115').update(type='m', revision='115')
#MapTile.objects.filter(type='m@116').update(type='m', revision='116')

#MapTile.objects.filter(type='h@114').update(type='h', revision='114')
#MapTile.objects.filter(type='h@115').update(type='h', revision='115')
#MapTile.objects.filter(type='h@116').update(type='h', revision='116')

# MapTile.objects.filter(type='49').update(type='s', revision='49')
# MapTile.objects.filter(type='50').update(type='s', revision='50')
# MapTile.objects.filter(type='51').update(type='s', revision='51')
# MapTile.objects.filter(type='52').update(type='s', revision='52')
# MapTile.objects.filter(type='53').update(type='s', revision='53')
# MapTile.objects.filter(type='54').update(type='s', revision='54')
# MapTile.objects.filter(type='61').update(type='s', revision='61')

process_all()