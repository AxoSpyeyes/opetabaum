from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from suha import Kotoli  
from mellan import format_fras  

import os

from model.ko import Ko, KoSchema
from model.params import Params, ParamsSchema


simper_svar_laksu = 10

from firestore_db import Database
db2 = Database()
db = db2.db # hack to not break old code



app = Flask(__name__)
api = Api(app)
kotoli = Kotoli()

class Ko(Resource):

    def get(self):
        # Load and vallidate request payload
        try:
            params = ParamsSchema().load(request.args.to_dict())
        except Exception as e:
            return jsonify({'error': str(e)})
        
        try: 
            response = db2.get_docs("ko", params)
            return jsonify(response)
        except Exception as e:
            return jsonify({'error': str(e)})       

    def post(self):
        # Load and vallidate request payload
        try:
            ko = KoSchema().load(request.get_json())
        except Exception as e:
            return jsonify({'error': str(e)})
        
        # Determine id from namai sequence number
        namaicount = db2.count_value("ko", "namai", ko["namai"])
        ko["id"] = ko["namai"] + "-" + str((namaicount + 1))
        # Write ko to firestore
        ko = db2.insert_doc(ko)
        return jsonify(ko)

class Ko_id(Resource):
    def get(self, id):
        try:
            doc_ref = db.collection('ko').document(id)
            doc = doc_ref.get()
            if doc.exists:
                return jsonify(doc.to_dict())
            else:
                return jsonify({'message': 'Document not found'})
        except Exception as e:
            return jsonify({'error': str(e)})

class Ttb(Resource):
    def get(self):
        
        docs = db.collection('ttb').get()
        svar = []
        laksu:int = int(request.args.get('laksu') or simper_svar_laksu)
        laksu = min(laksu, len(docs))
        for i in range(0,laksu):
            svar.append(docs[i].to_dict())
            svar[i]["id"] = docs[i].id
        return jsonify(svar)

    def post(self):
        try:
            data = request.get_json()  # Get data from the request
            db.collection('ttb').add(data)
            return jsonify({'message': 'Data added successfully'})
            
        except Exception as e:
            return jsonify({'error': str(e)})

class Ttb_id(Resource): # right now when recieving a reference, it breaks
    def get(self, id):
        try:
            doc_ref = db.collection('ttb').document(id)
            doc = doc_ref.get()
            if doc.exists:
                return jsonify(doc.to_dict())
            else:
                return jsonify({'message': 'Document not found'})
        except Exception as e:
            return jsonify({'error': str(e)})

class Brukdjin(Resource): # this is just copied from ko right now, but needs to be specialized for brukdjin
    def get(self):
        
        docs = db.collection('brukdjin').get()
        
        svar = []
        laksu:int = int(request.args.get('laksu') or simper_svar_laksu)
        laksu = min(laksu, len(docs))
        for i in range(0,laksu):
            svar.append(docs[i].to_dict())
            svar[i]["id"] = docs[i].id

        return jsonify(svar)

    def post(self):
        try:
            data = request.get_json()  # Get data from the request
            db.collection('brukdjin').add(data)
            return jsonify({'message': 'Data added successfully'})
        except Exception as e:
            return jsonify({'error': str(e)})

class Brukdjin_id(Resource):
    def get(self, id):
        try:
            doc_ref = db.collection('brukdjin').document(id)
            doc = doc_ref.get()
            if doc.exists:
                return jsonify(doc.to_dict())
            else:
                return jsonify({'message': 'Document not found'})
        except Exception as e:
            return jsonify({'error': str(e)})


api.add_resource(Ko, "/ko")
api.add_resource(Ko_id, "/ko/<id>")
api.add_resource(Ttb, "/ttb")
api.add_resource(Ttb_id, "/ttb/<id>")
api.add_resource(Brukdjin, "/brukdjin")
api.add_resource(Brukdjin_id, "/brukdjin/<id>")



if __name__ == '__main__':
    app.run(debug=True)
