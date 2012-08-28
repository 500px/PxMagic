from helpers.json_finder import _parse_json
import os

def get_consumer_key():
    """For more info on the API visit developer.500px.com.
    If you are logged in to your 500px account you can 
    go to: http://500px.com/settings/applications to retrieve
    your key.
    """
    with open(os.path.join('config','authentication.json')) as f:
        auth = _parse_json(f.read())
        return auth["authentication"]["consumer_key"]

def get_consumer_secret():
    """For more info on the API visit developer.500px.com.
    If you are logged in to your 500px account you can 
    go to: http://500px.com/settings/applications to retrieve
    your key.
    """
    with open(os.path.join('config','authentication.json')) as f:
        auth = _parse_json(f.read())
        return auth["authentication"]["consumer_secret"]
