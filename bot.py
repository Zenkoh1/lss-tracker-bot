from genericpath import exists
from telegram import Bot
from telegram.ext import Updater, CommandHandler, MessageHandler,Filters
from telegram.error import BadRequest    

import command_response

import os

#TOKEN = "5540495235:AAFfPf3FmjxmUFHwtAbegpatjILTq_gE_jI"

MODE = 'dev'
TOKEN = os.environ.get('TOKEN')

HEROKU_APP_NAME = os.environ.get('HEROKU_APP_NAME')
def run(updater):

        if MODE == 'dev':
            PORT = int(os.environ.get('PORT', 5000))
            updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
            updater.bot.setWebhook(f'https://{HEROKU_APP_NAME}.herokuapp.com/{TOKEN}')


        updater.start_polling()



if __name__ == '__main__':
    
    

    updater = Updater(TOKEN)
    #bot = Bot(token=TOKEN)
   
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(~ Filters.command, command_response.raw_text_handler))
    dp.add_handler(CommandHandler("new_ac", command_response.command_new_aircraft))
    dp.add_handler(CommandHandler("new_eq", command_response.command_new_equipment))
    dp.add_handler(CommandHandler("add", command_response.command_add))
    dp.add_handler(CommandHandler("remove", command_response.command_remove))
    dp.add_handler(CommandHandler("ac", command_response.command_aircraft_info))
    dp.add_handler(CommandHandler("eq", command_response.command_equipment_info))
    dp.add_handler(CommandHandler("del_ac", command_response.command_delete_aircraft))
    dp.add_handler(CommandHandler("del_eq", command_response.command_delete_equipment))
    run(updater)