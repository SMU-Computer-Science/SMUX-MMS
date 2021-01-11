from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from database import db

#Main Menu
# def main_menu(update, context):
#     query = update.callback_query
#     query.answer()
#     context.bot.send_message(chat_id=update.effective_chat.id, text=main_menu_message(),reply_markup=main_menu_keyboard())

def main_menu(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=main_menu_message(),reply_markup=main_menu_keyboard())

def cmd_menu(update, context):
    update.message.reply_text(main_menu_message(),reply_markup=main_menu_keyboard())

def main_menu_keyboard():
    keyboard = [
        [
        InlineKeyboardButton("Actvities", callback_data="callback_activities"),
        InlineKeyboardButton("Events", callback_data="callback_events"),
        ],
        [
        InlineKeyboardButton("My Schedule", callback_data="callback_schedule"),
        ],
        [
        InlineKeyboardButton("My Profile", callback_data="callback_my_profile"),
        InlineKeyboardButton("More", callback_data="callback_more_menu"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def main_menu_message():
    return 'Main Menu'

#More Menu
# def qr_more_menu(update, context):
#     query = update.callback_query
#     query.answer()
#     context.bot.send_message(chat_id=update.effective_chat.id, text=more_menu_message(),reply_markup=more_menu_keyboard())

def more_menu(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=more_menu_message(), reply_markup=more_menu_keyboard())

def more_menu_keyboard():
    keyboard = [[InlineKeyboardButton("FAQ", callback_data='callback_faq')],
    [InlineKeyboardButton("Back", callback_data='callback_main_menu'),
    InlineKeyboardButton("Credits", callback_data='callback_credits'),
    InlineKeyboardButton("PDPA", callback_data='callback_pdpa')]]
    return InlineKeyboardMarkup(keyboard)

def more_menu_message():
    return 'More Menu'


#FAQ
def faq(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text='<FAQ>', reply_markup=back_to_more_menu_button())


#Credits
def credits(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text='Copyright ©️ Kuehbies 2020 \n\n@kuehbies_contactus.', reply_markup=back_to_more_menu_button())

#PDPA
def pdpa_disposable(update, context):
    query = update.callback_query
    query.answer()
    keyboard = [[InlineKeyboardButton("Close", callback_data="callback_delete"),]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id, text=pdpa_text(), reply_markup=reply_markup)

def pdpa(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=pdpa_text(), reply_markup=back_to_more_menu_button())

def back_to_more_menu_button():
    keyboard = [[InlineKeyboardButton("Back", callback_data="callback_more_menu"),]]
    return InlineKeyboardMarkup(keyboard)

def pdpa_text() -> str:
    output = 'By using this bot, you hereby agree that Singapore Management University (SMU) may collect, use and disclose your personal data that you provide to this bot for the purpose of sending you updates for activites and future events by SMU Xtremists (SMUX).\n\n'
    output += 'You also consent to the disclosure of your personal data to SMU partners/affiliates and other third party service providers that SMU may engage from time to time. If you are providing someone else’s personal data or submitting this form on behalf of someone else, you hereby declare that you have obtained consent from the named individual(s) in this form, for the collection, use and disclosure of his/her personal data by you to SMU, SMU business partners and other third party service providers.\n\n'
    output += 'SMU respects the privacy of individuals and recognizes the importance of the personal data you have entrusted to us and believe that it is our responsibility to properly manage, protect, process and disclose your personal data. We will collect, use and disclose your personal data in accordance with the Personal Data Protection Act 2012.\n\n'
    output += 'If you would like to find out more about Personal Data Protection Statement, please view our Privacy Statement at http://www.smu.edu.sg/privacy-statement. Should you wish at any time to withdraw your consent for the collection, use and/or disclosure of your personal data after submitting this form, please contact us at <SMUX EMAIL>.'
    return output

def delete_recent(update, context):
    query = update.callback_query
    query.answer()
    query.delete_message()
