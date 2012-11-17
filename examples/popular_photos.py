import fhp.api.five_hundred_px as f
import fhp.helpers.authentication as authentication
from pprint import pprint
key = authentication.get_consumer_key()
secret = authentication.get_consumer_secret()

client = f.FiveHundredPx(key, secret)
results = client.get_photos(feature='popular')

i = 0
PHOTOS_NEEDED = 2
for photo in results:
    pprint(photo)
    i += 1
    if i == PHOTOS_NEEDED:
        break
