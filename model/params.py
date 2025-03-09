import json
from marshmallow import Schema, fields, post_load

class Params(object):
    def __init__(self, limit):
        self.limit = limit

    def __repr__(self):
        return '<Params(name={self.id!r})>'.format(self=self)
    
class ParamsSchema(Schema):
    limit = fields.Int()
