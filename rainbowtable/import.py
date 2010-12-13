from django.core.management import setup_environ
import settings

import sys

setup_environ(settings)

from rainbowtable.views import *
#from rainbowtable.models import *

file = sys.argv[1]

for line in open(file, 'r').readlines():
    line = line.strip();
    
    hash = add_single_entry(line)
    if hash.id:
        print "'%s' already exists" % line
    else:
        print "Adding '%s'" % line
    
