# -*- coding: utf-8 -*-

from random import shuffle

def is_hangul(unichr):
    return ord(unichr) >= 0x0800 and ord(unichr) <= 0xFFFF

def swap(word):
    if len(word) > 3:
        first, last = word[0], word[-1]
        if (first.isalpha() or is_hangul(first)) and (last.isalpha() or is_hangul(last)):
            middle = list(word[1:-1])
            middle.reverse() if len(word) == 4 else shuffle(middle)

            word = word[0] + ''.join(middle) + word[-1]
        
    return word

print ' '.join(map(swap, u'모든 국민은 신체의 자유를 가진다. 누구든지 법률에 의하지 아니하고는 체포·구속·압수·수색 또는 심문을 받지 아니하며, 법률과 적법한 절차에 의하지 아니하고는 처벌·보안처분 또는 강제노역을 받지 아니한다.'.split()))