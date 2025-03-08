from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from suha import Kotoli  
from mellan import format_fras  

import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1 import aggregation
from google.cloud.firestore_v1.base_query import FieldFilter
import os

from model.ko import Ko, KoSchema


simper_svar_laksu = 10

cred = credentials.Certificate("./serviceAccountKey.json") #Update with your path.
try:
    firebase_admin.initialize_app(cred)
    db = firestore.client()  #Get a Firestore client
    print(" 🔥 Firebase initialized successfully")
except Exception as e:
    print(f"Error initializing Firebase: {e}")



app = Flask(__name__)
api = Api(app)
kotoli = Kotoli()

class Ko(Resource):
    def get(self):
        
        docs = db.collection('ko').get()
        
        svar = []
        laksu:int = int(request.args.get('laksu') or simper_svar_laksu)
        laksu = min(laksu, len(docs))
        for i in range(0,laksu):
            svar.append(docs[i].to_dict())
            svar[i]["id"] = docs[i].id
        return jsonify(svar)

    def post(self):
        collection_ref = db.collection("ko")
        # Load and vallidate request payload
        try:
            ko = KoSchema().load(request.get_json())
        except Exception as e:
            return jsonify({'error': str(e)}
            )
        # Determine id from namai sequence number
        ko["namai"] = ko["kakutro"][0]
        query = collection_ref.where(filter=FieldFilter("namai", "==", ko["namai"])).count(alias="all")        
        for result in query.get():
            id = ko["namai"] + "-" + str(result[0].value + 1)
        # Write ko to firestore
        try:
            collection_ref.document(id).set(ko)
        except Exception as e:
            return jsonify({'error': str(e)})
        ko["id"] = id
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
