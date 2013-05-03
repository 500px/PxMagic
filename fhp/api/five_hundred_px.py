"""
Created by @arthurnn on 2012-01-19.
Modified by @zachaysan - now it actually does stuff :)
"""
from functools import partial

import urllib
from fhp.helpers.json_finder import _parse_json

from fhp.helpers.http import http_request, smart_urlencode, finalize_oauth_client
from fhp.helpers.http import build_oauth_client_for_client, use_auth_url_fn
from fhp.helpers.http import multipart_post, paginate

class FiveHundredPx(object):
    BASE_URL = 'https://api.500px.com/v1'
    
    def __init__(self, consumer_key, consumer_secret, verify_url=None):
        """For more info on the API visit developer.500px.com.
        If you are logged in to your 500px account you can 
        go to: http://500px.com/settings/applications to retrieve
        your key.
        """
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        
        """ Verify URL is used for clients that want oauth'd access
        without a full fledged server. If you are building a webapp
        don't worry about this. If you are building a client that doesn't 
        need oauth, don't worry about this.
        """
        self.verify_url = verify_url

    def request(self, path, post_args=None, log_request=False, **kwargs):
        """Handles the actual request to 500px. Posting has yet 
        to be implemented.
        """

        if post_args:
            raise NotImplementedError
        self._set_consumer_key_to_args_(post_args, kwargs)
        base_url = FiveHundredPx.BASE_URL
        return http_request(base_url, path, post_args, log_request, **kwargs)

    """ PHOTOS """

    def get_photo(self, id, **kwargs):
        data = self.request('/photos/%d' % id, **kwargs)
        return data

    def create_new_photo_upload_key(self, authorized_client, **kwargs):
        url = FiveHundredPx.BASE_URL + '/photos'
        url = url + "?" + smart_urlencode(kwargs)
        data = ""
        response = authorized_client.post(url, data=data)
        response_data = _parse_json(response.content)
        return response_data

    def upload_photo(self, upload_key, photo_id, photo_file, authorized_client):
        """ This method is only useful for client side applications """
        files = {'file': photo_file}
        url = FiveHundredPx.BASE_URL + '/upload'
        access_key = authorized_client.access_token
        kwargs = dict(upload_key=upload_key,
                      photo_id=photo_id,
                      consumer_key=self.consumer_key,
                      access_key=access_key)
        url = url + "?" + smart_urlencode(kwargs)
        response = multipart_post(url, files=files)
        if response.status_code == 200:
            return True
        else:
            print response.content

    def get_photos(self, skip=None, rpp=20, authorized_client=None, **kwargs):
        if authorized_client:
            url = FiveHundredPx.BASE_URL + '/photos'
            request_function = partial(self.use_authorized_client, authorized_client, url, **kwargs)
        else:
            request_function = partial(self.request, '/photos', **kwargs)
        for photo in paginate(skip, rpp, request_function, 'photos'):
            yield photo

    def get_photo_comments(self, photo_id, skip=None, rpp=20):
        if rpp != 20:
            """ It seems this does not work on the API """
            raise NotImplementedError
        request_function = partial(self.request, '/photos/%s/comments' % photo_id)
        for photo_comment in paginate(skip, rpp, request_function, 'comments'):
            yield photo_comment

    def photo_search(self, term=None, tag=None, tags=None, skip=None, sort=None, rpp=100):
        kwargs = {}
        if not bool(tag) != bool(term):
            raise TypeError, "one and only one of tag xor term is needed"
        elif tag:
            kwargs['tag'] = tag
        elif term:
            kwargs['term'] = term
        if tags:
            kwargs['tags'] = tags
        request_function = partial(self.request, '/photos/search', **kwargs)
        for photo in paginate(skip, rpp, request_function, 'photos'):
            yield photo
        

    """ BLOG POSTS """
    
    def get_blog_post(self, id):
        blog_post = self.request('/blogs/%d' % id)
        return dict(blog_post=blog_post)

    def get_blog_post_comments(self, blog_post_id, skip=None, rpp=20):
        if rpp != 20:
            """ It seems this does not work on the API """
            raise NotImplementedError
        request_function = partial(self.request, '/blogs/%s/comments' % blog_post_id)
        for blog_post_comment in paginate(skip, rpp, request_function, 'comments'):
            yield blog_post_comment

    def get_user_blog_posts(self, user_id, skip=None, rpp=100):
        request_function = partial(self.request,
                                   '/blogs',
                                   feature='user',
                                   user_id=user_id)
        for blog_post in paginate(skip, rpp, request_function, "blog_posts"):
            yield blog_post
            
    """ USERS - Getting user information """
    def get_user_by_id(self, user_id, authorized_client=None, **kwargs):
        if 'username' in kwargs:
            raise TypeError, "get_user_by_id cannot handle a username param"
        if 'email' in kwargs:
            raise TypeError, "get_user_by_id cannot handle a email param"
        args = [user_id, authorized_client]
        if not any(args):
            raise TypeError, "One of user_id or authorized_client is needed"
        if all(args):
            # This needs to be refactored.
            # It is a direct symptom of combining 
            # authorized users and normal users into 
            # the same class.
            pass
        if authorized_client:
            data = self.get_by_authorized_client(authorized_client)
        else:
            data = self.request('/users/%d' % user_id, **kwargs)
        return data

    def get_user_by_username(self, username=None, authorized_client=None, **kwargs):
        if 'id' in kwargs:
            raise TypeError, "get_user_by_username cannot handle a user_id param"
        if 'email' in kwargs:
            raise TypeError, "get_user_by_id cannot handle a email param"
        args = [username, authorized_client]
        if not any(args) or all(args):
            raise TypeError, "One of username or authorized_client must be supplied"
        if authorized_client:
            data = self.get_by_authorized_client
        else:
            data = self.request('/users/show', username=username, **kwargs)
        return data

    def get_by_authorized_client(self, authorized_client, **kwargs):
        url = FiveHundredPx.BASE_URL + '/users'
        data = self.use_authorized_client(authorized_client, url, **kwargs)
        return data

    """ USERS - Getting users based off of criteria """
    def user_search(self, term, skip=None, rpp=100):
        request_function = partial(self.request, '/users/search', term=term)
        for user in paginate(skip, rpp, request_function, "users"):
            yield user
        
    def get_user_friends(self, user_id, skip=None, rpp=100):
        request_function = partial(self.request, '/users/%s/friends' % user_id)
        for friend in paginate(skip, rpp, request_function, "friends", "friends_pages"):
            yield friend

    def get_user_followers(self, user_id, skip=None, rpp=100):
        request_function = partial(self.request, '/users/%s/followers' % user_id)
        for follower in paginate(skip, rpp, request_function, "followers", "followers_pages"):
            yield follower

    """ USERS - Available actions """

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

    """ COLLECTIONS (also known as sets)"""

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

    """ AUTHENTICATION """

    def get_authorized_client(self,
                              auth_url_fn=None,
                              oauth_token=None,
                              oauth_secret=None,
                              oauth_verifier=None,
                              **kwargs):
        oauth_terms = [oauth_token, oauth_secret, oauth_verifier]
        if any(oauth_terms) != all(oauth_terms):
            raise TypeError, "all or none of oauth_terms must be supplied"
            
        request_url = FiveHundredPx.BASE_URL + "/oauth/request_token"
        authorize_url = FiveHundredPx.BASE_URL + "/oauth/authorize"
        access_token_url = FiveHundredPx.BASE_URL + "/oauth/access_token"

        client = None
        if all(oauth_terms):
            client = finalize_oauth_client(oauth_token,
                                           oauth_secret,
                                           oauth_verifier,
                                           self.consumer_key,
                                           self.consumer_secret,
                                           access_token_url)
        if not auth_url_fn:
            auth_url_fn = self.sample_auth_url_fn
            
        if client:
            return client
        return build_oauth_client_for_client(request_url=request_url,
                                             authorize_url=authorize_url,
                                             access_token_url=access_token_url,
                                             consumer_key=self.consumer_key,
                                             consumer_secret=self.consumer_secret,
                                             auth_url_fn=auth_url_fn,
                                             verify_url=self.verify_url)
    def use_authorized_client(self,
                              authorized_client,
                              url,
                              post_args=None,
                              skip=None,
                              rpp=None,
                              **kwargs):
        
        resp_data = None
        if skip:
            kwargs['skip'] = skip
        if rpp:
            kwargs['rpp'] = rpp
        if not post_args:
            url += "/?%s" % smart_urlencode(kwargs)
            resp_data = _parse_json(authorized_client.get(url).content)
        else:
            resp_data = _parse_json(authorized_client.post(url,
                                                           data=post_args,
                                                           **kwargs))
        return resp_data

    def get_oauth_token_and_secret(self, auth_url_fn=None):
        request_url = FiveHundredPx.BASE_URL + "/oauth/request_token"
        authorize_url = FiveHundredPx.BASE_URL + "/oauth/authorize"
        access_token_url = FiveHundredPx.BASE_URL + "/oauth/access_token"
        auth_url_fn = auth_url_fn or self.sample_auth_url_fn
        result = use_auth_url_fn(request_url=request_url,
                                 authorize_url=authorize_url,
                                 access_token_url=access_token_url,
                                 consumer_key=self.consumer_key,
                                 consumer_secret=self.consumer_secret,
                                 auth_url_fn=auth_url_fn)
        oauth_token, oauth_secret = result
        return oauth_token, oauth_secret

    """ EXAMPLES """

    def sample_auth_url_fn(self, authorization_url):
        from subprocess import call
        call(["google-chrome", authorization_url])
        accepted = 'n'
        while accepted.lower() == 'n':
            accepted = raw_input('Have you authorized me? (y/n) ')

    """ HELPERS """

    def _set_consumer_key_to_args_(self, post_args, kwargs):
        if post_args is not None:
            post_args["consumer_key"] = self.consumer_key
        else:
            kwargs["consumer_key"] = self.consumer_key

