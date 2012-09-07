from fhp.src import fivehundred
from fhp.helpers import authentication

import fhp.models.collection
import fhp.models.blog_post

from fhp.magic.magic_cache import magic_cache, magic_fn_cache
from fhp.magic.magic_object import magic_object

@magic_fn_cache
def User(id=None, username=None, email=None, *args, **kwargs):
    if email:
        raise NotImplementedError
    if not bool(id) != bool(username):
        raise TypeError, "user requires exactly 1 of id, username"
    if username and username in User.username_cache:
        user_id = User.username_cache[username]
        return User(user_id, *args, **kwargs)  
    elif username:
        u = user(username=username, *args, **kwargs)
        return User(u.id, forced_return_value=u, *args, **kwargs)
    u = user(id, *args, **kwargs)
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

    @magic_cache
    def _get_friends_(self):
        self.friends = {}
        for friend in user.five_hundred_px.get_user_friends(self.id):
            friend_id = friend['id']
            friend_username = friend['username']
            friend_user = User(friend_id, data={"user": friend})
            self.friends[friend_id] = friend_user
            self.friends[friend_username] = friend_user
        
    @magic_cache
    def _get_followers_(self):
        self.followers = {}
        for follower in user.five_hundred_px.get_user_followers(self.id):
            follower_id = follower['id']
            follower_username = follower['username']
            follower_user = User(follower_id, data={"user": follower})
            self.followers[follower_id] = follower_user
            self.followers[follower_username] = follower_user
            
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
