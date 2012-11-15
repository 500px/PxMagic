try:
    import authentication
except ImportError:
    import sys
    warn_user = """No authentication set


*** You must set your authentication in fhp.helpers.authentication in order
 to use PxMagic. Edit the example file and save as authentication.py ***

"""
    sys.exit(warn_user)
import http
import json_finder
