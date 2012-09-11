from fhp.magic.caches import Caches

class magic_object(object):
    def empty_cache(self, *args, **kwargs):
        return self.clear_cache(*args, **kwargs)
    
    def clear_cache(self, method):
        if callable(method):
            cache_name = '_' + method.__name__ + "_cache_"
        elif type(cache_name) == str and cache_name[:7] == "_cache_":
            cache_name = method
        elif type(cache_name) == str:
            cache_name = '_' + method + "_cache_"
        elif type(cache_name) == Caches:
            cache = cache_name
        else:
            warnings.warn("Unknown cache type for magic object")
            cache = method
        cache = cache or getattr(self, cache_name)
        del(cache)
        return True
    
    def find_thing(self, things_name, **kwargs):
        things = getattr(self, things_name)
        for thing in things:
            is_match = True
            for kwarg in kwargs:
                if not getattr(thing, kwarg) == kwargs[kwarg]:
                    is_match = False
            if is_match:
                return thing
