from fhp.helpers.json_finder import _parse_json, _dump_json
import os

def root_dir():
    return os.path.join(os.path.dirname(__file__), "..")

def get_consumer_key():
    """ For more info on the API visit developer.500px.com.
    If you are logged in to your 500px account you can 
    go to: http://500px.com/settings/applications to retrieve
    your key.
    """
    with open_or_ask(os.path.join(root_dir(),'config','authentication.json')) as f:
        auth = _parse_json(f.read())
        return auth["authentication"]["consumer_key"]

def get_consumer_secret():
    """ For more info on the API visit developer.500px.com.
    If you are logged in to your 500px account you can 
    go to: http://500px.com/settings/applications to retrieve
    your key.
    """
    with open_or_ask(os.path.join(root_dir(),'config','authentication.json')) as f:
        auth = _parse_json(f.read())
        return auth["authentication"]["consumer_secret"]

def get_verify_url():
    """ Used for non-server applications """
    with open_or_ask(os.path.join(root_dir(),'config','authentication.json')) as f:
        auth = _parse_json(f.read())
        if "verify_url" in auth["authentication"]:
            return auth["authentication"]["verify_url"]

class open_or_ask(object):
    warning = False
    def __init__(self, *args, **kwargs):
        args = list(args)
        filename = args[0]
        try:
            self.f = open(*args, **kwargs)
        except IOError:
            if not open_or_ask.warning:
                open_or_ask.warning = True
                print "Configuration file does not exist, you probably need to"
                print "use sudo to properly save this file. This should only"
                print "happen once."
            try:
                self.f.close()
            except:
                pass
            args[0] += '.example'
            f = open(*args, **kwargs)
            file_text = f.read()
            example = _parse_json(file_text)
            real = {}
            print "building authentication"
            for key in example:
                real[key] = {}
                for k in example[key]:
                    value = raw_input("What is your %s %s?\n" % (key, k))
                    real[key][k] = value
            with open(filename, 'w') as new_file:
                file_text = _dump_json(real)
                new_file.write(file_text)
            self.f = open(*args, **kwargs)
            
    def __enter__(self):
        return self.f
    
    def __exit__(self, type, value, traceback):
        self.f.close()
