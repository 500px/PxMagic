class Cache(object):
    def __init__(self, args_kwargs_tuple, value):
        self.args_cache = args_kwargs_tuple[0]
        self.kwargs_cache  = args_kwargs_tuple[1]
        self.value = value

    def __getitem__(self, args_kwargs_tuple):
        args = args_kwargs_tuple[0]
        kwargs = args_kwargs_tuple[1]
        return self.args_cache == args and self.kwargs_cache == kwargs 
