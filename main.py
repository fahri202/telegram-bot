import logging
import time
from collections import defaultdict
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = "8368213838:AAG0ZyBfJwlYJm2ov0WmCqooRsDMJKkVoPU"

logging.basicConfig(level=logging.INFO)

user_warnings = defaultdict(int)
user_messages = defaultdict(list)

BAD_WORDS = ["anjing", "babi"]

async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        await update.message.reply_text(
            f"👋 Selamat datang {member.first_name}!\n🚫 Jangan spam ya!"
        )

async def anti_spam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    chat_id = update.message.chat.id
    text = update.message.text.lower() if update.message.text else ""

    if "http" in text or "t.me" in text:
        await update.message.delete()
        await warn_user(update, context, user_id, chat_id, "🚫 Dilarang kirim link!")
        return

    for word in BAD_WORDS:
        if word in text:
            await update.message.delete()
            await warn_user(update, context, user_id, chat_id, "⚠️ Jangan berkata kasar!")
            return

    current_time = time.time()
    user_messages[user_id].append(current_time)

    user_messages[user_id] = [
        msg_time for msg_time in user_messages[user_id]
        if current_time - msg_time < 5
    ]

    if len(user_messages[user_id]) > 5:
        await update.message.delete()
        await warn_user(update, context, user_id, chat_id, "🚫 Jangan spam pesan!")
        return

async def warn_user(update, context, user_id, chat_id, reason):
    user_warnings[user_id] += 1
    warning_count = user_warnings[user_id]

    await context.bot.send_message(
        chat_id=chat_id,
        text=f"{reason}\n⚠️ Warning {warning_count}/3"
    )

    if warning_count >= 3:
        await context.bot.restrict_chat_member(
            chat_id,
            user_id,
            permissions=None,
            until_date=int(time.time()) + 60
        )
        await context.bot.send_message(
            chat_id=chat_id,
            text="🔇 Kamu dimute 1 menit!"
        )
        user_warnings[user_id] = 0

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, anti_spam))

print("Bot is running...")
app.run_polling()
