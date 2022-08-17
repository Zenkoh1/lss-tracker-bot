
from dataclasses import dataclass
from telegram.error import BadRequest 

from datetime import datetime

import firestore

import constants


def new_aircraft(userinput: str):
    aircraft_list = userinput.split(' ')
    for number in aircraft_list:
        if (firestore.is_aircraft_existing(number)):
            msg = f"This aircraft ({number}) already exists in the database."
            return InputFeedbackInfo(msg, False)
    for number in aircraft_list:
        firestore.add_new_aircraft(number)
    
    
    
    
    
    msg = f"{', '.join(aircraft_list)} has been added to the list of aircraft."
    
    return InputFeedbackInfo(msg, True)

def new_equipment(userinput: str):
    equipment_list = userinput.split(' ')
    
        
    for id in equipment_list:
        if (firestore.is_equipment_existing(id)):
            msg = f"This equipment ({id}) already exists in the database."
            return InputFeedbackInfo(msg, False)
    for id in equipment_list:
        firestore.add_new_equipment(id)
    
    
    
    
    
    msg = f"{', '.join(equipment_list)} has been added to the list of equipment."
    
    return InputFeedbackInfo(msg, True)

def add_equipment(userinput: str, username: str):
    
    input_list = userinput.split(' ')

    if len(input_list) == 1:
        msg = "There is only one input, did you forget to press the spacebar?"
        return InputFeedbackInfo(msg, False)


    aircraft_number = input_list[0]

    if (not firestore.is_aircraft_existing(aircraft_number)):
        msg = f"This aircraft ({aircraft_number}) does not exist in the database."
        return InputFeedbackInfo(msg, False)
    
    equipment_list = input_list[1:]

    
    for equipment_id in equipment_list:
        if (not firestore.is_equipment_existing(equipment_id)):
            msg = f"This equipment ({equipment_id}) does not exist in the database."
            return InputFeedbackInfo(msg, False)


        if (firestore.is_equipment_onboard(equipment_id)):
            msg = f"This equipment ({equipment_id}) is already on board an aircraft, check if you have entered the correct information."
            return InputFeedbackInfo(msg, False)
    
    #loop through twice so it makes sure all equipment is valid first
    for equipment_id in equipment_list:
        firestore.add_equipment_to_aircraft(aircraft_number, equipment_id, username)
     
    
    
    
    
    
    
    
    msg = f"{', '.join(equipment_list)} has been added to {aircraft_number}."
    
    return InputFeedbackInfo(msg, True)


def remove_equipment(userinput: str, username: str):
    equipment_list = userinput.split(' ')
    
        
    
    for id in equipment_list:
        if (not firestore.is_equipment_existing(id)):
            msg = f"This equipment ({id}) does not exist in the database."
            return InputFeedbackInfo(msg, False)

        if (not firestore.is_equipment_onboard(id)):
            msg = f"This equipment ({id}) is not on board an aircraft, check if you have entered the correct information."
            return InputFeedbackInfo(msg, False)

    #loop through twice so it makes sure all equipment is valid first
    for id in equipment_list:
        firestore.remove_equipment_from_aircraft(id, username)
    
    
    
    
    
    msg = f"{', '.join(equipment_list)} has been removed from the aircraft."
    
    return InputFeedbackInfo(msg, True)


