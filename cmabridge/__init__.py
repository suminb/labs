from random import shuffle

def is_hangul(unichr):
    return ord(unichr) >= 0x0800 and ord(unichr) <= 0xFFFF
    
def is_acceptable(unichr):
    return unichr.isalpha() or is_hangul(unichr)

def swap(word):
    if len(word) > 3:
        first, last = word[0], word[-1]
        
        prefix = ''
        if not is_acceptable(first):
            prefix = first
            word = word[1:]
            
        suffix = ''
        if not is_acceptable(last):
            suffix = last
            word = word[:-1]
            
        middle = list(word[1:-1])
        middle.reverse() if len(word) == 4 else shuffle(middle)

        word = prefix + word[0] + ''.join(middle) + word[-1] + suffix
        
    return word

def partition(alist, indices):
    """Copied this function from http://stackoverflow.com/questions/1198512/split-a-list-into-parts-based-on-a-set-of-indexes-in-python
    """
    return [alist[i:j] for i, j in zip([0]+indices, indices+[None])]

def translate(text):
    text_index_pairs = zip(text, xrange(len(text)))

    # Finds text-index pairs where the character is neither English or Korean.
    filtered_pairs = filter(lambda p: not (p[0].isalpha() or is_hangul(p[0])), text_index_pairs)
    indices = map(lambda p: p[1], filtered_pairs)
    
    words = partition(text, indices)

    return ''.join(map(swap, words))