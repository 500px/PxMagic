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
    def __init__(self, ignore_caching_on=None):
        self.caches = {}
        self.ignore_caching_on = ignore_caching_on or []

    def __call__(self, function):
        @wraps(function)
        def function_wrapper(*args, **kwargs):
            result = None
            force_fn_call = False
            if 'force_fn_call' in kwargs:
                force_fn_call = kwargs['force_fn_call']
                del(kwargs['force_fn_call'])
            elif 'forced_return_value' in kwargs:
                """ This part is a little strange. Essentially, there are times
                when you want a function to return a certain object with a certain
                pattern of arguments that are *different* than the ones that called
                it originally. For example, since you can get a user by both id 
                and username, the cache would normally hand back two distinct objects
                but by using recursion and forcing a return value one is able to 
                make the cache return the same cache by either or all patterns
                """
                forced_return_value = kwargs['forced_return_value']
                del(kwargs['forced_return_value'])
                self.force_return_value(function,
                                        forced_return_value,
                                        *args, **kwargs)
            if function not in self.caches:
                self.caches[function] = Caches()
            if force_fn_call:
                result = self.get_and_set_cache(function,
                                                *args,
                                                **kwargs)
            else:
                result = self.get_from_cache(function, *args, **kwargs)
                if not result:
                    result = self.get_and_set_cache(function,
                                                    *args, **kwargs)
            return result
        return function_wrapper

    def get_from_cache(self, function, *args, **true_kwargs):
        from copy import copy
        kwargs = copy(true_kwargs)
        for kwarg in self.ignore_caching_on:
            if kwarg in kwargs:
                del(kwargs[kwarg])
        return self.caches[function][(args, kwargs)]

    def get_and_set_cache(self, function, *args, **kwargs):
        result = function(*args, **kwargs)
        for kwarg in self.ignore_caching_on:
            if kwarg in kwargs:
                del(kwargs[kwarg])
        self.caches[function][(args, kwargs)] = result
        return result

    def force_return_value(self, function, forced_return_value, *args, **kwargs):
        self.caches[function][(args, kwargs)] = forced_return_value

magic_fn_cache = MagicFunctionCache()
