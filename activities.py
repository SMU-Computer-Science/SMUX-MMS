from telegram import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup, Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, Filters, CallbackContext
from database import db

import logging
# Enable logging
from telegram.utils import helpers

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)



logger = logging.getLogger(__name__)

def activities(update, context):
    
    query = update.callback_query
    query.answer()
    
    query.edit_message_text(text=display_activities(update, context),reply_markup=activities_keyboard(),
    # parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True #needed for [name](url) markdown
    )
#https://stackoverflow.com/questions/36059572/how-do-i-have-my-bot-respond-with-arguments
    
 
 

def activities_keyboard():
    keyboard = [

        [InlineKeyboardButton("Back", callback_data="callback_main_menu")],

                ]
    return InlineKeyboardMarkup(keyboard)



def display_activities(update: Update, context: CallbackContext) -> str:
    bot = context.bot
    output = ""
    acts_dict = db.child("Activities").get().val()
    for acts_id in acts_dict.keys():
        user_present = db.child("Users").child(update.effective_chat.id).child("Registered Activities").child(acts_id).get().val()
        output += f"{acts_dict[acts_id]['Name']} | /details_{acts_id}"
        if user_present:
                output += "\t(Registered)\n"
        else: output += "\n"
        output += f"Date/Time: {acts_dict[acts_id]['Date']}\n"
        output += f"Location: {acts_dict[acts_id]['Location']}\n"
        output += "\n\n"
        
    return output

