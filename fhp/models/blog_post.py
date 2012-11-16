from functools import partial

from fhp.api import five_hundred_px
from fhp.helpers import authentication

import fhp.models.photo
import fhp.models.user
import fhp.models.blog_post_comment

from fhp.magic.magic_cache import magic_cache, magic_fn_cache
from fhp.magic.magic_object import magic_object
from fhp.magic.magic_generator import MagicGenerator

@magic_fn_cache
def BlogPost(id, *args, **kwargs):
    return blog_post(id, *args, **kwargs)

class blog_post(magic_object):
    five_hundred_px = five_hundred_px.FiveHundredPx(authentication.get_consumer_key(),
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
        elif 'user' in blog_post_data:
            self.user_id = blog_post_data['user']['id']
            del(blog_post_data['user'])
        
        if 'photos' in blog_post_data:
            self._make_photos_(blog_post_data['photos'])
            del(blog_post_data['photos'])

        for key in blog_post_data:
            setattr(self, key, blog_post_data[key])

    def get_long_public_blog_post_data(self, blog_post_id):
        data = blog_post.five_hundred_px.get_blog_post(blog_post_id)
        return data
                

    def __getattr__(self, name):
        if name == 'user':
            return self._get_user_(self.user_id)
        elif name == 'photos':
            data = self.get_long_public_blog_post_data(self.id)
            photo_data = data.get('photos', {})
            self._make_photos_(photo_data)
            return self.photos
        elif name == 'comments':
            self._get_comments_()
            return self.comments
        else:
            raise AttributeError

    @magic_cache
    def _get_user_(self, user_id):
        return fhp.models.user.User(self.user_id)

    def _get_comments_(self):
        iter_source = partial(blog_post.five_hundred_px.get_blog_post_comments,
                              self.id)
        def build_comment(blog_post_id, comment_data):
            return fhp.models.blog_post_comment.BlogPostComment(comment_data["id"],
                                                                blog_post_id,
                                                                comment_data)
        iter_destination = partial(build_comment, self.id)
        self.comments = MagicGenerator(iter_source=iter_source,
                                       iter_destination=iter_destination)

                
    def _make_photos_(self, photo_data):
        self.photos = {}
        for photo in photo_data:
            photo_id = photo['id']
            self.photos[photo_id] = fhp.models.photo.Photo(photo_id)
