from fhp.models.photo import Photo

from pprint import pprint

def narrate(text):
    if narrate.on:
        print "Narrator:", text

narrate.on = True

def main(narrations_on=True):
    """Fancy automagical api requests when needed 
    are completed by using the built in fhp.models.
   
    These fhp.models.do several things for you, like:
    1. Caching responses for you, so you don't need
       to waste time doing that yourself.
    2. Lazily doing requests so that the experience 
       feels faster
    
    We start by making a photo:
    """
    narrate.on = narrations_on
    narrate("We start by pulling down the photo")
    try:
        owly_photo = Photo(3256058)
        narrate("Looks like that went smoothly")
    except:
        narrate("Looks like a problem happened, are your auth creds set up?")

    narrate("Now, lets check out that photo photo url:")
    print owly_photo.image_url
    
    narrate("Here is a look at the full object:")
    pprint(owly_photo.__dict__)
    
    narrate("We don't *see* the user, but we know it is there")
    print 'user' in dir(owly_photo)
    
    narrate("So let's try to grab that user")
    print owly_photo.user
    
    narrate("Cool ain't it? Wondering who took this fine photo?")
    print owly_photo.user.username
    
if __name__ == '__main__':
    main(True)
