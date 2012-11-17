import fhp.api.five_hundred_px as fh
import fhp.helpers.authentication as a

f = fh.FiveHundredPx(a.get_consumer_key(),
                     a.get_consumer_secret(),
                     a.get_verify_url())


for result in f.photo_search(tag="freckles", sort="rating"):
    print result
    break



