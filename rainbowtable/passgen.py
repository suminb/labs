from django.core.management import setup_environ
import settings

setup_environ(settings)

from rainbowtable.views import *

import sys
from random import Random

rng = Random()

righthand = '123456qwertasdfgzxcvbQWERTASDFGZXCVB'#~!@#$%^'
lefthand = '7890yuiophjknmYUIPHJKLNM'#&*_+<>?:;'
allchars = righthand + lefthand

try:
    passwordLength = int(sys.argv[1])
except:
    #user didn't specify a length.  that's ok, just use 8
    passwordLength = 8
try:
    alternate_hands = sys.argv[2] == 'alt'
    if not alternate_hands:
        print "USAGE:"
        print sys.argv[0], "[length of password]",
        print "[alt (if you want the password to alternate hands]"
except:
    alternate_hands = False
    
def gen_password(length):
    password_list = []
    for i in range(length):
        if not alternate_hands:
            password_list.append(rng.choice(allchars))
        else:
            if i % 2:
                password_list.append(rng.choice(lefthand))
            else:
                password_list.append(rng.choice(righthand))
                
    password = ''.join(password_list)
    del password_list
    return password

while True:
    password = gen_password(Random().randint(6, 12))
    hash = add_single_entry(password)
    if hash.id:
        print "'%s' already exists" % password
    else:
        print "Adding '%s'" % password
        
    del password
