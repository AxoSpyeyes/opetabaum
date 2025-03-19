from suha import Kotoli  
from mellan import format_fras  

from firestore_db import Database
db = Database()

kotoli = Kotoli()

def delete_ko():
    docs = db.collection('ko').get()
    for ko in docs:
        try:
            ko.reference.delete()
            print(f'"{ko.to_dict()["kakutro"][0]}" dan sjkekso ko-kaban kara.')
        except Exception as e:
            print(str(e))

def delete_ttb():
    docs = db.collection('ttb').get()
    for ttb in docs:
        try:
            ttb.reference.delete()
            print(f'"{format_fras(ttb.to_dict())}" dan sjkekso ttb-kaban kara.')
        except Exception as e:
            print(str(e))

def delete_brukdjin():
    docs = db.collection('brukdjin').get()
    for brukdjin in docs:
        try:
            brukdjin.reference.delete()
            print(f'"{brukdjin.to_dict()["namai"]}" dan sjkekso brukdjin-kaban kara.')
        except Exception as e:
            print(str(e))


def add_ko():
    for id, ko in kotoli.tumam["ko"].items():
        try:
            db.collection('ko').document(id).set(ko)
            print(f'"{ko["kakutro"][0]}" dan tullajena ko-kaban made!')
        except Exception as e:
            print(str(e))

def add_ttb():
    for ttb in kotoli.tumam["ttb"].values():
        try:
            db.collection('ttb').add(ttb)
            print(f'"{format_fras(ttb)}" dan tullajena ttb-kaban made!')
        except Exception as e:
            print(str(e))

def add_brukdjin():
    for brukdjin in kotoli.tumam["brukdjin"].values():
        try:
            db.collection('brukdjin').add(brukdjin)
            print(f'"{brukdjin["namai"]}" dan tullajena brudjin-kaban made!')
        except Exception as e:
            print(str(e))


def reset_ko():
    print(db.delete_all_docs("ko"))
    print (db.batch_insert_docs("ko", kotoli.tumam["ko"]))

def reset_ttb():
    print(db.delete_all_docs("ttb"))
    print (db.batch_insert_docs("ttb", kotoli.tumam["ttb"]))

def reset_brukdjin():
    print(db.delete_all_docs("brukdjin"))
    print (db.batch_insert_docs("brukdjin", kotoli.tumam["brukdjin"]))

def reset_everything():
    reset_ko()
    reset_ttb()
    reset_brukdjin()

reset_everything()