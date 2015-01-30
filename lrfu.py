from itertools import count
from heapq import heapify, nsmallest

try:
    from collections import MutableMapping
except ImportError:
    from UserDict import DictMixin
    MutableMapping = None
    
class LRFUCache(MutableMapping or DictMixin):
    def __init__(self, control=1e-3, limit=16):
        self.data = {}
        self.limit = limit
        assert limit > 0
        self.base = 0.5 ** control
        self.time = count().next
        
    def __getitem__(self, key):
        entry = crf, atime, key, value = self.data[key]
        entry[1] = now = self.time()
        entry[0] = 1.0 + self.base ** (now - atime) * crf
        return value
    
    def __setitem__(self, key, value):
        data = self.data
        if key in data:
            data[key][3] = value
        else:
            if len(data) == self.limit:
                self.compact()
            data[key] = [1.0, self.time(), key, value]
        
    def __delitem__(self, key):
        del self.data[key]
        
    def compact(self):
        data = self.data
        base = self.base
        while True:
            now = self.time()
            entries = [(base ** (now - atime) * crf, key) for 
                crf, atime, key, value in data.itervalues()]
            heapify(entries)
            delete_count = len(entries) - (self.limit >> 1)
            if delete_count <= 0:
                break              
            try:
                for crf, key in nsmallest(delete_count, entries):
                    del data[key]
            except KeyError:
                continue
            break
    
    def __len__(self):
        return len(self.data)
    
    def __iter__(self):
        return iter(self.data)
    
    def keys(self):
        return self.data.keys()
    
    def __contains__(self, key):
        return key in self.data

    def iterkeys(self):
        return iter(self.data)
    
    def itervalues(self):
        return self.data.itervalues()
    
    def iteritems(self):
        for crf, atime, key, value in self.data.itervalues():
            yield (key, value)
    
    def __repr__(self):
        return repr(self.data)
