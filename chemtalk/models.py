from django.db import models
import re

lookup_table = ('', 'h', 'he', 'li', 'be', 'b', 'c', 'n', 'o', 'f', 'ne',
    'na', 'mg', 'al', 'si', 'p', 's', 'cl', 'ar', 'k', 'ca',
    'sc', 'ti', 'v', 'cr', 'mn', 'fe', 'co', 'ni', 'cu', 'zn',
    'ga', 'ge', 'as', 'se', 'br', 'kr', 'rb', 'sr', 'y', 'zr',
    'nb', 'mo', 'tc', 'ru', 'rh', 'pd', 'ag', 'cd', 'in', 'sn',
    'sb', 'te', 'i', 'xe', 'cs', 'ba', 'la', 'ce', 'pr', 'nd',
    'pm', 'sm', 'eu', 'gd', 'tb', 'dy', 'ho', 'er', 'tm', 'yb',
    'lu', 'hf', 'ta', 'w', 're', 'os', 'ir', 'pt', 'au', 'hg',
    'tl', 'pb', 'bi', 'po', 'at', 'rn', 'fr', 'ra', 'ac', 'th',
    'pa', 'u', 'np', 'pu', 'am', 'cm', 'bk', 'cf', 'es', 'fm',
    'md', 'no', 'lr', 'rf', 'db', 'sg', 'bh', 'hs', 'mt', 'ds',
    'rg', 'cn', 'uut', 'uuq', 'uup', 'uuh', 'uus', 'uuo')

subtraction_table = {
    'a':'13-17',
    'd':'60-7',
    'e':'2-1',
    'g':'12-25',
    'l':'13-91',
    'm':'62-16',
    'q':'114-92',
    'r':'36-19',
    't':'81-13',
    'x':'54-10',
    'z':'40-37',
}
# a d e g j l m q r t x z

def is_chemtalk_language(query):
    return re.match('1?[0-9]{1,2}(,(1?[0-9]{1,2}|.*))*', query)

def process_line(line):
    return ' '.join(map(process_word, line.split()))
    
def process_word(word):
    return ''.join(map(process_char, word.split(',')))

# Assumes str is in a right format.
def process_subtraction(str):
    n = map(int, str.split('-'))
    
    # Checks for the bounaries
    if n[0] < 1 or n[0] >= len(lookup_table):
        return str
    if n[1] < 1 or n[1] >= len(lookup_table):
        return str
    
    e = (lookup_table[n[0]], lookup_table[n[1]])
    return ''.join(set(e[0]) - set(e[1]))

def process_inverse(str):
    index = int(str.split('^')[0])
    return lookup_table[index][::-1]

def process_char(char):
    char = char.strip()
    if re.match('^1?[0-9]{1,2}$', char):
        index = int(char)
        if index > 0 and index < len(lookup_table):
            return lookup_table[index]
        else:
            return char
    elif re.match('^1?[0-9]{1,2}-1?[0-9]{1,2}$', char):
        return process_subtraction(char)
    elif re.match('^1?[0-9]{1,2}\\^-1$', char):
        return process_inverse(char)
    else:
        return char

def forward_lookup(source):
    return '\n'.join(map(process_line, source.split('\n')))


def investigate_word(word):
    if len(word) > 1:
        try:
            index = lookup_table.index(word)
            return (str(index), len(word))
        except:
            # lookup inverse
            try:
                index = lookup_table.index(word[::-1])
                return ('%d^-1' % index, len(word))
            except:
                return investigate_word(word[:-1])
    else:
        try:
            index = lookup_table.index(word)
            return (str(index), 1)
        except:
            if word in subtraction_table:
                return (subtraction_table[word], 1)
            else:
                return (word, 1)

def put_comma(curr, next):
    if re.match('\\d+', curr) and (next != None and (re.match('\\d+', next) or re.match('[^\\s]+', next))):
        return curr + ','
    elif re.match('[^\\s\\d]+', curr) and (next != None and re.match('\\d+', next)):
        return curr + ','
    #elif next != None and re.match('\\d+', next):
    #    return curr + ','
    else:
        return curr

def reverse_lookup(source):
    result = []
    pos = 0
    while pos < len(source):
        word, length = investigate_word(source[pos:pos+3])
        result.append(word)
        pos += length

    return ''.join(map(put_comma, result, result[1:]))
