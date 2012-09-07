import unittest
import os
from fhp.models.blog_post import BlogPost
from fhp.models.user import User
from fhp.helpers.json_finder import _parse_json


class Test_retrieve_collection(unittest.TestCase):

    def setUp(self):
        with open(os.path.join('fhp', 'config', 'test_settings.json')) as f:
            self.test_settings = _parse_json(f.read())

    def test_init(self):
        olegs_first_blog_post_id = 1
        first_blog_post = BlogPost(1)
        self.assertEqual(first_blog_post.id, 1)

    def test_user(self):
        olegs_first_blog_post_id = 1
        first_blog_post = BlogPost(1)
        self.assertEqual(first_blog_post.user.username, 'oleggutsol')

    def test_photos(self):
        awesome_blog_post_id = 27105
        awesome_blog_post = BlogPost(awesome_blog_post_id)
        freedom_photo_id = 5231155
        self.assertTrue(awesome_blog_post.photos)
        self.assertIn(freedom_photo_id, awesome_blog_post.photos)
    
    def test_photo_extends_properties(self):
        awesome_blog_post_id = 27105
        awesome_blog_post = BlogPost(awesome_blog_post_id)
        freedom_photo_id = 5231155
        self.assertEqual(awesome_blog_post.photos[freedom_photo_id].width, 1200)
        
    def test_empty_photos(self):
        """ Not all stories have photos """
        olegs_first_blog_post_id = 1
        first_blog_post = BlogPost(1)
        self.assertEqual(first_blog_post.user.username, 'oleggutsol')
        self.assertTrue(hasattr(first_blog_post, 'photos'))
        first_blog_post.photos
        self.assertFalse(first_blog_post.photos)

