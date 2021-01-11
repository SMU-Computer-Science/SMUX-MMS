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

def events(update, context):
    
    query = update.callback_query
    query.answer()
    
    query.edit_message_text(text=display_events(update, context),reply_markup=events_keyboard(),
    # parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True #needed for [name](url) markdown
    )
#https://stackoverflow.com/questions/36059572/how-do-i-have-my-bot-respond-with-arguments
    
 
 

def events_keyboard():
    keyboard = [

        [InlineKeyboardButton("Back", callback_data="callback_main_menu")],

                ]
    return InlineKeyboardMarkup(keyboard)



def display_events(update: Update, context: CallbackContext) -> str:
    bot = context.bot
    output = ""
    events_dict = db.child("Events").get().val()
    for event_id in events_dict.keys():
        user_present = db.child("Users").child(update.effective_chat.id).child("Registered Events").child(event_id).get().val()
        output += f"{events_dict[event_id]['Name']} | /details_{event_id}"
        if user_present:
                output += "\t(Registered)\n"
        else: output += "\n"
        output += f"Date/Time: {events_dict[event_id]['Date']}\n"
        output += f"Location: {events_dict[event_id]['Location']}\n"
        output += "\n\n"
        
    return output

def details(update: Update, context: CallbackContext) -> None:
    keyboard = [[InlineKeyboardButton("Back", callback_data="callback_activities")]]
    

    word = str(update.message.text)
    event_id = word.replace('/details_', '')
    event = db.child("Activities").child(event_id).get().val()
    if not event: #if id not found, search in events
        event =  db.child("Events").child(event_id).get().val()
        keyboard = [[InlineKeyboardButton("Back", callback_data="callback_events")]] #change the button to return to events instead of activties
    
    user_present = db.child("Users").child(update.effective_chat.id).child("Registered Events").child(event_id).get().val()

    if not user_present:
        user_present = db.child("Users").child(update.effective_chat.id).child("Registered Activities").child(event_id).get().val()

    if user_present: 
         update.message.reply_text(
        f"{event['Name']}\n"
        f"Date/Time: {event['Date']}\n"
        f"Location: {event['Location']}\n"
        f"Description: {event['Description']}\n\n"
        f"/unregister_{event_id}",
        reply_markup= InlineKeyboardMarkup(keyboard)
    ) 
    else:
        update.message.reply_text(
        f"{event['Name']}\n"
        f"Date/Time: {event['Date']}\n"
        f"Location: {event['Location']}\n"
        f"Description: {event['Description']}\n\n"
        f"/register_{event_id}",
        reply_markup= InlineKeyboardMarkup(keyboard)
        )

   

def register(update: Update, context: CallbackContext) -> None:
    keyboard = [[InlineKeyboardButton("Back", callback_data="callback_activities")]]
    word = str(update.message.text)
    event_id = word.replace('/register_', '')
    event_type = "Activities"
    event = db.child("Activities").child(event_id).get().val()
    if not event: #if id not found, search in events
        event =  db.child("Events").child(event_id).get().val()
        event_type = "Events"
        keyboard = [[InlineKeyboardButton("Back", callback_data="callback_events")]]
    
    db.child(event_type).child(event_id).child("Participants").child(update.effective_chat.id).set("date registered")
    db.child("Users").child(update.effective_chat.id).child(f"Registered {event_type}").child(event_id).set(event['Name'])
    update.message.reply_text(f"Successfully registered for {event['Name']}", reply_markup= InlineKeyboardMarkup(keyboard))


def unregister(update: Update, context: CallbackContext) -> None:
    keyboard = [[InlineKeyboardButton("Back", callback_data="callback_activities")]]
    word = str(update.message.text)
    event_id = word.replace('/unregister_', '')
    event_type = "Activities"
    event = db.child("Activities").child(event_id).get().val()
    if not event: #if id not found, search in activities
        event =  db.child("Events").child(event_id).get().val()
        event_type = "Events"
        keyboard = [[InlineKeyboardButton("Back", callback_data="callback_events")]]

    db.child(event_type).child(event_id).child("Participants").child(update.effective_chat.id).remove()
    db.child("Users").child(update.effective_chat.id).child(f"Registered {event_type}").child(event_id).remove()
    update.message.reply_text(f"Successfully unregistered for {event['Name']}", reply_markup= InlineKeyboardMarkup(keyboard))