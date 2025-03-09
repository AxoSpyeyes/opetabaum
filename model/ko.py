import json
from marshmallow import Schema, fields, post_load

class Ko(object):
    def __init__(self, id, namai, kakutro, kofal):
        self.id = id
        self.namai = namai
        self.kakutro = kakutro
        self.kofal = kofal

    def __repr__(self):
        return '<Ko(name={self.id!r})>'.format(self=self)
    
class KoSchema(Schema):
    id = fields.Str(load_default=None)
    namai = fields.Str(required=True)
    kakutro = fields.List(fields.Str(required=True))
    kofal = fields.Str(required=True)
    collection = fields.Str(load_default="ko")
