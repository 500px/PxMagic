import unittest
from tests.test_user import Test_retrieve_user

def suite():
    suite = unittest.TestSuite()
    suite.addTest(Test_retrieve_user('test_oauth_with_oauth'))
    return suite


def main():
    s = suite()
    all_tests = unittest.TestSuite([s])
    unittest.TextTestRunner().run(all_tests)

if __name__ == '__main__':
    main()
