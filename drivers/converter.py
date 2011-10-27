
"""
This script converts a .csv file exported from Google Docs into a .js file that
contains data in a JSON format, so our frontend can display it.
"""

import csv
import json
import operator
import re


def aggregate_as_pairs(rows, key):
    """
    Returns sorted list of key/value pairs, by value, in descending order.
    
    @param rows List containing raw data extracted from CSV
    @param key Field name to aggregate by (e.g. 'Make', 'Model', 'Color', etc.)
    """
    dict = {}
    for row in rows:
        k = row[key] if row[key].strip() != '' else 'Unknown'
        dict[k] = dict[k] + 1 if k in dict else 1
        
    # Sort by value
    return sorted(dict.iteritems(), key=operator.itemgetter(1), reverse=True)


def aggregate_range_data(rows, key):
    """
    Returns sorted list of key/value pairs, by key (year, age. etc), in ascending order.
    
    @param rows List containing raw data extracted from CSV
    @param key Field name to aggregate by (e.g. 'Year', 'Driver Age Group', etc.)
    """
    dict = {}
    for row in rows:
        field = row[key]
        if re.match('\d{4}-\d{4}', field):
            boundary = field.split('-')
            lower_bound, upper_bound = int(boundary[0]), int(boundary[1])
            n = upper_bound - lower_bound + 1
            
            for r in range(lower_bound, upper_bound+1):
                dict[r] = dict[r] + 1.0/n if r in dict else 1.0/n

    return sorted(dict.iteritems(), key=operator.itemgetter(0), reverse=False)
            
    
def write_kv_pairs(fout, varname, pairs):
    """
    @param fout File pointer
    @param varname JavaScript variable name
    @param pairs Key/value pairs to be written
    """
    fout.write('var %s = [' % varname);
    fout.write( ',\n    '.join( map(lambda p: "['%s', %f]" % (p[0], p[1]), pairs) ) )
    fout.write('];\n\n')

rows = csv.DictReader(open('data.csv', 'rb'), delimiter=',', quotechar='|')

slow_drivers = filter(lambda r: r['Driver Type'] == 'Slow', rows)

fout = open('data.js', 'w')

write_kv_pairs(fout, 'byYear', aggregate_range_data(slow_drivers, 'Year'))

write_kv_pairs(fout, 'byMake', aggregate_as_pairs(slow_drivers, 'Make'))
write_kv_pairs(fout, 'byBodyType', aggregate_as_pairs(slow_drivers, 'Body Type'))
write_kv_pairs(fout, 'byColor', aggregate_as_pairs(slow_drivers, 'Color'))
write_kv_pairs(fout, 'bySex', aggregate_as_pairs(slow_drivers, 'Driver Sex'))

fout.write(open('data_template.js', 'r').read())

fout.close()
