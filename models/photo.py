from src import fivehundred
from helpers import authentication

import models.user as user

from magic.magic_cache import magic_cache, magic_fn_cache
from magic.magic_object import magic_object

@magic_fn_cache
def Photo(id, *args, **kwargs):
    return photo(id)

class photo(magic_object):
    five_hundred_px = fivehundred.FiveHundredPx(authentication.get_consumer_key(),
                                                authentication.get_consumer_secret())
    def __init__(self, id, data=None):
        self.id = id
        data = data or photo.five_hundred_px.get_photo(id)
        photo_data = data["photo"]
        self.add_photo_data(photo_data)
        
    def add_photo_data(self, photo_data):
        for key in photo_data:
            if key == 'user':
                continue
            elif key == 'category':
                self.add_category_name(photo_data['category'])
            elif key == 'status':
                self.add_status_name(photo_data['status'])
            setattr(self, key, photo_data[key])

    def add_category_name(self, category_number):
        categories = {0: 'Uncategorized',
                      1: 'Celebrities',
                      2: 'Film',
                      3: 'Journalism',
                      4: 'Nude',
                      5: 'Black and White',
                      6: 'Still Life',
                      7: 'People',
                      8: 'Landscapes',
                      9: 'City and Architecture',
                      10: 'Abstract',
                      11: 'Animals',
                      12: 'Macro',
                      13: 'Travel',
                      14: 'Fashion',
                      15: 'Commercial',
                      16: 'Concert',
                      17: 'Sport',
                      18: 'Nature',
                      19: 'Performing Arts',
                      20: 'Family',
                      21: 'Street',
                      22: 'Underwater',
                      23: 'Food',
                      24: 'Fine Art',
                      25: 'Wedding',
                      26: 'Transportation',
                      27: 'Urban Exploration'}
        if category_number in categories:
            self.category_name = categories[category_number]
        else:
            self.category_name = "unknown"

    def add_status_name(self, status_number):
        status = {8: 'status_uploaded',
                  0: 'status_created',
                  1: 'status_active',
                  7: 'status_inactive_user_photo',
                  9: 'status_deleted',
                  6: 'status_file_deleted'}
        if status_number in status:
            self.status_name = status[status_number]
        else:
            self.status_name = 'unknown'
            

    def __getattr__(self, name):
        if name == 'user':
            return self._get_user_(self.user_id)
        else:
            raise AttributeError
        
    @magic_cache
    def _get_user_(self, user_id):
        return user.User(self.user_id)

    def __dir__(self):
        results = ['aperture',
                   'camera',
                   'category',
                   'category_name',
                   'clear_cache',
                   'comments_count',
                   'created_at',
                   'description',
                   'empty_cache',
                   'favorites_count',
                   'five_hundred_px',
                   'focal_length',
                   'for_sale',
                   'for_sale_date',
                   'height',
                   'hi_res_uploaded',
                   'highest_rating',
                   'highest_rating_date',
                   'id',
                   'image_url',
                   'images',
                   'iso',
                   'latitude',
                   'lens',
                   'location',
                   'longitude',
                   'name',
                   'nsfw',
                   'privacy',
                   'rating',
                   'sales_count',
                   'shutter_speed',
                   'status',
                   'status_name',
                   'store_download',
                   'store_print',
                   'taken_at',
                   'times_viewed',
                   'user_id',
                   'user',
                   'votes_count',
                   'width']
        return results
