from src import fivehundred
from helpers import authentication

from magic.magic_cache import magic_cache, magic_fn_cache
from magic.magic_object import magic_object

@magic_fn_cache
def User(id, *args, **kwargs):
    return user(id, *args, **kwargs)

class user(magic_object):
    five_hundred_px = fivehundred.FiveHundredPx(authentication.get_consumer_key(),
                                                authentication.get_consumer_secret())

    def __init__(self, id, data=None, authorize=False):
        self.id = id
        self.authorized_request_client = None
        if authorize:
            self.authorize()
        data = data or user.five_hundred_px.get_user(id,
                                                     self.authorized_request_client)
        user_data = data["user"]
        self.add_user_data(user_data)

    def add_user_data(self, user_data):
        for key in user_data:
            setattr(self, key, user_data[key])

    def authorize(self):
        self.authorized_request_client = user.five_hundred_px.get_authorized_client()

    def __getattr__(self, name):
        if name == 'friends':
            self._get_friends_()
            return self.friends
        elif name == 'followers':
            self._get_followers_()
            return self.followers
        else:
            raise AttributeError

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
        
