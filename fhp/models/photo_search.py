from functools import partial

from fhp.api import five_hundred_px
from fhp.helpers import authentication

import fhp.models.photo

from fhp.magic.magic_cache import magic_cache, magic_fn_cache
from fhp.magic.magic_generator import MagicGenerator

five_hundred_px = five_hundred_px.FiveHundredPx(authentication.get_consumer_key(),
                                            authentication.get_consumer_secret())
@magic_fn_cache
def PhotoSearch(term=None, tag=None, tags=None):
    if not bool(term) != bool(tag):
        error = "PhotoSearch requires exactly on of term and tag"
        error += "\n perhaps you meant to use a keyword argument"
        raise TypeError, error
    iter_source = partial(five_hundred_px.photo_search, term=term, tag=tag, tags=tags)
    def build_photo(photo_data):
        photo_id = photo_data["id"]
        data = dict(photo=photo_data)
        return fhp.models.photo.Photo(photo_id, data=data)
    iter_destination = build_photo
    return photo_search(iter_source=iter_source,
                        iter_destination=iter_destination)

class photo_search(MagicGenerator):
    pass
