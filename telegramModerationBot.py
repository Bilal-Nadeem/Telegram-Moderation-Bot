import telegram
from telegram import Update
from telegram.ext import Updater, CallbackContext, MessageHandler, Filters
import datetime
import pytz

# Initialize bot, dispatcher, job queue, and limits
updater = Updater("Token", use_context=True)
dispatcher = updater.dispatcher
job_queue = updater.job_queue

USER_LIMIT = 2
TOTAL_MESSAGE_LIMIT = 100
RUN_ONCE = False
total_messages_sent = 0
users = {}
whitelist = []

# Reset daily limits and unlock group and users
def daily_handler(context):
    global total_messages_sent, users
    total_messages_sent = 0
    unlock_group(context.job.context)
    for user_id in users.keys():
        unlock_user(context.job.context, context, user_id)
    users = {}

def schedule_daily_reset(update, context):
    job_queue.run_daily(
        daily_handler, 
        datetime.time(11, tzinfo=pytz.timezone('Asia/Dubai')), 
        days=(0, 1, 2, 3, 4, 5, 6), 
        context=update
    )

# Permissions for locking and unlocking group or users
def lock_perm():
    return telegram.ChatPermissions(can_send_messages=False)

def unlock_perm():
    return telegram.ChatPermissions(can_send_messages=True)

# Group control functions
def lock_group(update):
    update.effective_chat.set_permissions(lock_perm())

def unlock_group(update):
    try:
        update.effective_chat.set_permissions(unlock_perm())
    except:
        pass

# User control functions
def lock_user(update, context):
    context.bot.restrict_chat_member(
        chat_id=update.effective_chat.id, 
        user_id=update.effective_user.id, 
        permissions=lock_perm()
    )

def unlock_user(update, context, user_id=None):
    try:
        uid = user_id or update.effective_user.id
        context.bot.restrict_chat_member(
            chat_id=update.effective_chat.id, 
            user_id=uid, 
            permissions=unlock_perm()
        )
    except:
        pass

# Welcome new members
def welcome(update: Update, context: CallbackContext):
    for member in update.message.new_chat_members:
        msg = f"Hi {member.full_name},\nID: {member.id}\nWelcome to the server\n[Subscribe](https://youtube.com)&[Follow](https://instagram.com)"
        context.bot.send_message(update.message.chat_id, text=msg, parse_mode=telegram.ParseMode.MARKDOWN)

# Process each incoming message
def handle_message(update: Update, context: CallbackContext):
    global total_messages_sent, RUN_ONCE, users

    user_id = update.effective_user.id
    member = context.bot.get_chat_member(update.effective_chat.id, user_id)
    
    if member.status in ["creator", "administrator"]:
        process_admin_commands(update, context)
    elif update.message.text.startswith(("https://", "http://")):
        handle_link_message(update, context)
    else:
        context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.effective_message.message_id)

def process_admin_commands(update, context):
    global total_messages_sent, users

    msg_text = update.message.text
    if msg_text == "/lock all":
        lock_group(update)
    elif msg_text == "/unlock all":
        reset_locks(update, context)
    elif msg_text.startswith("/whitelist"):
        manage_whitelist(update, context, add=True)
    elif msg_text.startswith("/rmwhitelist"):
        manage_whitelist(update, context, add=False)

def manage_whitelist(update, context, add=True):
    link = update.message.text.split(maxsplit=1)[-1]
    if link[-1] != "/":
        link += "/"
    
    if add:
        whitelist.append(link)
        context.bot.send_message(update.message.chat_id, text=f"Added {link} to whitelist.")
    else:
        whitelist.remove(link)
        context.bot.send_message(update.message.chat_id, text=f"Removed {link} from whitelist.")

def reset_locks(update, context):
    global total_messages_sent, users
    total_messages_sent = 0
    unlock_group(update)
    for user_id in users.keys():
        unlock_user(update, context, user_id)
    users = {}

# Handle links and apply group/user limits
def handle_link_message(update, context):
    global total_messages_sent, RUN_ONCE, users

    link = extract_base_url(update.message.text)
    
    if link in whitelist:
        if not RUN_ONCE:
            schedule_daily_reset(update, context)
            RUN_ONCE = True

        total_messages_sent += 1

        if total_messages_sent >= TOTAL_MESSAGE_LIMIT:
            lock_group(update)

        users[user_id] = users.get(user_id, 0) + 1
        if users[user_id] >= USER_LIMIT:
            lock_user(update, context)
    else:
        context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.effective_message.message_id)

def extract_base_url(link):
    return "/".join(link.split("/")[:3]) + "/"

# Register handlers
dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome))
dispatcher.add_handler(MessageHandler(Filters.text | Filters.command, handle_message))

# Start polling
updater.start_polling()
updater.idle()