import unittest
import os
from fhp.models.collection import Collection
from fhp.models.user import User
from fhp.helpers.json_finder import _parse_json
from tests.settings import test_settings

class Test_retrieve_collection(unittest.TestCase):
    """ This tests the collection class.

    Since collections requires authorization at this time
    it is hard to write full integration tests without being user
    specific. Ultimately a combination of mocks and non-auth checks
    should be implemented.
    """
    
    def setUp(self):
        self.test_settings = test_settings

        authorized_client = None
        if self.test_settings['oauth']:
            zachaysan = User(403022, authorize=True)
            authorized_client = zachaysan.authorized_client
            self.test_collection = Collection(383355,
                                              authorized_client=authorized_client)

    def test_init(self):
        if not self.test_settings['ignore_known_failing_tests']:
            test_collection = Collection(383355)
            self.assertEqual(test_collection.id, 383355)
            
    def test_oauthed_init(self):
        if self.test_settings['oauth']:
            self.assertEqual(self.test_collection.id, 383355)
            
    def test_creating_collection(self):
        pass

    def test_deleting_collection(self):
        pass
    
    def test_editing_collection(self):
        pass
