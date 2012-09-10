import unittest
import os
from fhp.models.blog_post_comment import BlogPostComment
from fhp.helpers.json_finder import _parse_json

class Test_retrieve_collection(unittest.TestCase):
    """ This tests the blog_post_comment class. """
    
    def setUp(self):
        with open(os.path.join('fhp', 'config', 'test_settings.json')) as f:
            self.test_settings = _parse_json(f.read())
        
    def test_init(self):
        """ Skipping this for now as it is covered in the blog post and user tests """
        pass
