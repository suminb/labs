
# Converts a .csv file to .js that can be used for Protovis library

import csv
import time

# git://github.com/geopy/geopy.git
from geopy import geocoders

def geocoding(postal_address):
    g = geocoders.Google()
    try:
        place, (lat, lng) = g.geocode(postal_address)
        return lat, lng
    
    except geocoders.google.GQueryError:
        # Recursively try to geocode with a subset of the given address
        if '\n' in postal_address:
            index = postal_address.find('\n')
            return geocoding(postal_address[index:])

    return 0.0, 0.0    


def parse_amount(m):
    if len(m) > 0 and m.startswith('$'):
        return float(m[1:].replace(',', ''))
    else:
        return 0.0

if __name__ == '__main__':
    with open('sales.csv') as csvfile:
        reader = csv.reader(csvfile)

        # skip header row
        reader.next()

        for row in reader:
            postal_address = row[14]
            price = parse_amount(row[6])
            shipping = parse_amount(row[7])

            if price != 0.0 and postal_address != None:
                lat, lng = geocoding(postal_address)

                print '{amount:%.2f, lat:%.7f, lng:%.7f},' % (price+shipping, lat, lng)

                # Google doesn't like too frequent queries
                time.sleep(1)