def aircraft_info(userinput: str):
    useful_info = userinput.split(' ')[0]

    if useful_info.lower() == 'all':
        all_ac_info: dict =  firestore.get_all_aircraft_info()
        msg = ''
        for ac_number in all_ac_info:
            
            equipment_list = all_ac_info[ac_number][constants.EQUIPMENT].keys()
            indiv_ac_msg = (
                f"*{ac_number}*🚁{chr(10)}"
                f"{''.join(map(lambda x: f'•{x + chr(10)}',equipment_list))}"
                "\n"
            )

            msg += indiv_ac_msg

        return InputFeedbackInfo(msg, True)
    
    if (not firestore.is_aircraft_existing(useful_info)):
        msg = f"This aircraft ({useful_info}) does not exist in the database."
        return InputFeedbackInfo(msg, False)

    
    ac_info = firestore.get_aircraft_info(useful_info)
    indiv_ac_equipment_list = ac_info[constants.EQUIPMENT]
    print(indiv_ac_equipment_list)
    date_format = "%d/%m/%y %H:%M:%S"
   
    msg = f'Aircraft number: *{useful_info}*🚁{chr(10) + chr(10)}'

    if (indiv_ac_equipment_list):
    
        for equipment in indiv_ac_equipment_list:
            indiv_equipment_msg = (f"{equipment + chr(10)}"
                                f"•Brought onto aircraft by {indiv_ac_equipment_list[equipment][constants.LAST_CHANGED_NAME]} at "
                                f"{datetime.strftime(indiv_ac_equipment_list[equipment][constants.LAST_CHANGED_TIME].astimezone(constants.TIMEZONE), date_format)+ chr(10) + chr(10)}")
            msg += indiv_equipment_msg

    else:
        msg += "_NO EQUIPMENT_"
   
    return InputFeedbackInfo(msg, True)

def equipment_info(userinput: str):
    useful_info = userinput.split(' ')[0]

    
    if (not firestore.is_equipment_existing(useful_info)):
        msg = f"This equipment ({useful_info}) does not exist in the database."
        return InputFeedbackInfo(msg, False)



    
    eq_info = firestore.get_equipment_info(useful_info)


    #check if eq is new
    if eq_info[constants.LAST_CHANGED_TIME] ==None:
        msg = f"There is no information about {useful_info} just yet."
        return InputFeedbackInfo(msg, True)
    
    date_format = "%d/%m/%y %H:%M:%S"
   
    msg = f'Aircraft number: *{useful_info}*{chr(10) + chr(10)}'
    
    msg = (f"Equipment ID: *{useful_info}*{chr(10) + chr(10)}"
           f"Aircraft: {(eq_info[constants.AIRCRAFT] if eq_info[constants.AIRCRAFT] != None else 'None') + chr(10)}")

    if eq_info[constants.AIRCRAFT] == None:
        temp_msg = (f"Removed from aircraft by {eq_info[constants.LAST_CHANGED_NAME]} "
                    f"at {datetime.strftime(eq_info[constants.LAST_CHANGED_TIME].astimezone(constants.TIMEZONE), date_format)}")
    else:
        temp_msg = (f"Brought onto aircraft by {eq_info[constants.LAST_CHANGED_NAME]} "
                    f"at {datetime.strftime(eq_info[constants.LAST_CHANGED_TIME].astimezone(constants.TIMEZONE), date_format)}")
    msg += temp_msg
    return InputFeedbackInfo(msg, True)

def delete_aircraft(userinput: str):
    ac_list = userinput.split(' ')
    for ac in ac_list:
        if (not firestore.is_aircraft_existing(ac)):
            msg = f"This aircraft ({ac}) already does not exist in the database."
            return InputFeedbackInfo(msg, False)
        
        if (firestore.does_aircraft_have_equipment(ac)):
            msg = f"This aircraft ({ac}) has equipment on it, check if all the equipment has been removed."
            return InputFeedbackInfo(msg, False)

    for ac in ac_list:
        firestore.delete_aircraft(ac)
    
    msg = f"{', '.join(ac_list)} has been successfully removed from the database."

    return InputFeedbackInfo(msg, True)


def delete_equipment(userinput: str):
    eq_list = userinput.split(' ')
    for eq in eq_list:
        if (not firestore.is_equipment_existing(eq)):
            msg = f"This equipment ({eq}) already does not exist in the database."
            return InputFeedbackInfo(msg, False)
        
        if (firestore.is_equipment_onboard(eq)):
            msg = f"This equipment ({eq}) is still on an aircraft, check if you have removed the equipment."
            return InputFeedbackInfo(msg, False)

    for eq in eq_list:
        firestore.delete_equipment(eq)
    
    msg = f"{', '.join(eq_list)} has been successfully removed from the database."

    return InputFeedbackInfo(msg, True)


@dataclass
class InputFeedbackInfo:
    msg: str
    correct_input: bool
