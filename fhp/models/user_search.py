from functools import partial

from fhp.api import five_hundred_px
from fhp.helpers import authentication

import fhp.models.user

from fhp.magic.magic_cache import magic_fn_cache
from fhp.magic.magic_generator import MagicGenerator

five_hundred_px = five_hundred_px.FiveHundredPx(authentication.get_consumer_key(),
                                            authentication.get_consumer_secret())
@magic_fn_cache
def UserSearch(term):
    iter_source = partial(five_hundred_px.user_search, term=term)
    def build_user(user_data):
        user_id = user_data["id"]
        data = dict(user=user_data)
        return fhp.models.user.User(user_id, data=data)
    iter_destination = build_user
    return user_search(iter_source=iter_source,
                       iter_destination=iter_destination)

class user_search(MagicGenerator):
    pass
