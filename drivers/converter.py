
"""
This script converts a .csv file exported from Google Docs into a JSON formated
file, so our frontend can display it.
"""

import csv

rows = csv.DictReader(open('data.csv', 'rb'), delimiter=',', quotechar='|')

for row in rows:
    print row