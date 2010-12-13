from urllib import urlencode
from urllib2 import *
from urlparse import urlparse, parse_qs
from re import findall, search, match
from base64 import *
from hashlib import *
from time import time, sleep
from math import log, sqrt, asin, pi
from multiprocessing import Pool
from random import choice, randint, uniform, gauss

import django.utils.simplejson as json

useragent = 'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.8) Gecko/20100214 Ubuntu/9.10 (karmic) Firefox/3.5.8'
cities = (
    # lat, long, significance, description
    (32.12, -110.93, 'Tucson, AZ'),
    (33.43, -112.02, 'Phoenix, AZ'),
    #(37.5, 127.0, 'Seoul, South Korea'),
    #(39.031859, 125.753765, 'Pyongyang, North Korea'),

    (40.77, -73.98, 'New York, NY'),    
    (34.05, -118.25, 'Los Angeles, CA'),
    (41.836944, -87.684444, 'Chicago, IL'),
    (29.97, -95.35, 'Houston, TX'),
    (39.953333, -75.17, 'Philadelphia, PA'),
    (29.416667, -98.5, 'San Antonio, TX'),
    (32.82, -116.97, 'San Diego, CA'),
    (37.62, -122.38, 'San Francisco, CA'),
    (37.335278, -121.891944, 'San Hose, CA'),
    (36.08, -115.17, 'Las Vegas, NV'),
    
    (35.667, 139.75, 'Tokyo, Japan'),
    (34.7, 135.5, 'Osaka, Japan'),
    (55.750, 37.700, 'Moscow, Russia'),
    (30.050, 31.250, 'Cairo, Egypt'),
    (-35.285985, 149.124298, 'Canberra, Australia'),
    (45.420833, -75.69, 'Ottawa, Canada'),
    (41.9, 12.5, 'Rome, Italy'),
    (48.856667, 2.350833, 'Paris, France'),
    (52.500556, 13.398889, 'Berlin, Germany'),
    (51.508056, -0.124722, 'London, UK'),
    (37.966667, 23.716667, 'Athens, Greece'),
    (33.325, 44.422, 'Baghdad, Iraq'),
    (25.033333, 121.633333, 'Taipei, Taiwan'),
    (39.913889, 116.391667, 'Beijing, China'),
    (46.95, 7.45, 'Bern, Switzerland'),
    
    (31.302022, -110.937023, 'Nogales, Mexico'),
)

def parse_metadata(url):
    path = url[url.rfind('/')+1:]
    r = {}
    for kv in path.split('&'):
        k, v = kv.split('=')
        r[k] = v

    if r.has_key('lyrs'):
        r['type'] = r['lyrs']
    elif r.has_key('v'):
        r['type'] = r['v']
        
    if match('^[a-z]@[0-9]+$', r['type']):
        tr = r['type'].split('@')
        r['type'] = tr[0]
        r['revision'] = tr[1]
    elif match('^[0-9]+$', r['type']):
        r['revision'] = r['type']
        r['type'] = 's'
    
    return r
    
def get_rendered_html(url):
    print 'Requesting rendered HTML'
    req = Request('http://labs.sumin.us/incubator/webarchive?store=0&url=' + quote(url))
    f = urlopen(req)
    return f.read()
    
def download(url, quiet=False):
    headers = {
        'User-Agent': useragent,
        'Accept': 'image/png,image/*;q=0.8,*/*;q=0.5',
        'Accept-Language': 'en-us,en;q=0.5',
        'Referer': 'http://maps.google.com/',
    }
    req = Request(url, None, headers)

    f = urlopen(req)
    content = f.read()
    f.close()
    
    return content

def get_tile_urls(raw):
    # maps, satellite overlays
    urls = findall('http://mt[0-3].google.com/vt/lyrs=[^"]+', raw)
    urls = filter(lambda x: search('x=\d+', x), urls)
    urls = map(lambda x: x.replace('&amp;', '&'), urls)

    # satellite images
    urls2 = findall('http://khm[0-3].google.com/kh/[^"]+', raw)
    urls2 = filter(lambda x: search('x=\d+', x), urls2)
    urls2 = map(lambda x: x.replace('&amp;', '&'), urls2)

    return set(urls + urls2)
    
# This function is supposed to return the number of tiles at a particular point,
# but temporarily returns 1 if there is any, 0 otherwise.
def get_tile_count_at_point(x, y, z, type=None):
    content = download('http://labs.sumin.us/maps/image/%d-%d-%d/%s' % (x, y, z, type))
    
    return 0 if match('^{"status":', content) else 1
    
def upload(content, url, metadata):
    m = metadata

    if content.find('<html>') != -1:
        print 'Not supported message (%s @(%s, %s, %s)). Skipping.' % (m['type'], m['x'], m['y'], m['z'])
        return False
    
    m['date'] = int(time())
    m['size'] = len(content)
    m['digest'] = sha1(content).hexdigest()
    
    if m['digest'] == 'a04d1a144428407c0b7d1fa8420d281da74da8b8':
        print 'Transparent hover image. Skipping...'
        return False
    
    content = b64encode(content)

    params = {'file':content, 'metadata':json.dumps(m), 'checksum':None}
    checksum = sha1('%s-%s-%s-%s-%s-%s' % (m['x'], m['y'], m['z'], m['type'], m['size'], m['digest'])).hexdigest()
    params['checksum'] = checksum
    params = urlencode(params)
    
    try:
        u = urlopen(url, params)
    except HTTPError as e:
        print "error: code=%s message=%s" % (e.code, e.msg)
        return False
    except Exception as e:
        print e
        return False
        
    r = json.loads(u.read())
    if r['results']:
        print r['results']
    
    u.close()    
    return True
    
