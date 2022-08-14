
import enum
from telegram.error import BadRequest  

import firestore

import constants

import raw_text_response

raw_text_type = None

def command_new_aircraft(update, context):
    global raw_text_type
  
    try:
        
        
        update.message.reply_text("Enter the tail number(s) of the aircraft, separated by spaces.")
        raw_text_type = constants.RawTextType.NEW_AIRCRAFT
        
    except BadRequest:
  
        update.message.reply_text("An error has occurred, please try again.")

def command_new_equipment(update, context):
    global raw_text_type

    try:
        
        
        update.message.reply_text("Enter the ID(s) of the equipment, separated by spaces.")
        raw_text_type = constants.RawTextType.NEW_EQUIPMENT
        
    except BadRequest:
  
        update.message.reply_text("An error has occurred, please try again.")


def command_add(update, context):
    global raw_text_type

    try:
        
        
        update.message.reply_text("Enter the tail number of the aircraft, followed by the ID(s) of the equipment, separated by spaces.")
        raw_text_type = constants.RawTextType.ADD_EQUIPMENT
        
    except BadRequest:
  
        update.message.reply_text("An error has occurred, please try again.")


def command_remove(update, context):
    global raw_text_type

    try:
        
        
        update.message.reply_text("Enter the ID(s) of the equipment, separated by spaces.")
        raw_text_type = constants.RawTextType.REMOVE_EQUIPMENT
        
    except BadRequest:
  
        update.message.reply_text("An error has occurred, please try again.")


def command_aircraft_info(update, context):
    global raw_text_type

    try:
        
        
        update.message.reply_text("Enter the aircraft tail number, or type 'all' if you need an overview of all the aircraft.")
        raw_text_type = constants.RawTextType.AIRCRAFT_INFO
        
    except BadRequest:
  
        update.message.reply_text("An error has occurred, please try again.")

def command_equipment_info(update, context):

    #not sure whether I should implement the 'all' function
    global raw_text_type

    try:
        
        
        update.message.reply_text("Enter the equipment ID number.")
        raw_text_type = constants.RawTextType.EQUIPMENT_INFO
        
    except BadRequest:
  
        update.message.reply_text("An error has occurred, please try again.")

def command_delete_aircraft(update, context):
    global raw_text_type

    try:
        
        
        update.message.reply_text("Enter the aircraft tail number(s), separated by spaces.")
        raw_text_type = constants.RawTextType.DELETE_AIRCRAFT
        
    except BadRequest:
  
        update.message.reply_text("An error has occurred, please try again.")


def command_delete_equipment(update, context):


    global raw_text_type

    try:
        
        
        update.message.reply_text("Enter the equipment ID(s), separated by spaces")
        raw_text_type = constants.RawTextType.DELETE_EQUIPMENT
        
    except BadRequest:
  
        update.message.reply_text("An error has occurred, please try again.")








def raw_text_handler(update, context):
    global raw_text_type
    try: 

        user_input = update.message.text
        username = update.message.from_user['username']

        if raw_text_type == constants.RawTextType.NEW_AIRCRAFT:
            input_feedback_info: raw_text_response.InputFeedbackInfo = raw_text_response.new_aircraft(user_input)
            if input_feedback_info.correct_input:
                raw_text_type = None
            
            update.message.reply_text(input_feedback_info.msg)
        
        elif raw_text_type == constants.RawTextType.NEW_EQUIPMENT:
            input_feedback_info: raw_text_response.InputFeedbackInfo = raw_text_response.new_equipment(user_input)
            if input_feedback_info.correct_input:
                raw_text_type = None
            
            update.message.reply_text(input_feedback_info.msg)
        elif raw_text_type == constants.RawTextType.ADD_EQUIPMENT:
            input_feedback_info: raw_text_response.InputFeedbackInfo = raw_text_response.add_equipment(user_input, username)
            if input_feedback_info.correct_input:
                raw_text_type = None
            
            update.message.reply_text(input_feedback_info.msg)

        elif raw_text_type == constants.RawTextType.REMOVE_EQUIPMENT:
            input_feedback_info: raw_text_response.InputFeedbackInfo = raw_text_response.remove_equipment(user_input, username)
            if input_feedback_info.correct_input:
                raw_text_type = None
            
            update.message.reply_text(input_feedback_info.msg)

        elif raw_text_type == constants.RawTextType.AIRCRAFT_INFO:
            input_feedback_info: raw_text_response.InputFeedbackInfo = raw_text_response.aircraft_info(user_input)
            if input_feedback_info.correct_input:
                raw_text_type = None
            
            update.message.reply_text(input_feedback_info.msg, parse_mode = 'Markdown')

        elif raw_text_type == constants.RawTextType.EQUIPMENT_INFO:
            input_feedback_info: raw_text_response.InputFeedbackInfo = raw_text_response.equipment_info(user_input)
            if input_feedback_info.correct_input:
                raw_text_type = None
            
            update.message.reply_text(input_feedback_info.msg, parse_mode = 'Markdown')
        elif raw_text_type == constants.RawTextType.DELETE_AIRCRAFT:
            input_feedback_info: raw_text_response.InputFeedbackInfo = raw_text_response.delete_aircraft(user_input)
            if input_feedback_info.correct_input:
                raw_text_type = None
            
            update.message.reply_text(input_feedback_info.msg, parse_mode = 'Markdown')

        elif raw_text_type == constants.RawTextType.DELETE_EQUIPMENT:
            input_feedback_info: raw_text_response.InputFeedbackInfo = raw_text_response.delete_equipment(user_input)
            if input_feedback_info.correct_input:
                raw_text_type = None
            
            update.message.reply_text(input_feedback_info.msg, parse_mode = 'Markdown')

        else:
            msg ="placeholder for /help, ie all the commands"

            update.message.reply_text(msg, parse_mode = 'Markdown')

    except BadRequest:
        update.message.reply_text("An error has occurred, please try again.")
        
