from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from database import db

def schedule(update, context):
    query = update.callback_query
    query.answer()
    
    output = "Upcoming Events\n\n"

    event_dict =  db.child("Users").child(update.effective_chat.id).child("Registered Events").get().val()
    if event_dict: 
        output += "This are the Upcoming Events you have registered for:\n\n"
        for event_id in event_dict.keys():
            output += f"{event_dict[event_id]} | /details_{event_id}\n"
        output += "\n\n"
        
    if not event_dict:
        
        output += "You have not signed up for any Upcoming Events\n\n"
    
    output += "Weekly Activities\n\n"

    act_dict =  db.child("Users").child(update.effective_chat.id).child("Activities").get().val()
    if act_dict: 
        output += "This are the Weekly Activities you have registered for:\n\n"
        for act_id in act_dict.keys():
            output += f"{act_dict[act_id]} | /details_{act_id}\n"
        output += "\n\n"
        
    if not act_dict:
        output += "You have not signed up for any Weekly Activities\n\n"


    output += "Tap below to view upcoming events and activties:"
    
    query.edit_message_text(text=output,reply_markup=schedule_keyboard())

def schedule_keyboard():
    keyboard = [
        [InlineKeyboardButton("View Weekly Activities", callback_data="callback_activities"),],
        [InlineKeyboardButton("View Upcoming Events", callback_data="callback_events"),],
        [InlineKeyboardButton("Main Menu", callback_data="callback_main_menu"),],
    ]
    return InlineKeyboardMarkup(keyboard)