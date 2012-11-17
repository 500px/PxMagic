500px Python Magical API Client
===============================

This is the magical API client!

Soon :sunrise: and :bridge_at_night: will be on your monitor!

So some quick things you NEED to know before you get started:

1. You can either use the magical caching way of using the app
   with things like :
   ``` zach = User(username='zachaysan')```
   ``` zach.friends.first().username ```
   
   Or you can go the more traditional route
   ( see examples/popular_photos.py )

2. There are caches and generators everywhere. I haven't gotten 
   around to making sure that the caches get cleared automatically.

3. Usually generators will continue to yeild, regardless of the 
   how many results come in a single page from the api. It will just
   keep paging until it runs out of results.

4. There is a really hairy issue with Users due to me being 
   dumb. Basically I should have broken up Users into
   AuthorizedUser and User, where the AuthorizedUser has successfully
   authenticated with the app.

5. This library was written with two styles of apps in mind. First:
   a traditionally client app library (for example, using this to 
   write an Ubuntu app), Second: a web server.
   
   If you are going to be using OAuth and you are attending Pixel 
   Hack Day come find me. I'm by the window in the secondary room.

6. Before you do anything you need to create helpers/authentication.py
   and provided 3 functions: get_consumer_key(), get_consumer_secret(),
   and get_verify_url(). You can see an example of how this looks at 
   ``` helpers/authentication.example.py ```
   
To run test suite
-----------------
1. Ignore tests/settings.py since most of the OAuth tests assume that
   you have access to the zachaysan account.
2. ```python -m discover ```
