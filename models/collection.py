from src import fivehundred
from helpers import authentication

import models.photo

from magic.magic_cache import magic_cache, magic_fn_cache
from magic.magic_object import magic_object

@magic_fn_cache
def Collection(id, *args, **kwargs):
    return collection(id, *args, **kwargs)

class collection(magic_object):
    five_hundred_px = fivehundred.FiveHundredPx(authentication.get_consumer_key(),
                                                authentication.get_consumer_secret())

    def __init__(self, id, data=None, authorized_client=None):
        self.id = id
        self.authorized_client = authorized_client
        data = data or self.get_long_public_collection_data(id)
        self.add_colleciton_data(data)

    def add_colleciton_data(self, collection_data):
        self.photos = {}
        for photo in collection_data['photos']:
            photo_id = photo['id']
            self.photos[photo_id] = models.photo.Photo(photo_id, data={"photo": photo})
        del(collection_data['photos'])
        for key in collection_data:
            setattr(self, key, collection_data[key])
    
    def get_long_public_collection_data(self, id):
        return collection.five_hundred_px.get_collection(id, self.authorized_client)
