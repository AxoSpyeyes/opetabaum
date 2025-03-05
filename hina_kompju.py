from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from suha import Kotoli  


app = Flask(__name__)
api = Api(app)
kotoli = Kotoli()


class Al(Resource):
    def get(self):
        return jsonify(kotoli.kirain_kaban)
    
class Ko(Resource):
    def get(self):
        kakutro:str = request.args.get('kakutro') or ""
        kofal:str = request.args.get('kofal') or ""

        if (kakutro or kofal):
            return jsonify(kotoli.suha_ko(kakutro, kofal))
        return jsonify(kotoli.kirain_kaban["ko"])
    
class Ko_uuid(Resource):
    def get(self, uuid):
        return jsonify(kotoli.kirain_kaban["ko"][uuid])

class Ttb(Resource):
    def get(self):
        kakutro:str = request.args.get('kakutro') or ""
        kofal:str = request.args.get('kofal') or ""
        ko_uuid:str = request.args.get('ko-uuid') or ""

        if ko_uuid:
            return jsonify(kotoli.suha_ttb_uuid(ko_uuid))
        if (kakutro or kofal):
            return jsonify(kotoli.suha_ttb(kakutro,kofal))
        return jsonify(kotoli.kirain_kaban["ttb"])
    
class Ttb_uuid(Resource):
    def get(self, uuid):
        return jsonify(kotoli.kirain_kaban["ttb"][uuid])


class Brukdjin(Resource):
    def get(self):
        namai:str = request.args.get('namai') or ""
        ko:str = request.args.get('kakutro') or ""
        ko_uuid:str = request.args.get('ko-uuid') or ""

        if namai:
            return jsonify(kotoli.suha_brukdjin(namai))
        if ko_uuid:
            return jsonify(kotoli.suha_brukdjin_ko_uuid(ko_uuid))
        if ko:
            return jsonify(kotoli.suha_brukdjin_ko(ko))
        return jsonify(kotoli.kirain_kaban["brukdjin"])
    
class Brukdjin_uuid(Resource):
    def get(self, uuid):
        return jsonify(kotoli.kirain_kaban["brukdjin"][uuid])


api.add_resource(Al, "/")
api.add_resource(Ko, "/ko")
api.add_resource(Ko_uuid, "/ko/<uuid>")
api.add_resource(Ttb, "/ttb")
api.add_resource(Ttb_uuid, "/ttb/<uuid>")
api.add_resource(Brukdjin, "/brukdjin")
api.add_resource(Brukdjin_uuid, "/brukdjin/<uuid>")


if __name__ == '__main__':
    app.run(debug=True)
