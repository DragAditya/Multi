import json
import os
import time
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes,
)
from telegram.error import TelegramError
from datetime import datetime, timedelta
from collections import defaultdict

# Editable Variables
OWNER_CHAT_ID = '1183272367'  # Replace with your Telegram user ID
BOT_TOKEN = '6094405994:AAHX0HrV5Mo2q6Zyuuo-Xmk6Pg4GfP0b5Lc'          # Replace with your bot's token
LOG_FILE = "message_log.json"         # File to store logs
USER_RATE_LIMIT = timedelta(minutes=1) # Rate limit period

# Initialize log file
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, 'w') as f:
        json.dump([], f)

# Initialize message mapping and rate limiting
user_message_map = {}
user_last_message_time = defaultdict(datetime)
forwarding_enabled = True

# Function to log messages
def log_message(action, user_id, message):
    timestamp = datetime.now().isoformat()
    with open(LOG_FILE, 'a') as f:
        log_entry = {"timestamp": timestamp, "action": action, "user_id": user_id, "message": message}
        f.write(json.dumps(log_entry) + "\n")

# Function to handle errors
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        raise context.error
    except TelegramError as e:
        print(f"Telegram error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Command to toggle the forwarding feature
async def switch(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global forwarding_enabled
    forwarding_enabled = not forwarding_enabled
    status = "enabled" if forwarding_enabled else "disabled"
    await context.bot.send_message(
        chat_id=OWNER_CHAT_ID, 
        text=f"Forwarding has been {status}."
    )

# Command to check the status of the bot
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    status_message = "Forwarding is currently **enabled**." if forwarding_enabled else "Forwarding is currently **disabled**."
    await context.bot.send_message(chat_id=OWNER_CHAT_ID, text=status_message)

# Command to provide help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = (
        "Available Commands:\n"
        "/switch - Toggle message forwarding on/off\n"
        "/status - Check the current status of the bot\n"
        "/help - Show this help message"
    )
    await context.bot.send_message(chat_id=OWNER_CHAT_ID, text=help_text)

# Function to forward all types of messages
async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global user_last_message_time

    # Check rate limiting
    current_time = datetime.now()
    user_id = update.message.from_user.id
    if user_id in user_last_message_time and (current_time - user_last_message_time[user_id]) < USER_RATE_LIMIT:
        await update.message.reply_text("You are sending messages too quickly. Please wait a moment.")
        return
    
    user_last_message_time[user_id] = current_time

    if forwarding_enabled:
        user = update.message.from_user

        # Forward message based on type
        if update.message.text:
            forwarded_message = await context.bot.send_message(
                chat_id=OWNER_CHAT_ID, 
                text=f"Message from {user.first_name} (@{user.username}): {update.message.text}"
            )
            log_message("forward", user_id, update.message.text)
        elif update.message.photo:
            forwarded_message = await context.bot.send_photo(
                chat_id=OWNER_CHAT_ID, 
                photo=update.message.photo[-1].file_id,
                caption=f"Photo from {user.first_name} (@{user.username})"
            )
            log_message("forward", user_id, "Photo")
        elif update.message.video:
            forwarded_message = await context.bot.send_video(
                chat_id=OWNER_CHAT_ID, 
                video=update.message.video.file_id,
                caption=f"Video from {user.first_name} (@{user.username})"
            )
            log_message("forward", user_id, "Video")
        elif update.message.document:
            forwarded_message = await context.bot.send_document(
                chat_id=OWNER_CHAT_ID, 
                document=update.message.document.file_id,
                caption=f"Document from {user.first_name} (@{user.username})"
            )
            log_message("forward", user_id, "Document")
        elif update.message.voice:
            forwarded_message = await context.bot.send_voice(
                chat_id=OWNER_CHAT_ID, 
                voice=update.message.voice.file_id,
                caption=f"Voice message from {user.first_name} (@{user.username})"
            )
            log_message("forward", user_id, "Voice")
        elif update.message.audio:
            forwarded_message = await context.bot.send_audio(
                chat_id=OWNER_CHAT_ID, 
                audio=update.message.audio.file_id,
                caption=f"Audio message from {user.first_name} (@{user.username})"
            )
            log_message("forward", user_id, "Audio")
        else:
            await context.bot.send_message(
                chat_id=OWNER_CHAT_ID, 
                text=f"Unsupported message type from {user.first_name} (@{user.username})."
            )
            return

        # Map forwarded message to the original user for replies
        user_message_map[forwarded_message.message_id] = user.id

    else:
        await update.message.reply_text("The forwarding feature is currently disabled.")

# Function to handle replies and send them back to the original user
async def reply_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Check if this message is a reply to a forwarded message
    if update.message.reply_to_message and forwarding_enabled:
        original_message_id = update.message.reply_to_message.message_id

        if original_message_id in user_message_map:
            user_id = user_message_map[original_message_id]

            # Send the reply back to the original user
            await context.bot.send_message(chat_id=user_id, text=update.message.text)
            log_message("reply", user_id, update.message.text)
        else:
            await update.message.reply_text("Cannot find the user to send this reply.")
    else:
        await update.message.reply_text("The forwarding feature is disabled or this is not a reply to a forwarded message.")

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Handlers
    app.add_handler(MessageHandler(filters.ALL & (~filters.COMMAND), forward_message))
    app.add_handler(MessageHandler(filters.REPLY, reply_message))
    app.add_handler(CommandHandler("switch", switch))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(lambda update, context: None))
    app.add_error_handler(error_handler)

    while True:
        try:
            await app.run_polling()
            break  # Exit loop if polling stops successfully
        except (TelegramError, Exception) as e:
            print(f"Error occurred: {e}")
            await asyncio.sleep(5)  # Wait before retrying

# Run the main function to start the bot
if __name__ == "__main__":
    asyncio.run(main())
