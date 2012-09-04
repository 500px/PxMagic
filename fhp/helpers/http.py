import urllib
from fhp.helpers.json_finder import _parse_json
from oauth_hook import OAuthHook
import requests

class safe_urlopen(object):
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

def build_oauth_client(url,
                       authorize_url,
                       access_token_url,
                       consumer_key,
                       consumer_secret,
                       auth_url_fn,
                       *args,
                       **kwargs):
    import urlparse
    
    pre_oauth_hook = OAuthHook(consumer_key=consumer_key,
                           consumer_secret=consumer_secret)
    response = requests.post(url, hooks={'pre_request': pre_oauth_hook})
    
    qs = urlparse.parse_qs(response.text)
    oauth_token = qs['oauth_token'][0]
    oauth_secret = qs['oauth_token_secret'][0]

    auth_url = authorize_url + "?oauth_token=" + oauth_token

    auth_url_fn(auth_url)
    verify_url = "https://evening-scrubland-4062.herokuapp.com/oauth"
    verify_url += "?oauth_token=%s" % oauth_token
    with safe_urlopen(verify_url) as file_resp:
        raw_response = file_resp.read()
        response = _parse_json(raw_response)
    oauth_verifier = response
    
    new_oauth_hook = OAuthHook(oauth_token,
                               oauth_secret,
                               consumer_key,
                               consumer_secret)

    response = requests.post(access_token_url,
                             {'oauth_verifier': oauth_verifier},
                             hooks={'pre_request': new_oauth_hook})
    response = urlparse.parse_qs(response.content)
    access_token = response['oauth_token'][0]
    access_token_secret = response['oauth_token_secret'][0]
    oauth_hook = OAuthHook(access_token,
                           access_token_secret,
                           consumer_key,
                           consumer_secret,
                           header_auth=True)
    
    client = requests.session(hooks={'pre_request': oauth_hook})
    return client
