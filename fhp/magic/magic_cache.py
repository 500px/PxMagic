from functools import wraps
import warnings

from fhp.magic.caches import Caches

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
            try:
                result = method(self, *args, **kwargs)
            except Exception, e:
                # Honestly, I consider this a bug in Python
                warning = """Exception in a magically cached method
                Depending on your implementation
                if you use __getattr__, for example
                the Exception may silently fail, this was the exception:
                """
                warning += str(e)
                warnings.warn(warning)
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
            force_fn_call = False
            if 'force_fn_call' in kwargs:
                force_fn_call = kwargs['force_fn_call']
                del(kwargs['force_fn_call'])
            if function not in self.caches:
                self.caches[function] = Caches()
            if force_fn_call:
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
