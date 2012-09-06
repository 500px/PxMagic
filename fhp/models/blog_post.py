from fhp.src import fivehundred
from fhp.helpers import authentication

import fhp.models.photo

from fhp.magic.magic_cache import magic_cache, magic_fn_cache
from fhp.magic.magic_object import magic_object

@magic_fn_cache
def BlogPost(id, *args, **kwargs):
    return blog_post(id, *args, **kwargs)

class blog_post(magic_object):
    five_hundred_px = fivehundred.FiveHundredPx(authentication.get_consumer_key(),
                                                authentication.get_consumer_secret())
    
    def __init__(self, id, data=None, authorized_client=None, user=None):
        self.id = id
        self.authorized_client = authorized_client
        data = data or self.get_long_public_blog_post_data(id)
        self.add_blog_post_data(data['blog_post'], user=user)
        
    def add_blog_post_data(self, blog_post_data, user=None):
        if user:
            self.user = user
            del(blog_post_data['user'])
        for key in blog_post_data:
            setattr(self, key, blog_post_data[key])

        
