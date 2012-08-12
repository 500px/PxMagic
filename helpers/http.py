import urllib

class safe_urlopen:
    def __init__(self, *args, **kwargs):
        self.file_resp = urllib.urlopen(*args, **kwargs)

    def __enter__(self):
        return self.file_resp 
    
    def __exit__(self, type, value, traceback):
        self.file_resp.close()

def smart_urlencode(kwargs):
    for key in kwargs:
        array = type(kwargs[key]) == type(()) or \
            type(kwargs[key]) == type([])
        if array:
            new_key = key + '[]'
            kwargs[new_key] = kwargs[key]
            del(kwargs[key])
    return urllib.urlencode(kwargs, True)
