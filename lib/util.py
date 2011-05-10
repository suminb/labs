import hashlib
    
def sha1(s):
    hash = hashlib.sha1()
    hash.update(s)
    return hash.hexdigest()

class Base62:
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    base = 62
    
    @staticmethod
    def encode(value):
        """Converts given value to base62 digits. Only works for positive integers."""
        stack = []
        while value > 0:
            remainder = value % Base62.base
            value = value / Base62.base
            
            stack.append(str(Base62.digits[remainder]))
            
        stack.reverse()
        return "".join(stack)
        
    @staticmethod
    def decode(value):
        """Converts base62 digits into base10 digits."""
        
        v = 0
        p = len(value) - 1
        for d in value:
            # digits.index(d) is an O(n) operation. Very inefficient.
            v += Base62.digits.index(d) * (Base62.base ** p)
            p -= 1
        
        return v
        
        
        
        