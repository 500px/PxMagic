from functools import partial

from fhp.src import fivehundred
from fhp.helpers import authentication

import fhp.models.collection
import fhp.models.blog_post

from fhp.magic.magic_cache import magic_cache, MagicFunctionCache
from fhp.magic.magic_object import magic_object
from fhp.magic.magic_generator import MagicGenerator

user_magic_fn_cache = MagicFunctionCache(ignore_caching_on=["data"])

@user_magic_fn_cache
def User(id=None, username=None, email=None, data=None, *args, **kwargs):
    if email:
        raise NotImplementedError
    if not bool(id) != bool(username):
        error = "user requires exactly 1 of id, username"
        error += "\n perhaps you meant to use a keyword argument"
        error += "\n like data=user_data?"
        raise TypeError, error
    if username and username in User.username_cache:
        user_id = User.username_cache[username]
        return User(user_id, data=data, *args, **kwargs)
    elif username:
        u = user(username=username, data=data, *args, **kwargs)
        return User(u.id, data=data, forced_return_value=u, *args, **kwargs)
    u = user(id, data=data, *args, **kwargs)
    User.username_cache[u.username] = u.id
    return u
User.username_cache = {}


class user(magic_object):
    five_hundred_px = fivehundred.FiveHundredPx(authentication.get_consumer_key(),
                                                authentication.get_consumer_secret())

    def __init__(self,
                 id=None,
                 username=None,
                 email=None,
                 data=None,
                 authorize=False):
        if email:
            raise NotImplementedError

        if not bool(id) != bool(username):
            raise TypeError, "user requires exactly 1 of id, username"
        
        self.authorized_client = None
        if authorize:
            self.authorize()
        data = data or self.get_long_public_user_data(id, username)
        user_data = data["user"]
        self.add_user_data(user_data)

    def add_user_data(self, user_data):
        for key in user_data:
            setattr(self, key, user_data[key])

    def authorize(self):
        self.authorized_client = user.five_hundred_px.get_authorized_client()

    def __getattr__(self, name):
        if name == 'friends':
            self._get_friends_()
            return self.friends
        elif name == 'followers':
            self._get_followers_()
            return self.followers
        elif name == 'collections':
            self._get_collections_()
            return self.collections
        elif name == 'blog_posts':
            self._get_blog_posts_()
            return self.blog_posts
        elif name in dir(self):
            data = self.get_long_public_user_data(self.id,
                                                  self.authorized_client)
            new_user_data = data["user"]
            self.add_user_data(new_user_data)
            return getattr(self, name)
        else:
            raise AttributeError, name

    def get_long_public_user_data(self, id=None, username=None):
        if id:
            result = user.five_hundred_px.get_user_by_id(id, self.authorized_client)
        elif username:
            result = user.five_hundred_px.get_user_by_username(username, self.authorized_client)
        else:
            raise NotImplementedError
        return result

    def find_friend(self, **kwargs):
        for friend in self.friends:
            is_match = True
            for kwarg in kwargs:
                if not getattr(friend, kwarg) == kwargs[kwarg]:
                    is_match = False
            if is_match:
                return friend

    def find_follower(self, **kwargs):
        for follower in self.followers:
            is_match = True
            for kwarg in kwargs:
                if not getattr(follower, kwarg) == kwargs[kwarg]:
                    is_match = False
            if is_match:
                return follower
            
    def follow(self, user):
        """ Warning: if you pass in a user_id instead of a user
        object then any user object you are currently using 
        will not be informed of the additional follower.

        This may be especially tricky if the followed user is
        and authenticated user (which takes up it's own object)
        """
        if hasattr(user, "id"):
            user_id = user.id
        else:
            user_id = user
            user = False
        result = user.five_hundred_px.user_follows_user(user_id,
                                                        self.authorized_client)
        if result:
            self.friends.max_length += 1
        if result and user:
            user.followers.max_length += 1
        return result 

    def unfollow(self, user):
        """ Warning: if you pass in a user_id instead of a user
        object then any user object you are currently using 
        will not be informed that it has lost a follower.

        This may be especially tricky if the followed user is
        and authenticated user (which takes up it's own object)
        """
        if hasattr(user, "id"):
            user_id = user.id
        else:
            user_id = user
            user = False
        result = user.five_hundred_px.user_unfollows_user(user_id,
                                                          self.authorized_client)
        # This is necessary since we do not know where in the result
        # set the user was.
        if result:
            self.friends.reset_cache()
        if result and user:
            user.followers.reset_cache()
        return result 

    def _get_friends_(self):
        iter_source = partial(user.five_hundred_px.get_user_friends, self.id)
        def build_user(data):
            user_id = data["user"]['id']
            return User(user_id, data=data)
        self.friends = MagicGenerator(iter_source=iter_source,
                                      iter_destination=build_user)
        
    def _get_followers_(self):
        iter_source = partial(user.five_hundred_px.get_user_followers, self.id)
        def build_user(data):
            user_id = data["user"]['id']
            return User(user_id, data=data)
        self.followers = MagicGenerator(iter_source=iter_source,
                                      iter_destination=build_user)
    
    def favorite(self, photo):
        """ Returns True upon successful favoriting """
        photo_id = self._get_photo_id_(photo)
        return user.five_hundred_px.user_favorites_photo(photo_id,
                                                         self.authorized_client)
    
    def unfavorite(self, photo):
        photo_id = self._get_photo_id_(photo)
        return user.five_hundred_px.user_unfavorites_photo(photo_id,
                                                           self.authorized_client)
    def _get_photo_id_(self, photo):
        return photo.id if hasattr(photo, 'id') else photo
        
    def like(self, photo):
        photo_id = self._get_photo_id_(photo)
        return user.five_hundred_px.user_likes_photo(photo_id,
                                                     self.authorized_client)
    
    def dislike(self, photo):
        """ Since there is no way in the API to find out if a user is 
        able to dislike a photo I've decided not to implement it for 
        now. Remember: A dislike is NOT an unlike. It is a seperate action
        that only qualified users can take. The vast majority of 500px 
        users are not able to dislike a photo.
        """
        raise NotImplementedError

    def comment_on_photo(self, photo, comment_body):
        photo_id = self._get_photo_id_(photo)
        response = user.five_hundred_px.user_comments_on_photo(photo_id,
                                                               comment_body,
                                                               self.authorized_client)

        """ To stop the photo from incorrectly thinking that it has fully 
        cached the comments on the photo we increase the max length by 1.
        of course this will not stop the requirment to nuke the caches 
        from time to time anyways.
        """
        fhp.models.photo.Photo(photo_id).comments.max_length += 1
        return response
    

    def comment_on_blog_post(self, blog_post, comment_body):
        blog_post_id = blog_post.id if hasattr(blog_post, 'id') else blog_post

        resp = user.five_hundred_px.user_comments_on_blog_post(blog_post_id,
                                                               comment_body,
                                                               self.authorized_client)
        fhp.models.blog_post.BlogPost(blog_post_id).comments.max_length += 1
        return resp
    
    @magic_cache
    def _get_collections_(self):
        self.collections = {}
        kwargs = dict(authorized_client=self.authorized_client)
        collections = user.five_hundred_px.get_user_collections(**kwargs)
        for collection in collections:
            col_id = collection["id"]
            self.collections[col_id] = fhp.models.collection.Collection(col_id, collection)
    @magic_cache
    def _get_blog_posts_(self):
        self.blog_posts = {}
        for blog_post in user.five_hundred_px.get_user_blog_posts(self.id):
            blog_post_id = blog_post['id']
            data = {"blog_post": blog_post}
            self.blog_posts[blog_post_id] = fhp.models.blog_post.BlogPost(blog_post_id,
                                                                      data=data,
                                                                      user=self)

    def __dir__(self):
        results = ['domain',
                   'locale',
                   'store_on',
                   'sex',
                   'id',
                   'city',
                   'userpic_url',
                   'photos_count',
                   'friends_count',
                   'contacts',
                   'followers_count',
                   'equipment',
                   'state',
                   'upgrade_status',
                   'show_nude',
                   'username',
                   'firstname',
                   'lastname',
                   'registration_date',
                   'birthday',
                   'in_favorites_count',
                   'about',
                   'country',
                   'fotomoto_on',
                   'fullname',
                   'affection',
                   'blog_posts']
        return results
