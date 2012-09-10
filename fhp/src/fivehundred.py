"""
Created by @arthurnn on 2012-01-19.
"""

import urllib
from fhp.helpers.json_finder import _parse_json
from fhp.helpers.http import safe_urlopen, smart_urlencode, build_oauth_client
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
        log_request = False
            
        if post_args:
            raise NotImplementedError
        self._set_consumer_key_to_args_(post_args, kwargs)
        post_data = None if post_args is None else urllib.urlencode(post_args)
        encoded_kwargs = smart_urlencode(kwargs)
        full_url = FiveHundredPx.BASE_URL + path + "?" + encoded_kwargs
        if log_request:
            print full_url
            from time import time
            print time()
        with safe_urlopen(full_url, post_data) as file_resp:
            file_contents = file_resp.read()
            if log_request:
                print time()
            response = None
            try:
                response = _parse_json(file_contents)
            except:
                print file_contents
                print full_url
        
        return response

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

    def get_blog_post(self, id):
        blog_post = self.request('/blogs/%d' % id)
        return dict(blog_post=blog_post)

    def get_user_by_id(self, user_id, authorized_client=None, **kwargs):
        if 'username' in kwargs:
            raise TypeError, "get_user_by_id cannot handle a username param"
        if 'email' in kwargs:
            raise TypeError, "get_user_by_id cannot handle a email param"
        if authorized_client:
            # This may be done incorrectly. Authorized clients both let you 
            # do requests as well as pull down user information for the 
            # authorized user. Right now this basically throws out the user_id.
            url = FiveHundredPx.BASE_URL + '/users'
            data = self.use_authorized_client(authorized_client, url, **kwargs)
        else:
            data = self.request('/users/%d' % user_id, **kwargs)
        return data

    def get_user_by_username(self, username, authorized_client=None, **kwargs):
        if 'id' in kwargs:
            raise TypeError, "get_user_by_username cannot handle a user_id param"
        if 'email' in kwargs:
            raise TypeError, "get_user_by_id cannot handle a email param"
        if authorized_client:
            # This may be done incorrectly. Authorized clients both let you 
            # do requests as well as pull down user information for the 
            # authorized user. Right now this basically throws out the username.
            url = FiveHundredPx.BASE_URL + '/users'
            data = self.use_authorized_client(authorized_client, url, **kwargs)
        else:
            data = self.request('/users/show', username=username, **kwargs)
        return data

    def get_photo_comments(self, photo_id, skip=None, rpp=20):
        if rpp != 20:
            """ It seems this does not work on the API """
            raise NotImplementedError
        
        if skip:
            page = skip / rpp
            skip -= page * rpp
            assert(skip >= 0) 
        page = 1
        while True:
            data = self.request('/photos/%s/comments' % photo_id, page=page, rpp=rpp)
            assert(page == data['current_page'])
            for comment in data['comments']:
                if skip:
                    skip -= 1
                    continue
                yield comment
            if page == data['total_pages']:
                break
            page += 1

    def get_blog_post_comments(self, blog_post_id, skip=None, rpp=20):
        if rpp != 20:
            """ It seems this does not work on the API """
            raise NotImplementedError

        if skip:
            page = skip / rpp
            skip -= page * rpp
            assert(skip >= 0) 
        page = 1
        while True:
            data = self.request('/blogs/%s/comments' % blog_post_id,
                                page=page,
                                rpp=rpp)
            assert(page == data['current_page'])
            for comment in data['comments']:
                if skip:
                    skip -= 1
                    continue
                yield comment
            if page == data['total_pages']:
                break
            page += 1
        
    def photo_search(self, term=None, tag=None, tags=None, skip=None, rpp=100):
        if skip:
            page = skip / rpp
            skip -= page * rpp
            assert(skip >= 0) 
        page = 1
        while True:
            kwargs = dict(page=page,
                          rpp=rpp)

            if not bool(tag) != bool(term):
                raise TypeError, "one and only one of tag xor term is needed"
            elif tag:
                kwargs['tag'] = tag
            elif term:
                kwargs['term'] = term
                
            if tags:
                kwargs['tags'] = tags

            data = self.request('/photos/search', **kwargs)
            assert(page == data['current_page'])
            for photo in data['photos']:
                if skip:
                    skip -= 1
                    continue
                yield photo
            if page == data['total_pages']:
                break
            page += 1
        
    def user_search(self, term, skip=None, rpp=100):
        if skip:
            page = skip / rpp
            skip -= page * rpp
            assert(skip >= 0) 
        page = 1
        while True:
            kwargs = dict(page=page,
                          rpp=rpp,
                          term=term)
            data = self.request('/users/search', **kwargs)
            assert(page == data['current_page'])
            for user in data['users']:
                if skip:
                    skip -= 1
                    continue
                yield user
            if page == data['total_pages']:
                break
            page += 1
        
    def get_user_friends(self, user_id, skip=None, rpp=100):
        if skip:
            page = skip / rpp
            skip -= page * rpp
            assert(skip >= 0) 
        page = 1
        while True:
            data = self.request('/users/%s/friends' % user_id, page=page, rpp=rpp)
            assert(page == data['page'])
            for friend in data['friends']:
                if skip:
                    skip -= 1
                    continue
                yield dict(user=friend)
            if page == data['friends_pages']:
                break
            page += 1

    def get_user_followers(self, user_id, skip=None, rpp=100):
        if skip:
            page = skip / rpp
            skip -= page * rpp
            assert(skip >= 0) 
        page = 1
        while True:
            data = self.request('/users/%s/followers' % user_id, page=page, rpp=rpp)
            assert(page == data['page'])
            for follower in data['followers']:
                if skip:
                    skip -= 1
                    continue
                yield dict(user=follower)
            if page == data['followers_pages']:
                break
            page += 1

    def get_user_blog_posts(self, user_id):
        page = 1
        while True:
            data = self.request('/blogs',
                                feature='user',
                                user_id=user_id,
                                page=page,
                                rpp=99)
            assert(page == data['current_page'])
            for blog_post in data['blog_posts']:
                yield blog_post
            if page == data['total_pages']:
                break
            page += 1
            
    def get_user_collections(self, authorized_client=None, user_id=None):
        data = None
        if user_id and not authorized_client:
            # User Collections have not been implemented for public 
            # queries to the API
            raise NotImplementedError
        elif user_id and authorized_client:
            # this should be handled by check to see if the user
            # id is the same as the owner of the authorized client
            # if it is, it should go through fine, otherwise it 
            # is not currently supported by the api
            raise NotImplementedError
        elif not authorized_client:
            assert(user_id)
            # this default case is interesting because it could be 
            # used to pull down all public collections. Hard to tell,
            # requires thought and possible api build out
            raise NotImplementedError
        elif authorized_client:
            assert(not user_id)
            url = FiveHundredPx.BASE_URL + '/collections'
            data = self.use_authorized_client(authorized_client, url)
        else:
            # this is an undefined state that should never be entered.
            # but since this portion of code needs to expansion, it needs
            # to be resistant against someone altering it in such a way 
            # that lets a case though.
            assert(False)
        return data["collections"]

    def get_collection(self, collection_id, authorized_client=None):
        url = FiveHundredPx.BASE_URL + '/collections/%s' % collection_id
        data = None
        if authorized_client:
            data = self.use_authorized_client(authorized_client, url)
        else:
            # Despite api documentation to the contrary, this call
            # actually does require api authentication
            raise NotImplementedError
            data = self.request(url)
        return data

    def user_favorites_photo(self, photo_id, authorized_client):
        url = FiveHundredPx.BASE_URL + '/photos/%s/favorite' % photo_id
        post_args = ""
        response = authorized_client.post(url, data=post_args)
        return response.status_code == 200

    def user_unfavorites_photo(self, photo_id, authorized_client):
        url = FiveHundredPx.BASE_URL + '/photos/%s/favorite' % photo_id
        response = authorized_client.delete(url)
        success = response.status_code == 200
        if not success:
            from pprint import pprint
            pprint(response.__dict__)
        return success

    def user_likes_photo(self, photo_id, authorized_client):
        url = FiveHundredPx.BASE_URL + '/photos/%s/vote?vote=1' % photo_id
        post_args = ""
        response = authorized_client.post(url, data=post_args)
        return response.status_code == 200

    def user_follows_user(self, user_id, authorized_client):
        """ The user_id is of the user to be followed. The authorized
        client is of the user doing the following.
        """
        url = FiveHundredPx.BASE_URL + '/users/%s/friends' % user_id
        post_args = ""
        response = authorized_client.post(url, data=post_args)
        return response.status_code == 200

    def user_unfollows_user(self, user_id, authorized_client):
        """ The user_id is of the user to be followed. The authorized
        client is of the user doing the unfollowing.
        """
        url = FiveHundredPx.BASE_URL + '/users/%s/friends' % user_id
        response = authorized_client.delete(url)
        return response.status_code == 200

    def user_comments_on_photo(self, photo_id, comment_body, authorized_client):
        url = FiveHundredPx.BASE_URL + '/photos/%s/comments' % photo_id
        post_args = dict(body=comment_body)
        response = authorized_client.post(url, data=post_args)
        return response.status_code == 200

    def user_comments_on_blog_post(self, blog_post_id,
                                   comment_body,
                                   authorized_client):
        url = FiveHundredPx.BASE_URL + '/blogs/%s/comments' % blog_post_id
        post_args = dict(body=comment_body)
        response = authorized_client.post(url, data=post_args)
        return response.status_code == 200

    def use_authorized_client(self,
                              authorized_client,
                              url,
                              post_args=None,
                              **kwargs):
        resp_data = None
        if not post_args:
            resp_data = _parse_json(authorized_client.get(url, **kwargs).content)
        else:
            resp_data = _parse_json(authorized_client.post(url,
                                                           data=post_args,
                                                           **kwargs))
        return resp_data

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
