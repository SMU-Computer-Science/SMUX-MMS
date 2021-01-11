
import logging
from database import db
from typing import Dict
import re

from telegram import InlineKeyboardButton, InlineKeyboardMarkup,ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
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
smu_email_validator = '^[a-z]+[.]2[0-9]{3}[@][a-z]{3,4}[.][s][m][u][.][e][d][u][.][s][g]' # For smu email validation
personal_email_validator = '^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$' # For personal email validation

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

EMAIL_SMU, EMAIL_PERSONAL, CONTACTNO_MOBILE, CONTACTNO_HOME, ADDRESS, EDIT = range(6)
EDIT_EMAIL_SMU_END, EDIT_EMAIL_PERSONAL_END, EDIT_CONTACTNO_MOBILE_END, EDIT_CONTACTNO_HOME_END, EDIT_ADDRESS_END = range (6, 11)
contactinfo = {
    "email_smu" : "",
    "email_personal" : "",
    "contactno_mobile" : "",
    "contactno_home" : "",
    "address" : "",
}


def contact(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    context.bot.send_message(
        text='Please enter your SMU email address:',chat_id=update.effective_chat.id,
        reply_markup=ReplyKeyboardRemove()
    )

    return EMAIL_SMU


def test(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(
        text='Please enter your SMU email address:',chat_id=update.effective_chat.id,
        reply_markup=ReplyKeyboardRemove()
    )

    return EMAIL_SMU

def email_smu(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    if not re.search(smu_email_validator, update.message.text):
        logger.info(False)
        update.message.reply_text("Please enter a vaild SMU email address (e.g. johntan.2020@sis.smu.edu.sg):")
        return EMAIL_SMU
    contactinfo["email_smu"] = update.message.text
    logger.info("User <%s> SMU Email: %s", user.first_name, update.message.text)
    update.message.reply_text(
        'Please enter your primary personal email:'
    )

    return EMAIL_PERSONAL

def email_personal(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    if not re.search(personal_email_validator, update.message.text):
        logger.info(False)
        update.message.reply_text("Please enter a vaild email address (e.g. johntan@gmail.com):")
        return EMAIL_PERSONAL
    contactinfo["email_personal"] = update.message.text
    logger.info("User <%s> Personal Email: %s", user.first_name, update.message.text)
    update.message.reply_text(
        'Please enter your mobile contact number:'
    )

    return CONTACTNO_MOBILE

def contactno_mobile(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    contactinfo["contactno_mobile"] = update.message.text
    logger.info("User <%s> Mobile number: %s", user.first_name, update.message.text)
    update.message.reply_text(
        "Please enter your home contact number, or NA if you don't have one:",
        reply_markup=ReplyKeyboardRemove(),
    )

    return CONTACTNO_HOME

def contactno_home(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    contactinfo["contactno_home"] = update.message.text
    logger.info("User <%s> Home number: %s", user.first_name, update.message.text)
    update.message.reply_text(
        "Please enter your primary address in the format: '<block number and street name>, <unit number if applicable>, <postal code>'\n(e.g. 61 Victoria Street, #01-01, S188065):",
        reply_markup=ReplyKeyboardRemove(),
    )

    return ADDRESS

def address(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    contactinfo["address"] = update.message.text
    logger.info("User <%s> Address: %s", user.first_name, update.message.text)
    update.message.reply_text("Please check if your information entered is correct.\n\n" + editcontactinfo_message(), reply_markup=ReplyKeyboardRemove())


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

def edit_contact_entry(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    data = db.child("Users").child(user.id).child("Personal Particulars").child("Contact").get().val()
    contactinfo["email_smu"] = data["email_smu"]
    contactinfo["email_personal"] = data["email_personal"]
    contactinfo["contactno_mobile"] = data["contactno_mobile"]
    contactinfo["contactno_home"] = data["contactno_home"]
    contactinfo["address"] = data["address"]
    logger.info("User <%s> Contact data received.", user.first_name)
    update.message.reply_text(editcontactinfo_message(), reply_markup=ReplyKeyboardRemove())

    return EDIT


def edit_email_smu_start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Please enter your SMU email address:',
    )

    return EDIT_EMAIL_SMU_END

def edit_email_smu_end(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    if not re.search(smu_email_validator, update.message.text):
        logger.info(False)
        update.message.reply_text("Please enter a vaild SMU email address (e.g. johntan.2020@sis.smu.edu.sg):")
        return EDIT_EMAIL_SMU_END
    contactinfo["email_smu"] = update.message.text
    logger.info("User <%s> edited their SMU Email to: %s", user.first_name, update.message.text)
    update.message.reply_text(editcontactinfo_message(), reply_markup=ReplyKeyboardRemove())
    
    return EDIT


def edit_email_personal_start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Please enter your personal email address:',
    )

    return EDIT_EMAIL_PERSONAL_END

def edit_email_personal_end(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    if not re.search(personal_email_validator, update.message.text):
        logger.info(False)
        update.message.reply_text("Please enter a vaild email address (e.g. johntan@gmail.com):")
        return EDIT_EMAIL_PERSONAL_END
    contactinfo["email_personal"] = update.message.text
    logger.info("User <%s> edited their Personal Email to: %s", user.first_name, update.message.text)
    update.message.reply_text(editcontactinfo_message(), reply_markup=ReplyKeyboardRemove())
    
    return EDIT


def edit_contactno_mobile_start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Please enter your mobile number:',
    )

    return EDIT_CONTACTNO_MOBILE_END

def edit_contactno_mobile_end(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    contactinfo["contactno_mobile"] = update.message.text
    logger.info("User <%s> edited their mobile number to: %s", user.first_name, update.message.text)
    update.message.reply_text(editcontactinfo_message(), reply_markup=ReplyKeyboardRemove())
    
    return EDIT


def edit_contactno_home_start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Please enter your home number:',
    )

    return EDIT_CONTACTNO_HOME_END

def edit_contactno_home_end(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    contactinfo["contactno_home"] = update.message.text
    logger.info("User <%s> edited their home number to: %s", user.first_name, update.message.text)
    update.message.reply_text(editcontactinfo_message(), reply_markup=ReplyKeyboardRemove())
    
    return EDIT


def edit_address_start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        "Please enter your primary address in the format: '<block number and street name>, <unit number if applicable>, <postal code>'\n(e.g. 61 Victoria Street, #01-01, S188065):",
    )

    return EDIT_ADDRESS_END

def edit_address_end(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    contactinfo["address"] = update.message.text
    logger.info("User <%s> edited their address to: %s", user.first_name, update.message.text)
    update.message.reply_text(editcontactinfo_message(), reply_markup=ReplyKeyboardRemove())
    
    return EDIT


def editcontactinfo_message() ->str:
    output = "Click the fields below to edit or /done if everything is correct.\n"
    output += f"/SMU_Email: {contactinfo['email_smu']}\n"
    output += f"/Personal_Email: {contactinfo['email_personal']}\n"
    output += f"/Mobile_Number: {contactinfo['contactno_mobile']}\n"
    output += f"/Home_Number: {contactinfo['contactno_home']}\n"
    output += f"/Address: {contactinfo['address']}\n"
    
    return output

def contact_done(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user

    info = db.child("Users").child(user.id).child("Personal Particulars").child("Medical").get().val()
    
    #temporary manual return button to my_profile
    #is there a way to automatically call my_profile? for streamlining considerations
    keyboard = [[InlineKeyboardButton("Back", callback_data="callback_my_profile"),]]
    if info: #check if existing user
        update.message.reply_text(
            "Contact information updated.",
            reply_markup=InlineKeyboardMarkup(keyboard), #temp manual return
        )
    else: #new user
        #segue into medical information for first time user
        keyboard = [[InlineKeyboardButton("Continue", callback_data="callback_medical_new")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            "The following section requires your medical details.",
            reply_markup=reply_markup,
        )

    #database push!
    db.child("Users").child(user.id).child("Personal Particulars").child("Contact").set(contactinfo)
    logger.info("User <%s> confirmed their Contact details. Uploaded to database.", user.first_name)
    #database done pushing

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

contact_conv = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(contact, pattern="callback_contact_new"),
        CommandHandler('edit_contact', edit_contact_entry),
        # CommandHandler('ct', test), #enable to test
    ],
    states={
        EMAIL_SMU: [MessageHandler(Filters.text & ~Filters.command, email_smu)],
        EMAIL_PERSONAL: [MessageHandler(Filters.text & ~Filters.command, email_personal)],
        CONTACTNO_MOBILE: [MessageHandler(Filters.text & ~Filters.command, contactno_mobile)],
        CONTACTNO_HOME: [MessageHandler(Filters.text & ~Filters.command, contactno_home)],
        ADDRESS: [MessageHandler(Filters.text & ~Filters.command, address)],
        EDIT: [
            CommandHandler('done', contact_done),
            CommandHandler('SMU_Email', edit_email_smu_start),
            CommandHandler('Personal_Email', edit_email_personal_start),
            CommandHandler('Mobile_Number', edit_contactno_mobile_start),
            CommandHandler('Home_Number', edit_contactno_home_start),
            CommandHandler('Address', edit_address_start),
        ],
        EDIT_EMAIL_SMU_END: [MessageHandler(Filters.text & ~Filters.command, edit_email_smu_end)],
        EDIT_EMAIL_PERSONAL_END: [MessageHandler(Filters.text & ~Filters.command, edit_email_personal_end)],
        EDIT_CONTACTNO_MOBILE_END: [MessageHandler(Filters.text & ~Filters.command, edit_contactno_mobile_end)],
        EDIT_CONTACTNO_HOME_END: [MessageHandler(Filters.text & ~Filters.command, edit_contactno_home_end)],
        EDIT_ADDRESS_END: [MessageHandler(Filters.text & ~Filters.command, edit_address_end)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)