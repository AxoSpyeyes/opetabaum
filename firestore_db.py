import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1 import aggregation
from google.cloud.firestore_v1.base_query import FieldFilter

class Database(object):

    def __init__(self):
        # Initialize Firestore
        cred = credentials.Certificate("./serviceAccountKey.json")
        try:
            firebase_admin.initialize_app(cred)
            db = firestore.client()  #Get a Firestore client
            print(" 🔥 Firebase initialized successfully")
        except Exception as e:
            print(f"Error initializing Firebase: {e}")
        self.db = db

    def delete_all_docs(self, collection):
        # Delete all documents in a collection
        docs = self.db.collection(collection).get()
        i = 0
        for doc in docs:
            try:
                doc.reference.delete()
                i += 1
            except Exception as e:
                print(str(e))
        return (f'Delete all docs ({collection}): {i} records deleted') 

    def batch_insert_docs(self, collection, payload):
        # Insert a batch of documents from a json object
        i = 0
        for id, value in payload.items():
            try:
                self.db.collection(collection).document(id).set(value)
                i += 1
            except Exception as e:
                print(str(e))
        return (f'Batch insert docs ({collection}): {i} records inserted')