
"""
This script converts a .csv file exported from Google Docs into a .js file that
contains data in a JSON format, so our frontend can display it.
"""

import csv
import json


def write_kv_pairs(fout, varname, pairs):
    """
    @param fout File pointer
    @param varname JavaScript variable name
    @param pairs Key/value pairs to be written
    """
    fout.write('var %s = [' % varname);
    fout.write( ',\n    '.join( map(lambda k: "['%s', %d]" % (k, pairs[k]), pairs) ) )
    fout.write('];\n\n')


rows = csv.DictReader(open('data.csv', 'rb'), delimiter=',', quotechar='|')

slow_drivers = filter(lambda r: r['Driver Type'] == 'Slow', rows)

#map(lambda d: [d['Make'],  slow_drivers

slow_by_make = {}
for sd in slow_drivers:
    make = sd['Make']
    slow_by_make[make] = slow_by_make[make] + 1 if make in slow_by_make else 1
    
slow_by_sex = {}
for sd in slow_drivers:
    key = sd['Driver Sex']
    if key.strip() == '': key = 'Unknown'
    slow_by_sex[key] = slow_by_sex[key] + 1 if key in slow_by_sex else 1

fout = open('data.js', 'w')

write_kv_pairs(fout, 'byMake', slow_by_make)
write_kv_pairs(fout, 'bySex', slow_by_sex)

fout.close()
