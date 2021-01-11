#signup v5
from database import db
import logging
import re
from typing import Dict

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
    CallbackQueryHandler,
)


# Global Variable 
dob_validator = '^(0[1-9]|[1-2][0-9]|3[0-1])-(0[1-9]|1[0-2])-[0-9]{4}'

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

SIGNUP, NAME, GENDER, MATNUM, DOB, NATIONALITY = range(6)
EDIT, EDIT_NAME_END, EDIT_GENDER_END, EDIT_MATNUM_END, EDIT_DOB_END, EDIT_NATIONALITY_END,  = range(6, 12)

userinfo = {
    "name" : "",
    "gender" : "",
    "matnum" : "",
    "dob" : "",
    "nationality" : "",
}

def signup(update: Update, context: CallbackContext) -> int:
    context.bot.send_message(chat_id=update.effective_chat.id, text='Full name (according to matriculation):',)
    return NAME


def name(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    userinfo["name"] = update.message.text
    logger.info("User <%s> Matriculated name: %s", user.first_name, update.message.text)
    reply_keyboard = [['Male', 'Female']]
    update.message.reply_text(
        'Select gender:',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )

    return GENDER

def gender(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    userinfo["gender"] = update.message.text
    logger.info("User <%s> Gender: %s", user.first_name, update.message.text)
    update.message.reply_text(
        'Matriculation number (e.g. 01234567):',
        reply_markup=ReplyKeyboardRemove(),
    )

    return MATNUM

def matnum(update: Update, context: CallbackContext) -> int:
    user = update.message.from_useruser = update.message.from_user
    for i in update.message.text:
        if not i.isdigit() or len(update.message.text) != 8:
            update.message.reply_text(
                'Enter a valid 8-digit matriculation number (e.g. 01234567):',
                reply_markup=ReplyKeyboardRemove(),
            )
            return MATNUM
    userinfo["matnum"] = update.message.text
    logger.info("User <%s> Matriculation number: %s", user.first_name, update.message.text)
    update.message.reply_text(
        'Date of Birth (dd-mm-yyyy):',
        reply_markup=ReplyKeyboardRemove(),
    )

    return DOB

def dob(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    if not re.search(dob_validator, update.message.text):
        logger.info(False)
        update.message.reply_text(
            "Please enter your Date of Birth in the format dd-mm-yyyy:",
            reply_markup=ReplyKeyboardRemove(),
        )
        return DOB
    userinfo["dob"] = update.message.text
    logger.info("User <%s> DOB: %s", user.first_name, update.message.text)
    reply_keyboard = [['Singapore Citizen'], ['Singapore PR']]
    update.message.reply_text(
        'Nationality (select if applicable, otherwise please type out your nationality):',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )

    return NATIONALITY

def nationality(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    userinfo["nationality"] = update.message.text
    logger.info("User <%s> Nationality: %s", user.first_name, update.message.text)
    update.message.reply_text("Please check if your information entered is correct.\n\n" + edituserinfo_message(), reply_markup=ReplyKeyboardRemove())

    return EDIT


#==============================================================================================#
                            #  _______  ______  __________________ #
                            # (  ____ \(  __  \ \__   __/\__   __/ #
                            # | (    \/| (  \  )   ) (      ) (    #
                            # | (__    | |   ) |   | |      | |    #
                            # |  __)   | |   | |   | |      | |    #
                            # | (      | |   ) |   | |      | |    #
                            # | (____/\| (__/  )___) (___   | |    #
                            # (_______/(______/ \_______/   )_(    #
                            #                                      #
#==============================================================================================#

def edit_personal_entry(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    data = db.child("Users").child(user.id).child("Personal Particulars").child("Personal").get().val()
    userinfo["name"] = data["name"]
    userinfo["gender"] = data["gender"]
    userinfo["matnum"] = data["matnum"]
    userinfo["dob"] = data["dob"]
    userinfo["nationality"] = data["nationality"]
    logger.info("User <%s> Personal data received.", user.first_name)
    update.message.reply_text(edituserinfo_message(), reply_markup=ReplyKeyboardRemove())

    return EDIT

def edit_name_start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Full name (according to matriculation):',
    )

    return EDIT_NAME_END

def edit_name_end(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    userinfo["name"] = update.message.text
    logger.info("User <%s> edited their matriculated name to: %s", user.first_name, update.message.text)
    update.message.reply_text(edituserinfo_message(), reply_markup=ReplyKeyboardRemove())
    
    return EDIT

def edit_gender_start(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [['Male', 'Female']]
    update.message.reply_text(
        'Select gender:',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )

    return EDIT_GENDER_END

def edit_gender_end(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    userinfo["gender"] = update.message.text
    logger.info("User <%s> edited their gender to: %s", user.first_name, update.message.text)
    update.message.reply_text(edituserinfo_message(), reply_markup=ReplyKeyboardRemove())
    
    return EDIT

def edit_matnum_start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Matriculation number:',
        reply_markup=ReplyKeyboardRemove(),
    )

    return EDIT_MATNUM_END

def edit_matnum_end(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    for i in update.message.text:
        if not i.isdigit() or len(update.message.text) != 8:
            update.message.reply_text(
                'Enter a valid 8-digit matriculation number (e.g. 01234567):',
                reply_markup=ReplyKeyboardRemove(),
            )
            return EDIT_MATNUM_END
    userinfo["matnum"] = update.message.text
    logger.info("User <%s> edited their matriculation number to: %s", user.first_name, update.message.text)
    update.message.reply_text(edituserinfo_message(), reply_markup=ReplyKeyboardRemove())
    
    return EDIT

def edit_dob_start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Date of Birth (dd-mm-yyyy):',
        reply_markup=ReplyKeyboardRemove(),
    )

    return EDIT_DOB_END

def edit_dob_end(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    if not re.search(dob_validator, update.message.text):
        logger.info(False)
        update.message.reply_text(
            "Please enter your Date of Birth in the format dd-mm-yyyy:",
            reply_markup=ReplyKeyboardRemove(),
        )
        return EDIT_DOB_END
    userinfo["dob"] = update.message.text
    logger.info("User <%s> edited their DOB to: %s", user.first_name, update.message.text)
    update.message.reply_text(edituserinfo_message(), reply_markup=ReplyKeyboardRemove())
    
    return EDIT

def edit_nationality_start(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [['Singapore Citizen'], ['Singapore PR']]
    update.message.reply_text(
        'Nationality (select if applicable, otherwise please type out your nationality):',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )

    return EDIT_NATIONALITY_END

def edit_nationality_end(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    userinfo["nationality"] = update.message.text
    logger.info("User <%s> edited their Nationality to: %s", user.first_name, update.message.text)
    update.message.reply_text(edituserinfo_message(), reply_markup=ReplyKeyboardRemove())
    
    return EDIT

def edituserinfo_message() -> str:
    output = "Click the fields below to edit or /done if everything is correct.\n"
    output += f"/Name: {userinfo['name']}\n"
    output += f"/Gender: {userinfo['gender']}\n"
    output += f"/Matriculation_Number: {userinfo['matnum']}\n"
    output += f"/DOB: {userinfo['dob']}\n"
    output += f"/Nationality: {userinfo['nationality']}\n"
    
    return output

def done(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    info = db.child("Users").child(user.id).child("Personal Particulars").child("Contact").get().val()
    
    #temporary manual return button to my_profile
    #is there a way to automatically call my_profile?
    keyboard = [[InlineKeyboardButton("Back", callback_data="callback_my_profile"),]]
    if info: #check if existing user
        update.message.reply_text(
            "Personal particulars updated.",
            reply_markup=InlineKeyboardMarkup(keyboard), #temp manual return
        )
    else: #new user
        #segue into contact details for first time user
        keyboard = [[InlineKeyboardButton("Continue", callback_data="callback_contact_new")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            "The following section requires your contact details.",
            reply_markup=reply_markup,
        )

    #odd/even calculator
    if int(userinfo["matnum"]) % 2 == 0:
        oddeven = "Even"
    else:
        oddeven = "Odd"
    #database push!
    data_db_new = {
        "name" : userinfo["name"],
        "gender" : userinfo["gender"],
        "matnum" : userinfo["matnum"],
        "dob" : userinfo["dob"],
        "nationality" : userinfo["nationality"],
        "telehandle" : user.username,
        "oddeven": oddeven,
    }

    db.child("Users").child(user.id).child("Personal Particulars").child("Personal").set(data_db_new)
    logger.info("User <%s> confirmed their personal details. Uploaded to database.", user.first_name)
    #database done pushing
    #how to integrate back into main menu

    return ConversationHandler.END


#==============================================================================================#

# Fallback commands (return to all other menus), remember to integrate with main functions

def cancel(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User <%s> canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Action cancelled.', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END

#==============================================================================================#

signup_conv = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(signup, pattern="callback_signup"),
        CommandHandler('edit_personal', edit_personal_entry)],
    states={
        SIGNUP:  [CommandHandler('signup', signup)],
        NAME: [MessageHandler(Filters.text & ~Filters.command, name)],
        GENDER: [MessageHandler(Filters.regex('^(Male|Female)$'), gender)],
        MATNUM: [MessageHandler(Filters.text & ~Filters.command, matnum)],
        DOB: [MessageHandler(Filters.text & ~Filters.command, dob)],
        NATIONALITY: [MessageHandler(Filters.text & ~Filters.command, nationality)],
        EDIT: [
            CommandHandler('done', done),
            CommandHandler('Name', edit_name_start),
            CommandHandler('Gender', edit_gender_start),
            CommandHandler('Matriculation_Number', edit_matnum_start),
            CommandHandler('DOB', edit_dob_start),
            CommandHandler('Nationality', edit_nationality_start),
        ],
        EDIT_NAME_END: [MessageHandler(Filters.text & ~Filters.command, edit_name_end)],
        EDIT_GENDER_END: [MessageHandler(Filters.regex('^(Male|Female)$'), edit_gender_end)],
        EDIT_MATNUM_END: [MessageHandler(Filters.text & ~Filters.command, edit_matnum_end)],
        EDIT_DOB_END: [MessageHandler(Filters.text & ~Filters.command, edit_dob_end)],
        EDIT_NATIONALITY_END: [MessageHandler(Filters.text & ~Filters.command, edit_nationality_end)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
    )
