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
email_validator = '^[a-z]+[.]2[0-9]{3}[@][a-z]{3,4}[.][s][m][u][.][e][d][u][.][s][g]' # For email validation

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

BLOODTYPE, MEDICAL_CONDITIONS, DIETARY_REQUIREMENTS, DRUG_ALLERGIES, EDIT = range(5)
EDIT_BLOODTYPE_END, EDIT_MEDICAL_CONDITIONS_END, EDIT_DIETARY_REQUIREMENTS_END, EDIT_DRUG_ALLERGIES_END = range(5,9)

medicalinfo = {
    "bloodtype" : "",
    "medical_conditions" : "",
    "dietary_requirements" : "",
    "drug_allergies" : "",
}

def medical_launcher(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    reply_keyboard = [['O+', 'O-'], ['AB+', 'AB-'], ['A+', 'A-'], ['B+', 'B-']]
    context.bot.send_message(
        text='Blood Type:',chat_id=update.effective_chat.id,
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )

    return BLOODTYPE

def test(update: Update, context: CallbackContext) -> None:
    reply_keyboard = [['O+', 'O-'], ['AB+', 'AB-'], ['A+', 'A-'], ['B+', 'B-']]
    context.bot.send_message(
        text='Blood Type:',chat_id=update.effective_chat.id,
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )

    return BLOODTYPE

def bloodtype(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    medicalinfo["bloodtype"] = update.message.text
    logger.info("User <%s> Blood type: %s", user.first_name, update.message.text)
    update.message.reply_text(
        "Enter your prevailing medical conditions, or 'NA' if you have none.",
        reply_markup=ReplyKeyboardRemove(),
    )

    return MEDICAL_CONDITIONS

def medical_conditions(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    medicalinfo["medical_conditions"] = update.message.text
    logger.info("User <%s> Medical conditions: %s", user.first_name, update.message.text)
    update.message.reply_text(
        "Enter your dietary requirements, or 'NA' if you have none.",
        reply_markup=ReplyKeyboardRemove(),
    )

    return DIETARY_REQUIREMENTS

def dietary_requirements(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    medicalinfo["dietary_requirements"] = update.message.text
    logger.info("User <%s> Dietary requirements: %s", user.first_name, update.message.text)
    update.message.reply_text(
        "Enter your drug allergies, or 'NA' if you have none.",
        reply_markup=ReplyKeyboardRemove(),
    )

    return DRUG_ALLERGIES

def drug_allergies(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    medicalinfo["drug_allergies"] = update.message.text
    logger.info("User <%s> Drug allergies: %s", user.first_name, update.message.text)
    update.message.reply_text("Please check if your information entered is correct.\n\n" + editmedicalinfo_message(), reply_markup=ReplyKeyboardRemove())

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

def edit_medical_entry(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    data = db.child("Users").child(user.id).child("Personal Particulars").child("Medical").get().val()
    medicalinfo["bloodtype"] = data["bloodtype"]
    medicalinfo["medical_conditions"] = data["medical_conditions"]
    medicalinfo["dietary_requirements"] = data["dietary_requirements"]
    medicalinfo["drug_allergies"] = data["drug_allergies"]
    logger.info("User <%s> Medical data received.", user.first_name)
    update.message.reply_text(editmedicalinfo_message(), reply_markup=ReplyKeyboardRemove())

    return EDIT

def edit_bloodtype_start(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [['O+', 'O-'], ['AB+', 'AB-'], ['A+', 'A-'], ['B+', 'B-']]
    update.message.reply_text(
        'Blood Type:',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )

    return EDIT_BLOODTYPE_END

def edit_bloodtype_end(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    medicalinfo["bloodtype"] = update.message.text
    logger.info("User <%s> edited their blood type to: %s", user.first_name, update.message.text)
    update.message.reply_text(editmedicalinfo_message(), reply_markup=ReplyKeyboardRemove())
    
    return EDIT

def edit_medical_conditions_start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Update your medical conditions. If there are none, please enter "NA".',
        reply_markup=ReplyKeyboardRemove(),
    )

    return EDIT_MEDICAL_CONDITIONS_END

def edit_medical_conditions_end(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    medicalinfo["medical_conditions"] = update.message.text
    logger.info("User <%s> edited their medical condition to: %s", user.first_name, update.message.text)
    update.message.reply_text(editmedicalinfo_message(), reply_markup=ReplyKeyboardRemove())
    
    return EDIT

def edit_dietary_requirements_start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Update your dietary requirements. If there are none, please enter "NA".',
        reply_markup=ReplyKeyboardRemove(),
    )

    return EDIT_DIETARY_REQUIREMENTS_END

def edit_dietary_requirements_end(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    medicalinfo["dietary_requirements"] = update.message.text
    logger.info("User <%s> edited their dietary requirements to: %s", user.first_name, update.message.text)
    update.message.reply_text(editmedicalinfo_message(), reply_markup=ReplyKeyboardRemove())
    
    return EDIT

def edit_drug_allergies_start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Update your drug allergies. If there are none, please enter "NA".',
        reply_markup=ReplyKeyboardRemove(),
    )

    return EDIT_DRUG_ALLERGIES_END

def edit_drug_allergies_end(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    medicalinfo["drug_allergies"] = update.message.text
    logger.info("User <%s> edited their drug allergies to: %s", user.first_name, update.message.text)
    update.message.reply_text(editmedicalinfo_message(), reply_markup=ReplyKeyboardRemove())
    
    return EDIT

def editmedicalinfo_message() -> str:
    output = "Click the fields below to edit or /done if everything is correct.\n"
    output += f"/Blood_Type: {medicalinfo['bloodtype']}\n"
    output += f"/Medical_Conditions: {medicalinfo['medical_conditions']}\n"
    output += f"/Dietary_Requirements: {medicalinfo['dietary_requirements']}\n"
    output += f"/Drug_Allergies: {medicalinfo['drug_allergies']}\n"
    
    return output

def done(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    info = db.child("Users").child(user.id).child("Personal Particulars").child("NOK").get().val()
    
    #temporary manual return button to my_profile
    #is there a way to automatically call my_profile?
    keyboard = [[InlineKeyboardButton("Back", callback_data="callback_my_profile"),]]
    if info: #check if existing user
        update.message.reply_text(
            "Medical information updated.",
            reply_markup=InlineKeyboardMarkup(keyboard), #temp manual return
        )
    else: #new user
        #segue into NOK for first time user
        keyboard = [[InlineKeyboardButton("Continue", callback_data="callback_noknew")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            "The following section requires your Next-of-Kin (NOK) details.",
            reply_markup=reply_markup,
        )

    #database push!
    db.child("Users").child(user.id).child("Personal Particulars").child("Medical").set(medicalinfo)
    logger.info("User <%s> confirmed their medical details. Uploaded to database.", user.first_name)
    #database done pushing
    #how to integrate back into main menu

    return ConversationHandler.END


#==============================================================================================#

# Fallback commands (return to all other menus), remember to integrate with main functions

def cancel(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User <%s> canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Bot successfully cancelled.', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END

#==============================================================================================#

medical_conv = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(medical_launcher, pattern="callback_medical_new"),
        CommandHandler('edit_medical', edit_medical_entry),
        CommandHandler('md', test), #for testing
        ],
    states={
        BLOODTYPE: [MessageHandler(Filters.regex('^(O\+|O\-|AB\+|AB\-|A\+|A\-|B\+|B\-)$'), bloodtype)],
        MEDICAL_CONDITIONS: [MessageHandler(Filters.text & ~Filters.command, medical_conditions),],
        DIETARY_REQUIREMENTS: [MessageHandler(Filters.text & ~Filters.command, dietary_requirements),],
        DRUG_ALLERGIES: [MessageHandler(Filters.text & ~Filters.command, drug_allergies),],
        EDIT: [
            CommandHandler('done', done),
            CommandHandler('Blood_Type', edit_bloodtype_start),
            CommandHandler('Medical_Conditions', edit_medical_conditions_start),
            CommandHandler('Dietary_Requirements', edit_dietary_requirements_start),
            CommandHandler('Drug_Allergies', edit_drug_allergies_start),
        ],
        EDIT_BLOODTYPE_END: [MessageHandler(Filters.regex('^(O\+|O\-|AB\+|AB\-|A\+|A\-|B\+|B\-)$'), edit_bloodtype_end)],
        EDIT_MEDICAL_CONDITIONS_END: [MessageHandler(Filters.text & ~Filters.command, edit_medical_conditions_end)],
        EDIT_DIETARY_REQUIREMENTS_END: [MessageHandler(Filters.text & ~Filters.command, edit_dietary_requirements_end)],
        EDIT_DRUG_ALLERGIES_END: [MessageHandler(Filters.text & ~Filters.command, edit_drug_allergies_end)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
    )
