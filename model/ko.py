from marshmallow import Schema, fields

class Ko(object):
    def __init__(self, id, kakutro, kofal, uuid):
        self.id = id
        self.kakutro = kakutro
        self.kofal = kofal
        self.uuid = uuid

    def __repr__(self):
        return '<Ko(name={self.id!r})>'.format(self=self)
    
class KoSchema(Schema):
    id = fields.Str(dump_only=True)
    kakutro = fields.List(fields.Str(required=True))
    kofal = fields.Str(required=True)
    uuid = fields.Str(dump_only=True)
   