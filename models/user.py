from src import fivehundred
from helpers import authentication

from magic.magic_cache import magic_cache, magic_fn_cache
from magic.magic_object import magic_object

@magic_fn_cache
def User(id):
    return user(id)

class user(magic_object):
    five_hundred_px = fivehundred.FiveHundredPx(authentication.get_consumer_key())
    def __init__(self, id):
        self.id = id
        data = user.five_hundred_px.get_user(id)
        user_data = data["user"]
        self.add_user_data(user_data)

    def add_user_data(self, user_data):
        for key in user_data:
            setattr(self, key, user_data[key])
