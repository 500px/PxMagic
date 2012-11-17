#!/usr/bin/env python
# encoding: utf-8
"""
Created by @arthurnn
"""

import urllib
from StringIO import StringIO
try:
    from fhp import helpers
    get_consumer_key = helpers.authentication.get_consumer_key 
    get_consumer_secret = helpers.authentication.get_consumer_secret
    from fhp import api
    FiveHundredPx = src.five_hundred_px.FiveHundredPx
except ImportError:
    from fhp.api.five_hundred_px import *
    from fhp.helpers.authentication import get_consumer_key,get_consumer_secret

pil_exists = None

try:
    from PIL import Image
    pil_exists = True
except ImportError:
    print "no PIL found... try 'pip install PIL' "

CONSUMER_KEY = get_consumer_key()
CONSUMER_SECRET = get_consumer_secret()

def main():
    api = FiveHundredPx(CONSUMER_KEY, CONSUMER_SECRET)
    generator = api.get_photos(feature='popular',limit=3)
    for p in generator:
        thumbnail_url = p['image_url']
        fhpx_url = 'http://500px.com/photo/%d' % p['id']
        fileio = urllib.urlopen(thumbnail_url)
        im = StringIO(fileio.read())
        # if you have PIL you can play with the image
        if pil_exists:
            img = Image.open(im)
            img.show()
        try:
            print '(%s,%s)' % (thumbnail_url,fhpx_url)
        except Exception, e:
            print 'Error in the following url[%s]:%s' % (thumbnail_url,e)
            continue

if __name__ == '__main__':
    main()
