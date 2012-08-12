"""
Created by @arthurnn on 2012-01-19.
"""

import urllib
from helpers.json_finder import _parse_json
from helpers.http import safe_urlopen

class FiveHundredPx:
    BASE_URL = 'https://api.500px.com/v1'
    
    def __init__(self, consumer_key):
        """For more info on the API visit developer.500px.com.
        If you are logged in to your 500px account you can 
        go to: http://500px.com/settings/applications to retrieve
        your key.
        """
        self.consumer_key = consumer_key

    def request(self, path, post_args=None, **kwargs):
        """Handles the actual request to 500px. Posting has yet 
        to be implemented.
        """
        if post_args:
            raise NotImplementedError
        self._set_consumer_key_to_args_(post_args, kwargs)
        post_data = None if post_args is None else urllib.urlencode(post_args)
        encoded_kwargs = urllib.urlencode(kwargs, True)
        full_url = FiveHundredPx.BASE_URL + path + "?" + encoded_kwargs
        with safe_urlopen(full_url, post_data) as file_resp:
            response = _parse_json(file_resp.read())
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
        a limit of 20 results.
        """
        kwargs = kwargs or dict(feature='editors',
                                limit='100')
        
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
            
    def get_photo(self, id, args = None):
        data = self.request('/photos/%d' % id, args)
        return data

    def _set_consumer_key_to_args_(self, post_args, kwargs):
        if post_args is not None:
            post_args["consumer_key"] = self.consumer_key
        else:
            kwargs["consumer_key"] = self.consumer_key
