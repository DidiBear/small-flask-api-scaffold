import collections
import json
from flask_admin.contrib.sqla import ModelView

from flask import jsonify

# Common JSON responses (following JSend spec)

def success(data = None):
    return jsonify({ "status" : "success", "data" : data_as_dict(data)})

def error(message = "", code = None, data = None):
    response = { "status" : "error", "message" : message}

    if code: response["code"] = code
    if data: response["data"] = data_as_dict(data)

    return jsonify(response)

def fail(data = None):
    return jsonify({ "status" : "fail", "data" : data_as_dict(data)})

def data_as_dict(data):
    if isinstance(data, Jsonable):
        return data.as_dict()

    if isinstance(data, (list, tuple)):
        return [data_as_dict(element) for element in data]
    
    return data

class Jsonable:
    """ 
    Add JSON feature to a db.Model class
    
    Require to be a db.Model (have the variable __table__)
    """

    def as_dict(self):
        return dict((column.name, getattr(self, column.name)) for column in self.__table__.columns if getattr(self, column.name) is not None)

    def to_json(self, pretty=False):
        if pretty: 
            return json.dumps(self.as_dict(), sort_keys=True, indent=4, separators=(',', ': '))
        return json.dumps(self.as_dict())


    @classmethod
    def from_dict(cls, dictionary):
        return cls(**dictionary)

    @classmethod
    def from_json(cls, json_string):
        return cls.from_dict(json.loads(json_string))
