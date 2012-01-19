#!/usr/bin/env python
# encoding: utf-8
"""
Created by @arthurnn on 2012-01-19.
"""

import sys
import os
import urllib
from StringIO import StringIO
from fivehundred import *

CONSUMER_KEY = '__your_consumer_key__'
def main():
    api = FiveHundredPx(CONSUMER_KEY)
    generator = api.get_photos(feature='popular',limit=50)
    for p in generator:
        thumbnail_url = p['image_url']
        fhpx_url = 'http://500px.com/photo/%d' % p['id']
        
        try:
            fileio = urllib.urlopen(thumbnail_url)
            im = StringIO(fileio.read())
            # if you have PIL you can play with the image
            #img = Image.open(im)
            print '(%s,%s)' % (thumbnail_url,fhpx_url)
        except Exception, e:
		    print 'Error in the following url[%s]:%s' % (thumbnail_url,e)
		    continue


if __name__ == '__main__':
	main()

