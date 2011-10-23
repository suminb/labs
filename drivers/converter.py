
"""
This script converts a .csv file exported from Google Docs into a .js file that
contains data in a JSON format, so our frontend can display it.
"""

import csv
import json

rows = csv.DictReader(open('data.csv', 'rb'), delimiter=',', quotechar='|')

slow_drivers = filter(lambda r: r['Driver Type'] == 'Slow', rows)

print slow_drivers


fout = open('data.js', 'w')
fout.write('var data = ');
fout.write(json.dumps(slow_drivers))
fout.write(';')
fout.close();