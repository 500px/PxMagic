from functools import wraps
import warnings

from magic.caches import Caches

def magic_cache(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        cache_name = '_' + method.__name__ + "_cache_"
        result = None
        if hasattr(self, cache_name):
            result = getattr(self, cache_name)[(args, kwargs)]
        else:
            setattr(self, cache_name, Caches())
        if not result:
            result = method(self, *args, **kwargs)
            caches = getattr(self, cache_name)
            caches[(args, kwargs)] = result
        return result
    return wrapper

class MagicFunctionCache(object):
    def __init__(self):
        self.caches = {}

    def __call__(self, function):
        @wraps(function)
        def function_wrapper(*args, **kwargs):
            from pprint import pprint
            result = None
            if function not in self.caches:
                self.caches[function] = Caches()
            if 'force_fn_call' in kwargs:
                del(kwargs['force_fn_call'])
                result = self.get_and_set_cache(function, *args, **kwargs)
            else:
                result = self.caches[function][(args, kwargs)]
                if not result:
                    result = self.get_and_set_cache(function, *args, **kwargs)
            return result
        return function_wrapper

    def get_and_set_cache(self, function, *args, **kwargs):
        result = function(*args, **kwargs)
        self.caches[function][(args, kwargs)] = result
        return result

magic_fn_cache = MagicFunctionCache()
