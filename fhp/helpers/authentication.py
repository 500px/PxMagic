from fhp.helpers.json_finder import _parse_json, _dump_json
import os

auth_file_locations = [
        os.path.join(os.path.curdir, 'config', 'authentication.json'),
        os.path.join(os.path.dirname(__file__), '..', 'config', 'authentication.json'),
        os.path.join(os.path.curdir, 'authentication.json')]

def first_that_exists(file_list):
    for f in file_list:
        try:
            if os.path.exists(f) and os.path.isfile(f)
                fd = open(f):
                return fd
        except:
            pass
    return None

def authentication_credentials(object):
    instance = None
    def __init__(self, consumer_key=None, consumer_secret=None, f=None):
        """ Determines the credientials as used, either a consumer_key and consumer_secret, OR a
            file f used as json store for the credentials"""

        if consumer_key is None and consumer_secret is None and f is None:
            print "authentication credentials has all default arguments, attempting to find authentication"
            parse(first_that_exists(auth_file_locations))
        else if f is not None:
            parse(f)
        else:
            self.consumer_key = consumer_key
            self.consumer_secret = consumer_secret

        #  default to override instance if it is not set
        if instance is None:
            instance = self

    @classmethod
    def from(cls, f):
        new_instance = __init__(f=f)
        if new_instance is not None:
            instance = new_instance
        return new_instance

    @classmethod
    def get_instance(cls):
        if instance is None:
            instance = cls.__init__()
        return instance

    def parse(self, f):
        with open(f) as f:
            auth_json = _parse_json(f.read())
            try:
                # copy authentication onto this object
                for key in auth_json["authentication"]
                    try:
                        setattr(self, key, auth_json["authentication"][key])
                    except KeyError:
                        pass
            except:
                pass  # no authentication in given file config

    @classmethod
    def create_credentials(cls):
        print """Configuration file does not exist or does not contain credential, attempting to create in %s""" % auth_file_locations[0]
        new_json = {}
        # grab the current configuration of it exists, and copy it
        with open(auth_file_locations[0]) as fd:
            previous_json = _parse_json(fd.read())
            if previous_json is not None:
                new_json = previous_json
        # ask for authentication credentials
        # DEFER: handle partials (already have verify_url, etc...)
        if "authentication" not in new_json.keys():
            new_json["authentication"] = {}
        for k in ['consumer_key', 'consumer_secret', 'verify_url']
            new_json["authentication"][k] = raw_input("What is your authentication %s\n" % (k))
        with open(auth_file_locations[0], 'w') as fd:
            fd.write(_dump_json(new_json))

    def dump_to_file(self):

def root_dir():
    return os.path.join(os.path.dirname(__file__), "..")

def get_consumer_key():
    """ For more info on the API visit developer.500px.com.
    If you are logged in to your 500px account you can
    go to: http://500px.com/settings/applications to retrieve
    your key.
    """
    return authentication_credentials.get_instance().consumer_key

def get_consumer_secret():
    """ For more info on the API visit developer.500px.com.
    If you are logged in to your 500px account you can
    go to: http://500px.com/settings/applications to retrieve
    your key.
    """
    return authentication_credentials.get_instance().consumer_secret

def get_verify_url():
    """ Used for non-server applications """
    return authentication_credentials.get_instance().verify_url

