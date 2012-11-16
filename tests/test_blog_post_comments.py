import unittest
import os
from fhp.models.blog_post_comment import BlogPostComment
from fhp.helpers.json_finder import _parse_json
from tests.settings import test_settings

class Test_retrieve_collection(unittest.TestCase):
    """ This tests the blog_post_comment class. """
    
    def setUp(self):
        self.test_settings = test_settings
        
    def test_init(self):
        """ Skipping this for now as it is covered in the blog post and user tests """
        pass