def process_url(url):
    metadata = parse_metadata(url)
    qs = parse_qs(urlparse(url).path)
    coordinate = '%s-%s-%s/%s/%s' % (qs['x'][0], qs['y'][0], qs['z'][0], metadata['type'], metadata['revision'])
    
    try:
        print 'Downloading %s' % coordinate
        image = download(url)
    except Exception as e:
        print 'Download failed'
        print e
        return False
    metadata = parse_metadata(url)
    
    try:
        print 'Uploading %s' % coordinate
        upload(image, 'http://labs.sumin.us/maps/upload', metadata)
        #upload(image, 'http://localhost:8080/maps/upload', metadata)
    except Exception as e:
        print 'Upload failed'
        print e
        return False
        
    return True
    
def process_urls(urls, processes=4):
    pool = Pool(processes)
    pool.map(process_url, urls)
    pool.close()
        
def scan(cityname, lat, lng, z, t):
    print 'Scanning %s (%f, %f) @z=%d, t=%s' % (cityname, lat, lng, z, t)
    
    try:
        raw = get_rendered_html('http://maps.google.com/?ie=UTF8&ll=%f,%f&spn=1.931682,5.622253&z=%d&t=%s&output=embed' % (lat, lng, z, t))
        urls = get_tile_urls(raw)
    except:
        print 'Scanning failed'
        sleep(1)
        
    # If we've got nothing, increase the zoom level and scan until z = 5
    if len(urls) == 0:
        if z > 4:
            scan(cityname, lat, lng, z-1, t)
        else:
            print 'No URL found. Skipping...'
    else:
        print 'Found %d URLs' % len(urls)
        process_urls(urls)
        
def normalize_coordinate(x, y, z):
    return x%(2**z), y%(2**z), z
        
# picks a random city based on its significance
def pick_city():
    #n = abs(int(gauss(0.0, sqrt(len(cities)))))
    #return cities[n]
    return choice(cities)

# TODO: needs to be revised (unknown boundary of y)
def pick_random_point(z):
    return randint(0, 2**z), int(gauss(1.0, sqrt(0.085))*(2**(z-1)))

def pick_random_latlong():
    return gauss(1.0, sqrt(0.085)), uniform(-1.0, 1.0)*180
    
# TODO: might be inaccurate in some cases
def convert_point_to_latlong(x, y, z):
    w = 2**(z-1)
    lat, long = asin((y-w)/(w*-1.0))/pi*170, (x-w)/(w*1.0)*180
    return lat, long

if __name__ == '__main__':
    # lats = [5.32, 10.63, 15.94, 21.26, 58.47, 63.79, 69.10, 74.42]
    # #ys = [16868, 17357, 17854, 18365, 22980, 23985, 25201, 26757]
    # ys = [484, 973, 1470, 1981, 6596, 7601, 8817, 10373]
    # zs = map(lambda y, lat: y/sin(lat/180*pi), ys, lats)
    # xs = map(lambda z, lat: z*cos(lat/180*pi), zs, lats)
    # print xs
    
    # while True:
    #     #t = choice(('h', 'm'))
    #     t = 'm'
    #     z = int(gauss(10, sqrt(8)))%18 + 1
    #     lat, long = pick_random_latlong()
    # 
    #     scan('random location', lat, long, z, t)
    # 
    # while True:
    #     city = pick_city()
    #     t = 'h' if city[2] == 'Pyongyang, North Korea' else choice(('h', 'h', 'm'))
    # 
    #     if t == 'h':
    #         z = int(log(randint(pow(4, 2), pow(4, 19)), 4))
    #     else:
    #         z = int(log(randint(pow(4, 8), pow(4, 17)), 4))
    #     #z = randint(2, 19)    
    # 
    #     r = 8.0
    #     lat, lng = city[0]+uniform(-r/z, r/z), city[1]+uniform(-r/z, r/z)
    # 
    #     scan(city[2], lat, lng, z, t)

    x, y, z = map(int, (sys.argv[1], sys.argv[2], sys.argv[3]))
    t = sys.argv[4] # type

    width = 10
    height = 6

    while True:
        #z = int(log(randint(pow(4, 2), pow(4, 19)), 4))
        #x, y = pick_random_point(z)
        
        print 'Scanning %d-%d-%d/%s' % (x, y, z, t)
        
        urls = []
        for i in xrange(y-height/2, y+height/2):
            for j in xrange(x-width/2, x+width/2):
                j, i, z = normalize_coordinate(j, i, z)
                s = 'Galileo'[:randint(1, 6)]
                
                if t in 'hmt':
                    r = 129
                    url = 'http://mt%d.google.com/vt/lyrs=%s@%d&hl=en&src=api&x=%s&y=%s&z=%s&s=%s' % (randint(0, 3), t, r, j, i, z, s)
                elif t == 's':
                    r = 63
                    url = 'http://khm%d.google.com/kh/v=%d&hl=en&src=api&x=%s&y=%s&z=%s&s=%s' % (randint(0, 3), r, j, i, z, s)
                urls.append(url)
        process_urls(urls)
        
        direction = randint(0, 3)
        magnitude = randint(1, 5)
        if direction == 0:
            x += width
            print 'Move to right * %d' % magnitude
        elif direction == 1:
            y += height
            print 'Move down * %d' % magnitude
        elif direction == 2:
            x -= width
            print 'Move to left * %d' % magnitude
        else:
            y -= height
            print 'Move up * %d' % magnitude
        
        print 'Sleeping for a while...'
        if t == 's':
            sleep(randint(2, 32))
        else:
            sleep(randint(2, 16))
