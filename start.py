from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from database import db
import logging

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

#Start
def start(update, context):
    # context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to SMUX's Membership Management System, You may begin accessing your account via /menu. For more information regarding functionalities, please use /faq.")
    user = update.message.from_user
    info = db.child("Users").child(user.id).child("Personal Particulars").get().val()
    if info:
        logger.info("User <%s> logged in.", user.first_name)
        keyboard = [[
            InlineKeyboardButton("Continue", callback_data="callback_main_menu"),
            ]]
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Welcome back, {user.first_name}.")
        context.bot.send_message(chat_id=update.effective_chat.id, text=motd())
        context.bot.send_message(chat_id=update.effective_chat.id, text="You can /menu anytime to bring up the buttons, or /help for other commands.",
        reply_markup=InlineKeyboardMarkup(keyboard),)
    else:
        logger.info("User <%s> First time log in.", user.first_name)
        keyboard = [[
            InlineKeyboardButton("Continue", callback_data="callback_signup"),
            InlineKeyboardButton("View PDPA", callback_data="callback_disposable")
            ]]
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Hello {user.first_name}! Welcome to SMUX's Membership Management System. Before you can use this bot's functionality, please fill in your details.\n\n"
        "By using this bot, you agree to our PDPA clause.",
        reply_markup=InlineKeyboardMarkup(keyboard),
        )

def motd():
    output = db.child("Admin").child("MOTD").get().val()
    return output