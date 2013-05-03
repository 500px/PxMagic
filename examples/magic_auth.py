from fhp.models.user import User

from pprint import pprint

def narrate(text):
    if narrate.on:
        print "Narrator:", text

narrate.on = True

USERNAME = 'zachaysan'

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
    narrate("We start by taking a user_id")
    
    

    username = USERNAME
    if not username:
        print "we need you to edit this file first!"
        print "filename:", __name__
        exit(0)
    user_id = int(User(username=username).id)
    narrate("We then make the authorized user object")
    user = User(user_id, authorize=True)
    narrate("Looks like that went smoothly")
    for photo in user.photos:
        print "photo:", photo.name, photo.id
    narrate("look at that!")
    """
    except Exception, e:
        narrate("Looks like a problem happened, are your auth creds set up?")
        raise e
    """
    
if __name__ == '__main__':
    main(True)
