
import logging
from database import db
from typing import Dict

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


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

NAME, HPNUM, RELATIONSHIP, EDIT, EDIT_NAME_END, EDIT_HPNUM_END, EDIT_RELATIONSHIP_END = range(7)

nokinfo = {
    "name" : "",
    "hpnum" : "",
    "relationship" : "",
}


def nok(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    context.bot.send_message(
        text='NOK Name:',chat_id=update.effective_chat.id,
        reply_markup=ReplyKeyboardRemove()
    )

    return NAME

def nok_name(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    nokinfo["name"] = update.message.text
    logger.info("User <%s> NOK name: %s", user.first_name, update.message.text)
    update.message.reply_text(
        'NOK Contact Number (e.g 91234567):',
        reply_markup=ReplyKeyboardRemove()
        )

    return HPNUM

def nok_hpnum(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    nokinfo["hpnum"] = update.message.text
    logger.info("User <%s> NOK contact number: %s", user.first_name, update.message.text)
    update.message.reply_text(
        'Relationship of NOK (e.g. Father, Mother):',
        reply_markup=ReplyKeyboardRemove()
    )

    return RELATIONSHIP

def nok_relationship(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    nokinfo["relationship"] = update.message.text
    logger.info("User <%s> NOK relationship: %s", user.first_name, update.message.text)
    update.message.reply_text(editnokinfo_message(), reply_markup=ReplyKeyboardRemove())

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

def edit_nok_entry(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    data = db.child("Users").child(user.id).child("Personal Particulars").child("NOK").get().val()
    nokinfo["name"] = data["name"]
    nokinfo["hpnum"] = data["hpnum"]
    nokinfo["relationship"] = data["relationship"]
    logger.info("User <%s> NOK data received.", user.first_name)
    update.message.reply_text(editnokinfo_message(), reply_markup=ReplyKeyboardRemove())

    return EDIT

def edit_nok_name_start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'NOK Name:',
    )

    return EDIT_NAME_END

def edit_nok_name_end(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    nokinfo["name"] = update.message.text
    logger.info("User <%s> edited their NOK name to: %s", user.first_name, update.message.text)
    update.message.reply_text(editnokinfo_message(), reply_markup=ReplyKeyboardRemove())
    
    return EDIT

def edit_nok_hpnum_start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'NOK Contact Number (e.g 91234567):',
        reply_markup=ReplyKeyboardRemove(),
    )

    return EDIT_HPNUM_END

def edit_nok_hpnum_end(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    nokinfo["hpnum"] = update.message.text
    logger.info("User <%s> edited their NOK contact number to: %s", user.first_name, update.message.text)
    update.message.reply_text(editnokinfo_message(), reply_markup=ReplyKeyboardRemove())
    
    return EDIT

def edit_nok_relationship_start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Relationship of NOK (e.g. Father, Mother):',
        reply_markup=ReplyKeyboardRemove(),
    )

    return EDIT_RELATIONSHIP_END

def edit_nok_relationship_end(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    nokinfo["relationship"] = update.message.text
    logger.info("User <%s> edited their NOK relationship to: %s", user.first_name, update.message.text)
    update.message.reply_text(editnokinfo_message(), reply_markup=ReplyKeyboardRemove())
    
    return EDIT

def editnokinfo_message() ->str:
    output = "Click the fields below to edit or /done if everything is correct.\n"
    output += f"/Name: {nokinfo['name']}\n"
    output += f"/HP_Number: {nokinfo['hpnum']}\n"
    output += f"/Relationship: {nokinfo['relationship']}\n"
    
    return output

def nok_done(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user

    info = db.child("Users").child(user.id).child("Personal Particulars").child("Personal").child("registration_complete").get().val()
    
    #temporary manual return button to my_profile
    #is there a way to automatically call my_profile?
    keyboard = [[InlineKeyboardButton("Back", callback_data="callback_my_profile"),]]
    if info: #check if existing user
        update.message.reply_text(
            "NOK Information updated.",
            reply_markup=InlineKeyboardMarkup(keyboard), #temp manual return
        )
    else: #new user
        #registration complete message
        keyboard = [[InlineKeyboardButton("Hooray!", callback_data="callback_main_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            "Congratulations! Registration complete!",
            reply_markup=reply_markup,
        )
    
    #database push!
    data_db_new = {
        "name" : nokinfo["name"],
        "hpnum" : nokinfo["hpnum"],
        "relationship" : nokinfo["relationship"],
    }

    db.child("Users").child(user.id).child("Personal Particulars").child("NOK").set(data_db_new)
    logger.info("User <%s> confirmed their NOK details. Uploaded to database.", user.first_name)
    #database done pushing

    #Mark registration complete
    db.child("Users").child(user.id).child("Personal Particulars").child("Personal").child("registration_complete").set("done")

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

nok_conv = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(nok, pattern="callback_noknew"),
        CommandHandler('edit_nok', edit_nok_entry),
        # CommandHandler('nok', nok), #enable to test
    ],
    states={
        NAME: [MessageHandler(Filters.text & ~Filters.command, nok_name)],
        HPNUM: [MessageHandler(Filters.text & ~Filters.command, nok_hpnum)],
        RELATIONSHIP: [MessageHandler(Filters.text & ~Filters.command, nok_relationship)],
        EDIT: [
            CommandHandler('done', nok_done),
            CommandHandler('Name', edit_nok_name_start),
            CommandHandler('HP_Number', edit_nok_hpnum_start),
            CommandHandler('Relationship', edit_nok_relationship_start),
        ],
        EDIT_NAME_END: [MessageHandler(Filters.text & ~Filters.command, edit_nok_name_end)],
        EDIT_HPNUM_END: [MessageHandler(Filters.text & ~Filters.command, edit_nok_hpnum_end)],
        EDIT_RELATIONSHIP_END: [MessageHandler(Filters.text & ~Filters.command, edit_nok_relationship_end)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)