import datetime
import flask
import functools
import json
import bson


convert = {
    datetime.datetime: lambda x: x.isoformat(),
    bson.ObjectId: str,
}
def _dthandler(obj):
    for type_, converstion in convert.iteritems():
        if isinstance(obj, type_):
            return converstion(obj)


def to_json(fnc):
    @functools.wraps(fnc)
    def wrapper(*args, **kwargs):
        return flask.Response(
            json.dumps(fnc(*args, **kwargs), default=_dthandler),
            status=200,
            mimetype='application/json'
        )
    return wrapper


import pymongo
import os


_client = pymongo.MongoClient(os.environ["MONGO_URL"] or None)
_db = _client[os.environ["MONGO_DB_NAME"]]

def get_database():
    return _db
