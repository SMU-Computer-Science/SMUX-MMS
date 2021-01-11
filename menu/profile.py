from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

#My Profile
def my_profile(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text=my_profile_message(),
        reply_markup=my_profile_keyboard(),
    )

def my_profile_keyboard():
    keyboard = [[InlineKeyboardButton("Back", callback_data="callback_main_menu"),]]
    return InlineKeyboardMarkup(keyboard)

def my_profile_message() -> str:
    output = "My Profile \n\n"
    output += profile_team_participation()
    output += profile_edit_message()
    return output

def profile_team_participation() -> str:
    output = "(WIP) Team name | Number of activites/events joined:\n"
    output += "\n"
    return output

def profile_edit_message()-> str:
    output = "Choose the fields you want to edit\n"
    output += "/edit_personal | Name, gender, matriculation number, date of birth, nationality.\n"
    output += "/edit_contact | SMU and personal email address, contact numbers, home address.\n"
    output += "/edit_medical | Bloodtype, medical conditions, dietary requirements, drug allergies.\n"
    output += "/edit_nok | Next-Of-Kin name, contact, relationship.\n"
    #add if conditions to conditionally display team information
    return output