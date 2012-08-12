#!/usr/bin/env python
# encoding: utf-8
"""
Created by @arthurnn
"""

import sys
import os
import urllib
from StringIO import StringIO
try:
    from fivehundred import *
except ImportError:
    from src.fivehundred import *
    from helpers.json_finder import _parse_json


# More info at developer.500px.com. If you are logged in
# go to: http://500px.com/settings/applications 
def get_consumer_key():
    with open(os.path.join('config','authentication.json')) as f:
        auth = _parse_json(f.read())
        return auth["authentication"]["consumer_key"]

CONSUMER_KEY = get_consumer_key()


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
