try:
    import json
    _parse_json = lambda s: json.loads(s)
    _dump_json = lambda s: json.dumps(s)
except ImportError:
    try:
        import simplejson
        _parse_json = lambda s: simplejson.loads(s)
        _dump_json = lambda s: simplejson.dumps(s)
    except ImportError:
        # For Google AppEngine
        from django.utils import simplejson
        _parse_json = lambda s: simplejson.loads(s)
        _dump_json = lambda s: simplejson.dumps(s)
