import json
import uuid

class Kotoli :
    def __init__(self):
        self.read_data()

    def read_data(self):
        with open('data.json', 'r') as f:
            self.kirain_kaban = json.load(f)

    def update_data(self):
        with open('data.json','w') as f:
            json.dump(self.kirain_kaban, f)

    def hosoimah(self,kaban):
        return [ting for unakaban in kaban for ting in unakaban]

    def sada_ko(self, ko_uuid):
        self.read_data()
        return self.kirain_kaban["ko"][ko_uuid]

    def sada_ttb(self, ttb_uuid):
        self.read_data()
        return self.kirain_kaban["ttb"][ttb_uuid]

    def sada_brukdjin(self, brukdjin_uuid):
        self.read_data()
        return self.kirain_kaban["brukdjin"][brukdjin_uuid]

    def sada_konen(self, ttb_uuid):
        self.read_data()
        svar = []
        for ko in self.sada_ttb(ttb_uuid)["zunaga"]:
            konen = []
            for konen_uuid in ko:
                konen.append(self.sada_ko(konen_uuid))
            svar.append(konen)
        return svar

    def suha_ko(self, suhajena_ko = "", kofal = ""):
        self.read_data()
        svar = []
        for ko in self.kirain_kaban["ko"].values():
            if ((suhajena_ko in ko["kakutro"] or suhajena_ko == "") and (kofal == ko["kofal"] or kofal == "")):
                svar.append(ko)
        return svar

    def suha_ttb_uuid(self, ko_uuid):
        self.read_data()
        svar = []
        for ttb in self.kirain_kaban["ttb"].values():
            for ko in ttb["zunaga"]:
                if ko_uuid in ko["konen"]:
                    svar.append(ttb)
        return svar

    def suha_ttb(self, suhajena_ko, kofal = ""):
        self.read_data()
        svar = []
        for ko in self.suha_ko(suhajena_ko, kofal=kofal):
            for ttb in self.suha_ttb_uuid(ko["uuid"]):
                ttb["suhajena_ko"] = ko["uuid"]
                svar.append(ttb)
        return svar

    def suha_brukdjin(self, namai):
        self.read_data()
        for brukdjin in self.kirain_kaban["brukdjin"].values():
            if brukdjin["namai"] == namai:
                return brukdjin

    def suha_brukdjin_ko(self,ko):
        svar = []
        for ko in self.suha_ko(ko):
            for brukdjin in self.suha_brukdjin_ko_uuid(ko["uuid"]):
                brukdjin["suhajena_ko"] = ko["uuid"]
                svar.append(brukdjin)
        return svar
    
    def suha_brukdjin_ko_uuid(self, ko_uuid):
        svar = []
        for brukdjin in self.kirain_kaban["brukdjin"].values():
            print
            if ko_uuid in brukdjin["sjirujena_ko"]:
                svar.append(brukdjin)
        return svar

    def sada_fsjtozma(self, brukdjin_uuid, ko_uuid):
        self.read_data()
        return ko_uuid in self.kirain_kaban["brukdjin"][brukdjin_uuid]["sjirujena_ko"]

    def maha_fsjto(self, brukdjin_uuid, ko_uuid, fsjto = True):
        self.read_data()
        # lera
        if self.sada_fsjtozma(brukdjin_uuid,ko_uuid) and not fsjto:
            self.kirain_kaban["brukdjin"][brukdjin_uuid]["sjirujena_ko"].remove(ko_uuid)
        # vasu
        elif not self.sada_fsjtozma(brukdjin_uuid,ko_uuid) and fsjto:
            self.kirain_kaban["brukdjin"][brukdjin_uuid]["sjirujena_ko"].append(ko_uuid)
        self.update_data()


    def maha_ko(self, kakutro, kofal):
        self.read_data()
        UUID = str(uuid.uuid4())
        self.kirain_kaban["ko"][UUID] = {"uuid":UUID, "kakutro":kakutro, "kofal":kofal}
        self.update_data()

    # TODO v
    def maha_ttb(self, fras, zunaga):
        self.read_data()
        UUID = str(uuid.uuid4())
        ko_uuid = list(set(self.hosoimah(zunaga)))
        self.kirain_kaban["ttb"][UUID] = {"uuid":UUID, 'fras':fras, "zunaga":zunaga, "ko_uuid":ko_uuid}
        # this has got to be like a wizard, bc its difficult

    def maha_brukdjin(self, namai):
        self.read_data()
        UUID = str(uuid.uuid4())
        self.kirain_kaban["brukdjin"][UUID] = {"uuid":UUID, "namai":namai, "sjirujena_ko":[]}
        self.update_data()

