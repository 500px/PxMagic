from fhp.magic.cache import Cache

class Caches(object):
    def __init__(self):
        self.caches = []

    def __getitem__(self, args_kwargs_tuple):
        for cache in self.caches:
            if cache[args_kwargs_tuple]:
                return cache.value

    def __setitem__(self, args_kwargs_tuple, value):
        self.caches.append(Cache(args_kwargs_tuple, value))
