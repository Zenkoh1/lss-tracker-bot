import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import constants

import datetime

import os

FIREBASE_CREDS = os.environ.get("FIREBASE_CREDS")
cred = credentials.Certificate(dict(FIREBASE_CREDS))
firebase_admin.initialize_app(cred)
db: firestore.firestore.Client = firestore.client()

def add_new_aircraft(number):
    doc_ref = db.collection(constants.AIRCRAFT).document(number)
    if (not doc_ref.get().exists):
        doc_ref.set({constants.EQUIPMENT: {}})

def add_new_equipment(id):
    doc_ref = db.collection(constants.EQUIPMENT).document(id)
    if (not doc_ref.get().exists):
        doc_ref.set({constants.AIRCRAFT: None, constants.LAST_CHANGED_TIME: None, constants.LAST_CHANGED_NAME: None})

def add_equipment_to_aircraft(aircraft_number, equipment_id, username):

    time_now = datetime.datetime.now(constants.TIMEZONE)

    print(time_now)
    #update aircraft collection
    ac_doc_ref = db.collection(constants.AIRCRAFT).document(aircraft_number)
    ac_doc_ref.update({f"{constants.EQUIPMENT}.{equipment_id}": {constants.LAST_CHANGED_TIME: time_now, constants.LAST_CHANGED_NAME: username}})

    #update equipment collection
    eq_doc_ref = db.collection(constants.EQUIPMENT).document(equipment_id)
    eq_doc_ref.update({constants.AIRCRAFT: aircraft_number, constants.LAST_CHANGED_TIME: time_now, constants.LAST_CHANGED_NAME: username})

def remove_equipment_from_aircraft(equipment_id, username):
    time_now = datetime.datetime.now(constants.TIMEZONE)

    #update equipment collection
    eq_doc_ref = db.collection(constants.EQUIPMENT).document(equipment_id)
    aircraft_number = eq_doc_ref.get().get(constants.AIRCRAFT)

    eq_doc_ref.update({constants.AIRCRAFT: None, constants.LAST_CHANGED_TIME: time_now, constants.LAST_CHANGED_NAME: username})
    
    
    #update aircraft collection
    ac_doc_ref = db.collection(constants.AIRCRAFT).document(aircraft_number)
    ac_doc_ref.update({f"{constants.EQUIPMENT}.{equipment_id}": firestore.DELETE_FIELD})



def get_all_aircraft_info():
    
    ac_docs= db.collection(constants.AIRCRAFT).stream()
    all_ac_dict = {}
    for doc in ac_docs:

        all_ac_dict[doc.id] = doc.to_dict()
    return all_ac_dict

def get_aircraft_info(number):
    ac_doc = db.collection(constants.AIRCRAFT).document(number).get()

    ac_dict = ac_doc.to_dict()

    return ac_dict

def get_equipment_info(id):
    eq_doc = db.collection(constants.EQUIPMENT).document(id).get()

    eq_dict = eq_doc.to_dict()

    return eq_dict

def delete_aircraft(number):
    #Delete from aircraft collection, for now, i assume that it will correctly check
    #that this aircraft has no equipment on board
    ac_doc_ref = db.collection(constants.AIRCRAFT).document(number)
    ac_doc_ref.delete()


def delete_equipment(id):
    #Delete from equipment collection, for now, i assume that it will correctly check
    #that this equipment is not on board any aircraft
    eq_doc_ref = db.collection(constants.EQUIPMENT).document(id)
    eq_doc_ref.delete() 

def is_aircraft_existing(number):
    doc_ref = db.collection(constants.AIRCRAFT).document(number)
    if (doc_ref.get().exists):
        return True
    return False

def is_equipment_existing(id):
    doc_ref = db.collection(constants.EQUIPMENT).document(id)
    
    if (doc_ref.get().exists):
        return True
    return False

def does_aircraft_have_equipment(number):

    doc_ref = db.collection(constants.AIRCRAFT).document(number)
    if (doc_ref.get().get(constants.EQUIPMENT)):
        return True
    return False
def is_equipment_onboard(id):
    doc = db.collection(constants.EQUIPMENT).document(id).get()
    if (doc.exists):
        if (doc.get(constants.AIRCRAFT) != None):
            return True
    return False





