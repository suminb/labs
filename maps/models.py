from django.db import models
import hashlib
import os, sys
        
class MapImage(models.Model):
    digest = models.CharField(max_length=120, primary_key=True)
    data = models.TextField()
    class Meta:
        db_table = u'maps_image'


class MapTile(models.Model):
    id = models.IntegerField(primary_key=True)
    date = models.DateTimeField()
    type = models.CharField(max_length=96)
    revision = models.IntegerField()
    x = models.IntegerField()
    y = models.IntegerField()
    z = models.IntegerField()
    digest = models.CharField(max_length=120)
    class Meta:
        db_table = u'maps_tile'


def digest_file(filename):
    file = open(filename, 'rb')
    hash = hashlib.sha1()
    #for chunk in file.chunks():
    #    hash.update(chunk)
    hash.update(file.read())
    file.close()
    return hash.hexdigest()

def parse_filename(filename):
    r = {}
    for kv in filename.split('&'):
        k, v = kv.split('=')
        r[k] = v

    if r.has_key('lyrs'):
        r['type'] = r['lyrs']
    elif r.has_key('v'):
        r['type'] = r['v']
    
    return r

def get_subdirectories(dir, digest, level=3):
    d = [os.path.dirname(dir)]
    for l in range(0, level):
        d.append(digest[l*2:(l*2+2)])
    d.append(digest)
    
    return '/'.join(d)

def create_subdirectories(dest, digest, level=3):
    path = get_subdirectories(dest, digest, level)
    
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path), 0755)
        
    # new path
    return path
    
    
def store_file(src, m, dest):
    dest = create_subdirectories(dest, m['digest'])
    
    source = open(src, 'rb')
    destination = open(dest, 'wb+')
    #for chunk in f.chunks():
    #    destination.write(chunk)
    destination.write(source.read())
    destination.close()
    source.close()
    
# content: file content, not a file name
# dest: destination file name
# m: metadata
# DEPRECATED: all map images will be stored in the database
def write_to_file(content, dest, m):
    path = create_subdirectories(dest, m['digest'])
    
    if not os.path.exists(dest):
        dest = open(path, 'wb')
        dest.write(content)
        dest.close()
    

plaintiles = [
    '826e2f7ff6223f4068cbaee0b5825f3a112eefa0', # m@114 ocean
    'a04d1a144428407c0b7d1fa8420d281da74da8b8', # h@114 transparent
    'b5f9bae93d7e05614d5d15709f835426a742624a', # m@114 light yellow
    'e4a7ff58dbbeed9f2e682619ad768ab90effbcbd', # w2p.114 ocean
    'fbf5e38e97f77cfcde11b6e3d23880c9e93c4374', # m@114 light green
    '31d8a9c70426bec769118ff1dd2994bfecb22f4f', # m@114 light grey
    '41a7f93ade113701a4be89f0fd2da2b3d77175a2', # m@114 light yellow (2)
    '6780b84073a03d563778a12fc2201398f6f3722e', # kr1.11 ocean
]

# src, dest: filename
# m: metadata
def process_file(src, m, dest):
    if os.path.getsize(src) <= 0:
        print 'Found a file size of zero (%s @(%s, %s, %s)). Skipping.' % (m['type'], m['x'], m['y'], m['z'])
        return -1
       
    
    # special cases
    #if m['digest'] in plaintiles:
        #print 'PlainTile'
        #plaintile = MapPlainTile(type=m['type'], x=m['x'], y=m['y'], z=m['z'], digest=m['digest'])
        #plaintile.save()

    tile = None
    try:
        tile = MapTile.objects.filter(x=m['x'], y=m['y'], z=m['z'], type=m['type']).order_by('-revision')
        if len(tile) > 0:
            tile = tile[0]
        else:
            raise MapTile.DoesNotExist
        
        if m['digest'] == tile.digest:
            print 'Conflict found (%d), but same tile. Ignoring...' % tile.id
            return tile.id
        else:
            #print 'Collision found. Stopping right here.'
            #sys.exit(0)
            print 'Different tile. Revision', tile.revision+1
            tile = MapTile(revision=tile.revision+1, date=m['date'], type=m['type'], size=m['size'], x=m['x'], y=m['y'], z=m['z'], digest=m['digest'])
            store_file(src, m, dest)

    except MapTile.DoesNotExist:
        tile = MapTile(revision=1, date=m['date'], type=m['type'], size=m['size'], x=m['x'], y=m['y'], z=m['z'], digest=m['digest'])
        store_file(src, m, dest)
    
    tile.save()
    return tile.id # this doesn't fucking work!!! WTF

