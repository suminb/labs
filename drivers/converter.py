
"""
This script converts a .csv file exported from Google Docs into a .js file that
contains data in a JSON format, so our frontend can display it.
"""

import csv
import json

rows = csv.DictReader(open('data.csv', 'rb'), delimiter=',', quotechar='|')

slow_drivers = filter(lambda r: r['Driver Type'] == 'Slow', rows)

#map(lambda d: [d['Make'],  slow_drivers

slow_by_make = {}
for sd in slow_drivers:
    make = sd['Make']
    slow_by_make[make] = slow_by_make[make] + 1 if make in slow_by_make else 1


fout = open('data.js', 'w')
fout.write('var _data = [');
fout.write( ','.join( map(lambda d: "['%s', %d]\n" % (d, slow_by_make[d]), slow_by_make) ) )
fout.write('];')
fout.close();