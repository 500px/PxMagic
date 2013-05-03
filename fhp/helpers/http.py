import urllib
from fhp.helpers.json_finder import _parse_json
from oauth_hook import OAuthHook
import requests
import urlparse

class safe_urlopen(object):
    def __init__(self, *args, **kwargs):
        self.file_resp = urllib.urlopen(*args, **kwargs)

    def __enter__(self):
        return self.file_resp 
    
    def __exit__(self, type, value, traceback):
        self.file_resp.close()

def multipart_post(url, files):
    return requests.post(url, files=files)

def smart_urlencode(kwargs):
    for key in kwargs:
        array = type(kwargs[key]) in (list, tuple)
        if array:
            new_key = key + '[]'
            kwargs[new_key] = kwargs[key]
            del(kwargs[key])
    return urllib.urlencode(kwargs, True)

def http_request(base_url, path, post_args, log_request=False, **kwargs):
    post_data = None if post_args is None else urllib.urlencode(post_args)
    encoded_kwargs = smart_urlencode(kwargs)
    full_url = base_url + path + "?" + encoded_kwargs
    if log_request:
        from time import time
        print time()
        print full_url
    with safe_urlopen(full_url, post_data) as file_resp:
        file_contents = file_resp.read()
        if log_request:
            from time import time
            print time()
            print file_contents[:40]
        response = None
        try:
            response = _parse_json(file_contents)
        except:
            print file_contents
            print full_url
    return response

def build_oauth_client_for_client(request_url,
                                  authorize_url,
                                  access_token_url,
                                  consumer_key,
                                  consumer_secret,
                                  auth_url_fn,
                                  verify_url=None,
                                  *args,
                                  **kwargs):
    
    result = use_auth_url_fn(request_url,
                             authorize_url,
                             access_token_url,
                             consumer_key,
                             consumer_secret,
                             auth_url_fn)
    if not verify_url:
        raise NotImplementedError, "Only possible with a verify url. Maybe you can use http://verify-oauth.herokuapp.com/ ?"
    oauth_token, oauth_secret = result
    oauth_verifier = retrieve_oauth_verifier(oauth_token=oauth_token,
                                            verify_url=verify_url)
    client = finalize_oauth_client(oauth_token,
                                   oauth_secret,
                                   oauth_verifier,
                                   consumer_key,
                                   consumer_secret,
                                   access_token_url)
    return client

def use_auth_url_fn(request_url,
                    authorize_url,
                    access_token_url,
                    consumer_key,
                    consumer_secret,
                    auth_url_fn):
    pre_oauth_hook = OAuthHook(consumer_key=consumer_key,
                               consumer_secret=consumer_secret)
    response = requests.post(request_url, hooks={'pre_request': pre_oauth_hook})

    qs = urlparse.parse_qs(response.text)
    
    oauth_token = qs['oauth_token'][0]
    oauth_secret = qs['oauth_token_secret'][0]

    auth_url = authorize_url + "?oauth_token=" + oauth_token
    auth_url_fn(auth_url)
    return oauth_token, oauth_secret

def retrieve_oauth_verifier(oauth_token, verify_url):
    if verify_url[-1] != "/":
        verify_url += "/"
    verify_url += str(oauth_token)
    with safe_urlopen(verify_url) as file_resp:
        oauth_verifier = file_resp.read()
    return oauth_verifier

def finalize_oauth_client(oauth_token,
                          oauth_secret,
                          oauth_verifier,
                          consumer_key,
                          consumer_secret,
                          access_token_url):
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
    client.access_token = access_token
    return client


def paginate(skip, rpp, request_function, title, total_pages='total_pages'):
    page = 1
    if skip:
        page = skip / rpp
        skip -= page * rpp
        page += 1
        assert(skip >= 0) 
    while True:
        data = request_function(page=page, rpp=rpp)
        for thing in data[title]:
            if skip:
                skip -= 1
                continue
            yield thing
        if page == data[total_pages]:
            break
        page += 1
