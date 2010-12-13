import hashlib
    
def sha1(s):
    hash = hashlib.sha1()
    hash.update(s)
    return hash.hexdigest()
