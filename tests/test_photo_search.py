import unittest
import os
from fhp.models.photo_search import PhotoSearch
from fhp.helpers.json_finder import _parse_json
from tests.settings import test_settings

class Test_retrieve_photo_search(unittest.TestCase):
    """ This tests the photo_search class. """
    
    def setUp(self):
        self.test_settings = test_settings
        self.nature_photos = PhotoSearch(tag='nature')
    
    def test_init(self):
        self.assertTrue(self.nature_photos.first().name)
        
    def test_return_with_tags(self):
        self.assertFalse('tags' in self.nature_photos.first().__dict__)
        self.assertTrue('tags' in dir(self.nature_photos.first()))
        missile_photo = PhotoSearch(tag='missile', tags=True).first()
        self.assertTrue('tags' in missile_photo.__dict__)
        self.assertTrue('tags' in dir(missile_photo))

