# status_report.py gathers necessary information to report

import sys
sys.path.append('.')

import re, shlex
import os

from subprocess import Popen, PIPE
from urllib import urlencode
from urllib2 import Request, urlopen
from django.utils import simplejson as json

report_url = 'http://localhost:8080/antitheft/statusreport'

def exec_command(command):
    args = shlex.split(command)

    p = Popen(args, stdout=PIPE)
    return p.communicate()[0]
    
def get_hostname():
    return os.uname()[1]

# Returns a two-dimensional array containing:
# [username, console/tty, time logged in]
def get_active_users():
    raw = exec_command('who').strip()
    regex = re.compile('[ ]{2,}')

    return map(lambda x: regex.split(x), raw.split('\n'))

def get_uptime():
    return exec_command('uptime')

memory_usage = exec_command('top -l 1') # | head -n 7

def get_disk_usage():
    return exec_command('df -h')

def get_processes():
    return exec_command('ps aux').strip().split('\n')

# ckrootkit

def report(data):
    req = Request(report_url, urlencode(data), {})
    f = urlopen(req)
    
    return f.read()

payload = {'hostname':get_hostname(),
        'activeusers':get_active_users(),
        'uptime':get_uptime(),
        'diskusage':get_disk_usage(),
        'processes':get_processes(),
        }

print report({'payload':json.dumps(payload)}) 
