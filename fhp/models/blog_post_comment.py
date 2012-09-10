from fhp.src import fivehundred
from fhp.helpers import authentication

import fhp.models.blog_post
import fhp.models.user

from fhp.magic.magic_cache import magic_cache, MagicFunctionCache
from fhp.magic.magic_object import magic_object

blog_post_comment_magic_fn_cache = MagicFunctionCache(ignore_caching_on=["data"])

@blog_post_comment_magic_fn_cache
def BlogPostComment(id, *args, **kwargs):
    return blog_post_comment(id, *args, **kwargs)

class blog_post_comment(magic_object):
    five_hundred_px = fivehundred.FiveHundredPx(authentication.get_consumer_key(),
                                                authentication.get_consumer_secret())

    def __init__(self, id, blog_post_id, data):
        self.id = id
        self.blog_post_id = blog_post_id
        self.add_blog_post_comment_data(data)

    def add_blog_post_comment_data(self, data):
        for key in data:
            if key == 'user':
                user_data = dict(user=data["user"])
                self.user = fhp.models.user.User(self.user_id, data=user_data)
                continue
            setattr(self, key, data[key])

    def __getattr__(self, name):
        if name == 'blog_post':
            self._get_blog_post_(self.blog_post_id)
            return self.blog_post
        if name == 'user':
            self._get_user_(self.user_id)
            return self.user
        if name == 'to_whom_user':
            self._get_to_whom_user_(self.to_whom_user_id)
            return self.to_whom_user
        if name == 'parent':
            self._get_parent_(self.parent_id)
            return self.parent
        else:
            raise AttributeError
        
    def _get_blog_post_(self, blog_post_id):
        self.blog_post = fhp.models.blog_post.BlogPost(blog_post_id)

    def _get_user_(self, user_id):
        self.user = fhp.models.user.User(user_id)
        
    def _get_to_whom_user_(self, to_whom_user_id):
        self.to_whom_user = fhp.models.user.User(to_whom_user_id)

    def _get_parent_(self, parent_id):
        """ Since there is no way to get the information for 
        a single comment without having sumbled across it 
        while pulling down the rest of the comments for a blog post
        we just have to hope it is in there, or assume it is None.
        """
        self.parent = None
        if self.parent_id:
            try:
                # Note that we are excluding any data here, hoping to 
                # hit upon the cached blog post comment, if an error is raised
                # then we'll just have to treat it as if this is a root 
                # comment
                self.parent = BlogPostComment(self.parent_id, self.blog_post_id)
            except TypeError:
                pass
