import urllib

class safe_urlopen:
    def __init__(self, *args, **kwargs):
        self.file_resp = urllib.urlopen(*args, **kwargs)

    def __enter__(self):
        return self.file_resp 
    
    def __exit__(self, type, value, traceback):
        self.file_resp.close()
