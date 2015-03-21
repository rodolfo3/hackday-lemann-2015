import datetime
import flask
import functools
import json


def _dthandler(obj):
    return obj.isoformat() if isinstance(obj, datetime.datetime) else None


def to_json(fnc):
    @functools.wraps(fnc)
    def wrapper(*args, **kwargs):
        return flask.Response(
            json.dumps(fnc(*args, **kwargs), default=_dthandler),
            status=200,
            mimetype='application/json'
        )
    return wrapper
