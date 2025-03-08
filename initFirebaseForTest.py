from suha import Kotoli  
from mellan import format_fras  

from firestore_db import Database
db2 = Database()
db = db2.db # hack to not break old code

kotoli = Kotoli()

def reset_ko():
    print(db2.delete_all_docs("ko"))
    print (db2.batch_insert_docs("ko", kotoli.kirain_kaban["ko"]))

def reset_ttb():
    print(db2.delete_all_docs("ttb"))
    print (db2.batch_insert_docs("ttb", kotoli.kirain_kaban["ttb"]))

def reset_brukdjin():
    print(db2.delete_all_docs("brukdjin"))
    print (db2.batch_insert_docs("brukdjin", kotoli.kirain_kaban["brukdjin"]))

def reset_everything():
    reset_ko()
    reset_ttb()
    reset_brukdjin()

reset_everything()