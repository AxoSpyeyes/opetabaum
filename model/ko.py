from marshmallow import Schema, fields

class Ko(object):
    def __init__(self, id, kakutro, kofal):
        self.id = id
        self.kakutro = kakutro
        self.kofal = kofal

    def __repr__(self):
        return '<Ko(name={self.id!r})>'.format(self=self)
    
class KoSchema(Schema):
    id = fields.Str(dump_only=True)
    kakutro = fields.List(fields.Str(required=True))
    kofal = fields.Str(required=True)   