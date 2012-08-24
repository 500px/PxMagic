import unittest
from models.photo import Photo

class Test_retrieve_photo(unittest.TestCase):
    def setUp(self):
        self.owly_photo = Photo(3256058)

    def test_init(self):
        self.assertEqual(self.owly_photo.id, 3256058)
    
    def test_nsfw(self):
        self.assertFalse(self.owly_photo.nsfw)
        
    def test_status(self):
        self.assertEqual(self.owly_photo.status, 1)
        
    def test_status_name(self):
        self.assertEqual(self.owly_photo.status_name, 'status_active')

    def test_photos_user_cache(self):
        owly_photo = Photo(3256058)
        same_owly_photo = Photo(3256058)
        self.assertEqual(owly_photo.__hash__(), same_owly_photo.__hash__())

        different_owly_photo = Photo(4600083)
        self.assertNotEqual(owly_photo.__hash__(), different_owly_photo.__hash__())
        self.assertNotEqual(owly_photo.image_url, different_owly_photo.image_url)
        
    def test_dir_for_magic_user_generation(self):
        self.assertIn('user', dir(self.owly_photo))
        
    def test_photo_autogens_user(self):
        user = self.owly_photo.user
        self.assertEqual(user.username, 'AlexThomson')
