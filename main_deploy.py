#FUNCTIONAL MODULES
from start import start
from pparticulars.signup import signup_conv
from pparticulars.nok import nok_conv
from pparticulars.contact import contact_conv
from pparticulars.medical import medical_conv
from menu.menu import (
    main_menu, cmd_menu, credits, pdpa, pdpa_disposable, delete_recent, more_menu, faq,
)
from menu.profile import  my_profile
from activities import activities
from events import events, details, register, unregister
from schedule import schedule

#KEY MODULES
from database import db
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
    CallbackQueryHandler,
    RegexHandler,
)
import logging
from dotenv import load_dotenv
import os

#WebHook
PORT = int(os.environ.get('PORT', '5000'))

#Logging Module
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

#Token
load_dotenv('.env')
updater = Updater(token=os.getenv('SMUX_BOT_TOKEN'), use_context=True)
dispatcher = updater.dispatcher

#==============================================================================================#

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

dispatcher.add_handler(signup_conv)
dispatcher.add_handler(contact_conv)
dispatcher.add_handler(medical_conv)
dispatcher.add_handler(nok_conv)

#events callbacks

# updater.dispatcher.add_handler(RegexHandler('^(/info_[\d]+)$', info))
updater.dispatcher.add_handler(MessageHandler(Filters.regex('^(/details_[\d]+)$'), details))
updater.dispatcher.add_handler(MessageHandler(Filters.regex('^(/register_[\d]+)$'), register))
updater.dispatcher.add_handler(MessageHandler(Filters.regex('^(/unregister_[\d]+)$'), unregister))
# dispatcher.add_handler(CommandHandler("details", detailed_event, pass_args=True))

#Main Menu Callbacks
updater.dispatcher.add_handler(CommandHandler('menu', cmd_menu))
# updater.dispatcher.add_handler(CommandHandler('done', cmd_my_profile))
updater.dispatcher.add_handler(CallbackQueryHandler(main_menu, pattern='callback_main_menu'))
updater.dispatcher.add_handler(CallbackQueryHandler(my_profile, pattern='callback_my_profile'))
updater.dispatcher.add_handler(CallbackQueryHandler(more_menu, pattern='callback_more_menu'))
updater.dispatcher.add_handler(CallbackQueryHandler(activities, pattern='callback_activities'))
updater.dispatcher.add_handler(CallbackQueryHandler(events, pattern='callback_events'))
updater.dispatcher.add_handler(CallbackQueryHandler(schedule, pattern='callback_schedule'))

#More Menu Callbacks
updater.dispatcher.add_handler(CallbackQueryHandler(faq, pattern='callback_faq'))
updater.dispatcher.add_handler(CallbackQueryHandler(credits, pattern='callback_credits'))
updater.dispatcher.add_handler(CallbackQueryHandler(pdpa, pattern='callback_pdpa'))
updater.dispatcher.add_handler(CallbackQueryHandler(pdpa_disposable, pattern='callback_disposable'))
updater.dispatcher.add_handler(CallbackQueryHandler(delete_recent, pattern='callback_delete'))

updater.start_webhook(listen="0.0.0.0",
                       port=PORT,
                       url_path="SMUX_EXCO_BOT_TOKEN")
updater.bot.setWebhook('https://smux-mms-backend.herokuapp.com/' + "SMUX_EXCO_BOT_TOKEN")
updater.idle()


#Activites conversation handler
#==============================================================================================#

