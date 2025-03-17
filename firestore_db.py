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
        self.default_limit = 10

    def get_docs(self, collection, params = {}):
        docs = self.db.collection(collection).get()
        limit = int(params["limit"] or self.default_limit)
        limit = min(limit, len(docs))
        response = []
        for i in range(0,limit):
            response.append(docs[i].to_dict())
            response[i]["id"] = docs[i].id
        return response

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

    def batch_insert_docs(self, collection, docs):
        # Insert a batch of documents from a json object
        i = 0
        for id, value in docs.items():
            try:
                self.db.collection(collection).document(id).set(value)
                i += 1
            except Exception as e:
                print(str(e))
        return (f'Batch insert docs ({collection}): {i} records inserted')
    
    def insert_doc(self, doc):
        # Insert a doc to the database
        if doc["id"] is not None: # Insert object if an id is present 
            doc = self.set_doc(doc)
            return doc
        else: # Otherwise add
            doc = self.add_doc(doc)
            return doc
    
    def add_doc (self, doc):
        try:
            update_time, doc_ref = self.db.collection(doc["collection"]).add(doc)
            doc["id"] = doc_ref.id
            return doc
        except Exception as e:
            print(str(e))

    
    def set_doc (self, doc):
        try:
            self.db.collection(doc["collection"]).document(doc["id"]).set(doc)
        except Exception as e:
            print(str(e))
        return doc
    
    def count_value (self, collection, field, value):
        # To-do: Check if field is a an array and in that case do an array search
        try:
            query = self.db.collection(collection).where(filter=FieldFilter(field, "==", value))
            aggregate_query = aggregation.AggregationQuery(query)
            aggregate_query.count(alias="all")
            results = aggregate_query.get()        
            for result in results:
                count = int(result[0].value)
            # print(count)
            return count
        except Exception as e:
            print(str(e))
        