#!/usr/bin/env python
# encoding: utf-8
"""
Created by @arthurnn on 2012-01-19.
"""

import urllib
from StringIO import StringIO
try:
    from five_hundred_px import *
except ImportError:
    from src.five_hundred_px import *
    from helpers.authentication import get_consumer_key

CONSUMER_KEY = get_consumer_key()

def main():
    api = FiveHundredPx(CONSUMER_KEY)

    kwargs = dict(term='sao paulo',
                  rpp=10,
                  image_size=[3,4])

    photos = api.search_photos(**kwargs)['photos']
    for p in photos:
        thumbnail_url = p['image_url']
        fhpx_url = 'http://500px.com/photo/%d' % p['id']
        
        try:
            print '(%s,%s,%s)' % (thumbnail_url[0],thumbnail_url[1],fhpx_url)
        except Exception, e:
              print 'Error in the following url[%s]:%s' % (fhpx_url,e)
              continue


if __name__ == '__main__':
	main()
