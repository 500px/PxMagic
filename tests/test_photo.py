import unittest
from fhp.models.photo import Photo
from tests.settings import test_settings

class Test_retrieve_photo(unittest.TestCase):
    def setUp(self):
        self.owly_photo = Photo(3256058)
        self.test_settings = test_settings

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

        different_users_owly_photo = Photo(1763176)
        self.assertNotEqual(owly_photo.__hash__(), different_users_owly_photo.__hash__())
        self.assertNotEqual(owly_photo.image_url, different_users_owly_photo.image_url)
        
        self.assertEqual(owly_photo.user.__hash__(),
                         same_owly_photo.user.__hash__())
        self.assertNotEqual(owly_photo.user.__hash__(),
                            different_users_owly_photo.user.__hash__())
        
        same_users_different_owly_photo = Photo(3255978)
        self.assertNotEqual(owly_photo.__hash__(), same_users_different_owly_photo.__hash__())
        self.assertEqual(owly_photo.user.__hash__(),
                         same_users_different_owly_photo.user.__hash__())
        
    def test_dir_for_magic_user_generation(self):
        self.assertIn('user', dir(self.owly_photo))
        
    def test_photo_autogens_user(self):
        user = self.owly_photo.user
        self.assertEqual(user.username, 'AlexThomson')

    def test_edit_photo(self):
        pass
        
    def test_photo_comments(self):
        comment = self.owly_photo.comments.first()
        self.assertEqual(comment.body, "Awesome. Great capture!")
    
    def test_user_can_tag_photo(self):
        pass
    
    def test_photo_has_tags(self):
        marching_owl = Photo(897276)
        self.assertTrue(marching_owl.tags)
        self.assertIn('marching', marching_owl.tags)
        self.assertIn('owl', marching_owl.tags)

    def test_favorite_photo(self):
        pass
    
    def test_delete_photo(self):
        pass
    
    def test_delete_photo_tag(self):
        pass
    
    def test_delete_photo_favorite(self):
        pass

    def test_create_photo(self):
        """ This is a compicated procedure that involves
        using a two call approach """
        pass
    
    def test_upload_image_to_newly_created_photo_resource(self):
        pass
