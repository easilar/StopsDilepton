import pickle, os
class Cache:
    def __init__(self, filename=None, verbosity=0, overwrite=False):
        self.verbosity=verbosity
        self.cacheFileLoaded = False
        self.initCache(filename)

    def initCache(self, filename):
        self.filename=filename
        try:
            self._cache = pickle.load(open(filename, 'r'))
            if self.verbosity>=1: print "Loaded cache file %s"%filename
            self.cacheFileLoaded = True
        except:# (IOError, ValueError, EOFError):
            if self.verbosity>=2: print "File %s not found or corrupted. Starting new cache."%filename
            self._cache = {}

    def contains (self, key):
        return key in self._cache

    def get(self, key):
        return self._cache[key]

    def add(self, key, val, save):
        self._cache[key] = val
        if save==True:
            if self.verbosity>=2: print "Storing new result %r to key %r"%(val, key)
            self.save()
        return self._cache[key]

    def save(self):
        pickle.dump(self._cache, open(self.filename, 'w'))
        if self.verbosity>=2: print "Written cache file %s"%self.filename
