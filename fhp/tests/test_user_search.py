import unittest
import os
from fhp.models.user_search import UserSearch
from fhp.helpers.json_finder import _parse_json

class Test_retrieve_user_search(unittest.TestCase):
    """ This tests the user_search class. User search is kinda
    strange because you kinda have to know *who* you are looking 
    for already.
    """
    
    def setUp(self):
        with open(os.path.join('fhp', 'config', 'test_settings.json')) as f:
            self.test_settings = _parse_json(f.read())
        self.Berliners = UserSearch(term="Berlin")
    
    def test_init(self):
        self.assertTrue(self.Berliners.first().username)
