import unittest
import os
from fhp.models.user_search import UserSearch
from fhp.helpers.json_finder import _parse_json
from tests.settings import test_settings

class Test_retrieve_user_search(unittest.TestCase):
    """ This tests the user_search class. User search is kinda
    strange because you kinda have to know *who* you are looking 
    for already.
    """
    
    def setUp(self):
        self.test_settings = test_settings
        self.Berliners = UserSearch(term="Berlin")
    
    def test_init(self):
        self.assertTrue(self.Berliners.first().username)
