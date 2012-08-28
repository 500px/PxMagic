"""
Created by @arthurnn on 2012-01-19.
"""

import urllib
from helpers.json_finder import _parse_json
from helpers.http import safe_urlopen, smart_urlencode, build_oauth_client
from pprint import pprint
class FiveHundredPx(object):
    BASE_URL = 'https://api.500px.com/v1'
    
    def __init__(self, consumer_key, consumer_secret):
        """For more info on the API visit developer.500px.com.
        If you are logged in to your 500px account you can 
        go to: http://500px.com/settings/applications to retrieve
        your key.
        """
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret

    def request(self, path, post_args=None, **kwargs):
        """Handles the actual request to 500px. Posting has yet 
        to be implemented.
        """
        if post_args:
            raise NotImplementedError
        self._set_consumer_key_to_args_(post_args, kwargs)
        post_data = None if post_args is None else urllib.urlencode(post_args)
        encoded_kwargs = smart_urlencode(kwargs)
        full_url = FiveHundredPx.BASE_URL + path + "?" + encoded_kwargs
        with safe_urlopen(full_url, post_data) as file_resp:
            file_contents = file_resp.read()
            response = None
            try:
                response = _parse_json(file_contents)
            except:
                print file_contents
                print full_url
        return response

    def search_photos(self, **kwargs):
        data = self.request('/photos/search', **kwargs)
        return data

    def get_photos(self, **kwargs):
        """ kwargs are the none-post arguments (ie, url arguments)
        that you would like to attach to the get_photos request.
        
        If there are no arguments, the the default is set to
        getting the first 100 photos from the editiors list.
        
        If there are no limits, it defaults to the API default of
        a limit of 20 results, which is also the official limit in 
        the terms of use for number of photos to be displayed at 
        once, although you can email 500px to get permission to 
        display more.
        """
        kwargs = kwargs or dict(feature='editors')
        
        limit = 20 if 'limit' not in kwargs else kwargs['limit']
        data = self.request('/photos', **kwargs)
        total_pages = data['total_pages']
        count = 0
        
        page = data['current_page']
        
        while page <= total_pages:
            for p in data['photos']:
                count = count+1
                if count > limit: return
                yield p
            
            kwargs['page'] = page = page+1
            data = self.request('/photos', **kwargs)
            
    def get_photo(self, id, **kwargs):
        data = self.request('/photos/%d' % id, **kwargs)
        return data

    def get_user(self, user_id, authorized_client=None, **kwargs):
        if 'username' in kwargs:
            raise NotImplementedError
        if 'email' in kwargs:
            raise NotImplementedError
        if authorized_client:
            url = FiveHundredPx.BASE_URL + '/users'
            data = self.use_authorized_client(authorized_client, url, **kwargs)
        else:
            data = self.request('/users/%d' % user_id, **kwargs)
        return data

    def get_user_friends(self, user_id):
        page = 1
        while True:
            data = self.request('/users/%s/friends' % user_id, page=page)
            assert(page == data['page'])
            for friend in data['friends']:
                yield friend
            if page == data['friends_pages']:
                break
            page += 1

    def get_user_followers(self, user_id):
        page = 1
        while True:
            data = self.request('/users/%s/followers' % user_id, page=page)
            assert(page == data['page'])
            for follower in data['followers']:
                yield follower
            if page == data['followers_pages']:
                break
            page += 1

    def use_authorized_client(self,
                              authorized_client,
                              url,
                              post_args=None,
                              **kwargs):
        if not post_args:
            data = _parse_json(authorized_client.get(url, **kwargs).content)
        else:
            raise NotImplementedError
        return data

    def sample_auth_url_fn(self, authorization_url):
        from subprocess import call
        call(["google-chrome",authorization_url])
        accepted = 'n'
        while accepted.lower() == 'n':
            accepted = raw_input('Have you authorized me? (y/n) ')

    def get_authorized_client(self, 
                              auth_url_fn=None,
                              **kwargs):
        if not auth_url_fn:
            auth_url_fn = self.sample_auth_url_fn
            
        request_url = FiveHundredPx.BASE_URL + "/oauth/request_token"
        authorize_url = FiveHundredPx.BASE_URL + "/oauth/authorize"
        access_token_url = FiveHundredPx.BASE_URL + "/oauth/access_token"
        
        return build_oauth_client(request_url,
                                  authorize_url,
                                  access_token_url,
                                  self.consumer_key,
                                  self.consumer_secret,
                                  auth_url_fn)    
        
    def _set_consumer_key_to_args_(self, post_args, kwargs):
        if post_args is not None:
            post_args["consumer_key"] = self.consumer_key
        else:
            kwargs["consumer_key"] = self.consumer_key
