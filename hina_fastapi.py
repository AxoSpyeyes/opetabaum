# Install FastAPI: pip install "fastapi[standard]"
# Run script: fastapi dev hina_fastapi.py

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from firestore_db import Database

from model_fastapi.ko import Ko

app = FastAPI()
db = Database()

@app.get("/")
def root():
    return {"message": "Hellow World"}

@app.get("/ko")
def get_kos(skip: int = 0, limit: int = 10):
    params = {"skip": skip, "limit": limit}
    try: 
        response = db.get_docs("ko", params)
        return response
    except Exception as e:
        return {'error': str(e)}

@app.post("/ko")
def new_ko(ko: Ko):
    try:
        ko = db.insert_doc(jsonable_encoder(ko))
        return ko
    except Exception as e:
        return {'error': str(e)}
    