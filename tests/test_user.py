import unittest
import os

from fhp.models.user import User
from fhp.models.photo import Photo
from fhp.models.blog_post import BlogPost
from fhp.helpers.json_finder import _parse_json
from fhp.helpers.http import retrieve_oauth_verifier
from tests.settings import test_settings

class Test_retrieve_user(unittest.TestCase):
    def setUp(self):
        self.zachaysan = User(403022)
        self.test_settings = test_settings
        if self.test_settings['oauth']:
            self.auth_zach = User(403022, authorize=True)

    def test_init(self):
        self.assertEqual(self.zachaysan.id, 403022)
        
    def test_username(self):
        self.assertEqual(self.zachaysan.username, 'zachaysan')

    def test_init_with_username(self):
        zachaysan = User(username='zachaysan')
        self.assertEqual(zachaysan.id, self.zachaysan.id)

    def test_init_with_username_ensure_same_object_as_id_lookup(self):
        zachaysan = User(username='zachaysan')
        self.assertEqual(zachaysan.__hash__(),
                         self.zachaysan.__hash__())

    def test_init_with_username_first_then_id(self):
        arragorn = User(username='arragorn')
        arragorn_again = User(1354783)
        self.assertEqual(arragorn.__hash__(),
                         arragorn_again.__hash__())

    def test_auth_without_oauth(self):
        self.assertFalse(hasattr(self.zachaysan, 'auth'))
        
    def test_oauth_with_oauth(self):
        if self.test_settings['oauth']:
            api_test_user = self.auth_zach
            self.assertTrue(hasattr(api_test_user, 'auth'))
    
    def test_two_stage_oauth(self):
        if self.test_settings['oauth']:
            zachaysan = User(403022, force_fn_call=True)
            verify_url = zachaysan.five_hundred_px.verify_url
            zachaysan.initialize_authorization()
            # Normally, at this point, you would break this into 
            # the section of code that the user would hit on your site
            # *after* they finished authorizing (so the webserver would 
            # pick it up there) but since I don't want to run the tests
            # as a web server + client, I'm re-creating the lightweight 
            # verifier app.
            oauth_token = zachaysan._oauth_token
            oauth_verifier = retrieve_oauth_verifier(oauth_token, verify_url)
            zachaysan.complete_authorization(oauth_verifier)
            self.assertTrue(zachaysan.auth)

    def test_friends(self):
        evgenys_id = 1
        evgenys_username = 'tchebotarev'
        friend_evgeny = self.zachaysan.find_friend(id=evgenys_id)
        self.assertEqual(evgenys_id, friend_evgeny.id)
        friend_evgeny = self.zachaysan.find_friend(username=evgenys_username)
        self.assertEqual(evgenys_username, friend_evgeny.username)
    
    def test_friends_is_same_object_when_before(self):
        evgenys_id = 1
        friend_evgeny = self.zachaysan.find_friend(id=evgenys_id)
        self.assertEqual(evgenys_id, friend_evgeny.id)
        evgeny = User(evgenys_id)
        self.assertEqual(friend_evgeny.__hash__(),
                         evgeny.__hash__())

    def test_friends_is_same_object_when_after(self):
        evgenys_id = 1
        evgeny = User(evgenys_id)
        zachaysan = User(username='zachaysan')
        friend_evgeny = self.zachaysan.find_friend(id=evgenys_id)
        self.assertEqual(friend_evgeny.__hash__(),
                         evgeny.__hash__())

    def test_stories(self):
        olegs_id = 2
        oleg = User(olegs_id)
        oleg.blog_posts
        self.assertTrue(hasattr(oleg, 'blog_posts'))
        """ Oleg wrote the first blog post :) """
        self.assertIn(1, oleg.blog_posts)

    def test_story_retrival_in_proper_order(self):
        pass

    def test_friends_auto_build_needed_data(self):
        """ Since less data is sent from the api when 
        pulling a list of friends, we need the user
        model to update itself if we request an attribute
        that it should have automatically.
        """
        self.assertTrue(hasattr(self.zachaysan, 'friends'))
        evgenys_id = 1
        self.assertTrue('affection' in dir(self.zachaysan.friends[evgenys_id]))
        self.assertTrue(self.zachaysan.friends[evgenys_id].affection > 5)
        
    def test_followers(self):
        evgenys_id = 1
        evgenys_username = 'tchebotarev'
        self.assertTrue(hasattr(self.zachaysan, 'followers'))
        follower_evgeny = self.zachaysan.find_follower(id=evgenys_id)
        self.assertEqual(evgenys_id, follower_evgeny.id)
        follower_evgeny = self.zachaysan.find_follower(username=evgenys_username)
        self.assertEqual(evgenys_username, follower_evgeny.username)

    def test_friends_auto_build_needed_data(self):
        """ Since less data is sent from the api when 
        pulling a list of friends, we need the user
        model to update itself if we request an attribute
        that it should have automatically.
        """
        evgenys_id = 1
        friend_evgeny = self.zachaysan.find_friend(id=evgenys_id)
        self.assertTrue('affection' in dir(friend_evgeny))
        self.assertTrue(friend_evgeny > 5)
    
    def test_collection_pulling(self):
        if not self.test_settings['ignore_known_failing_tests']:
            evgenys_id = 1
            evgeny = User(evgenys_id)
            self.assertTrue(evgeny.collections)
 
    def test_self_collection_pulling_with_oauth(self):
        if self.test_settings['oauth']:
            zachaysan = self.auth_zach
            zachaysan.collections
            self.assertTrue(hasattr(zachaysan, 'collections'))
            self.assertIn(383355, zachaysan.collections)
            
    def test_user_favorite(self):
        """ Normally I would split these into their own tests, but 
        they need to proceed sequentially or I may get an error due
        to trying to "unfavorite" a photo I've already unfavorited.
        """
        if self.test_settings['oauth']:
            photo_id = 10005987
            self.assertTrue(self.auth_zach.favorite(photo_id))
            self.assertTrue(self.auth_zach.unfavorite(photo_id))
            photo = Photo(photo_id)
            self.assertTrue(self.auth_zach.favorite(photo))
            self.assertTrue(self.auth_zach.unfavorite(photo))

    def test_user_favorites(self):
        liberty_photo_id = 5431246
        favorites = (photo.id for photo in self.zachaysan.favorites)
        self.assertIn(liberty_photo_id, favorites)

    def test_user_likes(self):
        """ Since there is no way to unlike something with the 
        500px app / API, we are only left with the option to 
        have an annoying test where we find something to actually like.
        """
        annoying_test = not self.test_settings['ignore_annoying_tests']
        if self.test_settings['oauth'] and annoying_test:
            photo = Photo(13473159)
            self.assertTrue(self.auth_zach.like(photo))

    def test_comment_on_photo(self):
        annoying_test = not self.test_settings['ignore_annoying_tests']
        if self.test_settings['oauth'] and annoying_test:
            old_photo = Photo(10)
            comment_body = """sweet photo Ev! Sorry if this gets posted a 
bunch of times, I'm testing out the api and there is no delete method in the api"""
            self.auth_zach.comment_on_photo(old_photo, comment_body)

    def test_comment_on_blog_post(self):
        annoying_test = not self.test_settings['ignore_annoying_tests']
        if self.test_settings['oauth'] and annoying_test:
            working_blog_post = BlogPost(50163)
            comment_body = "And this is where I work on making comments on stories from the api :) <3"
            self.auth_zach.comment_on_blog_post(working_blog_post, comment_body)
        
    def test_asking_for_an_oauth_only_resource_from_a_nonowned_user_id(self):
        pass

    def test_list_photos_a_user_has_taken(self):
        paddy = User(username="tapi")
        self.assertTrue(paddy.photos.first())
        self.assertEqual(paddy.find_photo(name="Llama!").category_name, "Animals")

    def test_user_can_create_new_photo(self):
        annoying_test = not self.test_settings['ignore_annoying_tests']
        if self.test_settings['oauth']:
            photo_details = dict(name="fancy test photo of me flying",
                                 description="This is a photo that ev took",
                                 category="7",
                                 shutter_speed="1/40",
                                 focal_length="100",
                                 aperture="f2.4",
                                 camera="iPhone",
                                 lens="glass",
                                 privacy="1")
            """ Note that test_photo is a photo_object *without* an accompanying 
            photo, so some functionality may be broken until the photo has been
            uploaded
            """
            upload_key, test_photo = self.auth_zach.add_photo(**photo_details)
            self.assertTrue(upload_key and test_photo)
            # Note, you will not normally need to do this part unless
            # you are building a local client or something
            photo_file = open("tests/zach.jpg", "rb")
            successful_response = self.auth_zach.upload_photo(upload_key,
                                                              test_photo,
                                                              photo_file)
            self.assertTrue(successful_response)
            
    def test_follow_and_unfollow_user(self):
        """ Normally these would be two tests but I can't 
        guarantee execution order.
        """
        if self.test_settings['oauth']:
            zachapitest = User(username="zachapitest")
            self.assertTrue(self.auth_zach.follow(zachapitest))
            self.assertTrue(self.auth_zach.find_friend(username="zachapitest"))
            self.assertTrue(zachapitest.find_follower(username="zachaysan"))
            self.assertTrue(self.auth_zach.unfollow(zachapitest))
            no_friend = self.auth_zach.find_friend(username="zachapitest")
            no_follower = zachapitest.find_follower(username="zachaysan")
            self.assertTrue(no_friend is None)
            self.assertTrue(no_follower is None)

    def test_super_amounts_of_magic_in_user_dont_interfere_with_force_fn_call(self):
        pass

    def test_that_non_sample_auth_fns_can_be_used_with_the_auth_client(self):
        pass
