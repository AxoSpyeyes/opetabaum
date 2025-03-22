# Install FastAPI: pip install "fastapi[standard]"
# Run script: fastapi dev hina_fastapi.py

from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from firestore_db import Database

from model_fastapi.ko import Ko
from model_fastapi.ttb import Ttb
from model_fastapi.brukdjin import Brukdjin

app = FastAPI()
db = Database()

@app.get("/")
def root():
    return {"message": "Hellow World"}

# Ko methods

@app.get("/ko")
def get_kos(skip: int = 0, limit: int = 10):
    params = {"skip": skip, "limit": limit}
    try: 
        kos = db.get_docs("ko", params)
        return kos
    except Exception as e:
        return {'error': str(e)}

@app.post("/ko")
def new_ko(ko: Ko):
    try:
        ko = db.insert_doc(jsonable_encoder(ko))
        return ko
    except Exception as e:
        return {'error': str(e)}

@app.get("/ko/{ko_id}")
def get_ko(ko_id: str):
    try: 
        ko = db.get_doc_by_id("ko", ko_id)
    except Exception as e:
        return {'error': str(e)}
    if ko: 
        return ko
    else:
        raise HTTPException(status_code=404, detail="Ko not found")

# Ttb methods

@app.get("/ttb")
def get_ttbs(skip: int = 0, limit: int = 10):
    params = {"skip": skip, "limit": limit}
    try: 
        ttbs = db.get_docs("ttb", params)
        return ttbs
    except Exception as e:
        return {'error': str(e)}
    
@app.get("/ttb/{ttb_id}")
def get_ttb(ttb_id: str):
    try: 
        ko = db.get_doc_by_id("ttb", ttb_id)
    except Exception as e:
        return {'error': str(e)}
    if ko: 
        return ko
    else:
        raise HTTPException(status_code=404, detail="Ttb not found")

@app.post("/ttb")
def new_ttb(ttb: Ttb):
    try:
        ttb = db.insert_doc(jsonable_encoder(ttb))
        return ttb
    except Exception as e:
        return {'error': str(e)}
    
# Brukdjin methods

@app.get("/brukdjin")
def get_brukdjin(skip: int = 0, limit: int = 10):
    params = {"skip": skip, "limit": limit}
    try: 
        brukdjins = db.get_docs("brukdjin", params)
        return brukdjins
    except Exception as e:
        return {'error': str(e)}
    
@app.get("/brukdjin/{brukdjin_id}")
def get_brukdjin(brukdjin_id: str):
    try: 
        brukdjin = db.get_doc_by_id("brukdjin", brukdjin_id)
    except Exception as e:
        return {'error': str(e)}
    if brukdjin: 
        return brukdjin
    else:
        raise HTTPException(status_code=404, detail="Brukdjin not found")
    
@app.post("/brukdjin")
def new_brukdjin(brukdjin: Brukdjin):
    try:
        brukdjin = db.insert_doc(jsonable_encoder(brukdjin))
        return brukdjin
    except Exception as e:
        return {'error': str(e)}