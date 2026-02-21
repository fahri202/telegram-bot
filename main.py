import telebot

TOKEN = "8368213838:AAG0ZyBfJwlYJm2ov0WmCqooRsDMJKkVoPU"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Halo! Bot kamu sudah online 🚀")

@bot.message_handler(func=lambda message: True)
def echo(message):
    bot.reply_to(message, "Kamu bilang: " + message.text)

print("Bot berjalan...")
bot.infinity_polling()
