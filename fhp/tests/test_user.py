import unittest
import os
from fhp.models.user import User
from fhp.helpers.json_finder import _parse_json

class Test_retrieve_user(unittest.TestCase):
    def setUp(self):
        self.zachaysan = User(403022)
        with open(os.path.join('fhp', 'config', 'test_settings.json')) as f:
            self.test_settings = _parse_json(f.read())

    def test_init(self):
        self.assertEqual(self.zachaysan.id, 403022)
        
    def test_username(self):
        self.assertEqual(self.zachaysan.username, 'zachaysan')

    def test_auth_without_oauth(self):
        self.assertFalse(hasattr(self.zachaysan, 'auth'))
        
    def test_oauth_with_auth(self):
        if self.test_settings['oauth']:
            api_test_user = User(1264083, authorize=True)
            self.assertTrue(hasattr(api_test_user, 'auth'))
            
    def test_friends(self):
        evgenys_id = 1
        evgenys_username = 'tchebotarev'
        
        olegs_id = 2
        olegs_username = 'oleggutsol'

        self.assertIn(evgenys_id, self.zachaysan.friends)
        self.assertIn(evgenys_username, self.zachaysan.friends)

        self.assertIn(olegs_id, self.zachaysan.friends)
        self.assertIn(olegs_username, self.zachaysan.friends)

        self.assertEqual(self.zachaysan.friends[olegs_id].username, olegs_username)

    def test_friends_auto_build_needed_data(self):
        """ Since less data is sent from the api when 
        pulling a list of friends, we need the user
        model to update itself if we request an attribute
        that it should have automatically.
        """
        evgenys_id = 1
        self.assertTrue('affection' in dir(self.zachaysan.friends[evgenys_id]))
        self.assertTrue(self.zachaysan.friends[evgenys_id].affection > 5)
        

    def test_followers(self):
        evgenys_id = 1
        evgenys_username = 'tchebotarev'
        
        self.assertIn(evgenys_id, self.zachaysan.followers)
        self.assertIn(evgenys_username, self.zachaysan.followers)

        self.assertEqual(self.zachaysan.followers[evgenys_id].username, evgenys_username)

    def test_followers_auto_build_needed_data(self):
        """ Since less data is sent from the api when 
        pulling a list of friends, we need the user
        model to update itself if we request an attribute
        that it should have automatically.
        """
        evgenys_id = 1
        self.assertTrue('affection' in dir(self.zachaysan.friends[evgenys_id]))
        self.assertTrue(self.zachaysan.friends[evgenys_id].affection > 5)
        
    def test_collection_pulling(self):
        if not self.test_settings['ignore_known_failing_tests']:
            evgenys_id = 1
            evgeny = User(evgenys_id)
            self.assertTrue(evgeny.collections)
 
    def test_self_collection_pulling_with_oauth(self):
        if self.test_settings['oauth']:
            zachaysan = User(403022, authorize=True)
            zachaysan.collections
            self.assertTrue(hasattr(zachaysan, 'collections'))
            self.assertIn(383355, zachaysan.collections)
            
    def test_asking_for_an_oauth_only_resource_from_a_nonowned_user_id(self):
        pass
    
