import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import json
import os
import sqlite3
import database  # Import the database functions from the file we just created

# Replace this with your actual bot token from BotFather
BOT_TOKEN = "7987098857:AAH_nwOlbdn5Sq3VsEML0UqTEAKQyQfEnqE"

# Initialize bot
bot = telebot.TeleBot(BOT_TOKEN)

# File to store user data (referral tracking)
USER_DATA_FILE = 'user_data.json'

# Create the database when starting the bot
database.create_db()

# Function to create the menu
def main_menu(user_id):
    markup = InlineKeyboardMarkup(row_width=2)
    
    # Create a referral link for the user
    referral_link = f"https://t.me/risetokenblum?start={user_id}"
    btn1 = InlineKeyboardButton("📜 Планы", callback_data="планы")
    btn2 = InlineKeyboardButton("📅 Дата Выпуска", callback_data="датавыпускамонеты")
    btn3 = InlineKeyboardButton("🛒 Покупка Токена", callback_data="каккупитьмонету?")    
    btn4 = InlineKeyboardButton("🌍 Веб-сайт", url="https://i.redd.it/ceetrhas51441.jpg")  # External link
    btn5 = InlineKeyboardButton(f"🔗 Ваша реферальная ссылка", callback_data="referral_link")
    btn6 = InlineKeyboardButton(f"📊 Моя Статистика", callback_data="referral_count")  # New button for referral stats

    markup.add(btn1, btn2)
    markup.add(btn3, btn4)  # Adding buttons in a new row
    markup.add(btn5, btn6)  # Add referral stats button

    return markup

# Handle '/start' command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = str(message.chat.id)
    
    print(f"User {user_id} started the bot.")  # Debugging line to confirm start
    
    # Initialize the user in the database if it's the first time they use the bot
    database.add_user(user_id)

    # Check if the user was referred by someone else via the referral link
    referrer_id = message.text.split('start=')[1] if 'start=' in message.text else None
    if referrer_id:
        referrer_id = referrer_id.strip()
        print(f"Referral detected. Referrer ID: {referrer_id}")  # Debugging line
        database.update_referral_count(referrer_id)  # Increment the referrer's count
        bot.send_message(message.chat.id, "🎉 Вас пригласили! Спасибо, что присоединились!")

    # Send welcome message with main menu
    bot.send_message(message.chat.id, "Добро Пожаловать! Меня зовут RiseCoin Bot 🤖! Моя цель - помочь создателям в продвижении монеты 🚀 Выберите команду которая вас интересует ⬇️:", reply_markup=main_menu(user_id))

# Handle button clicks
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    user_id = str(call.message.chat.id)

    if call.data == "referral_link":
        referral_link = f"https://t.me/risetokenblum?start={user_id}"
        bot.answer_callback_query(call.id, "📲 Your referral link copied!")
        bot.send_message(call.message.chat.id, f"📲 Your referral link is: {referral_link}")
    elif call.data == "referral_count":
        referral_count = database.get_referral_count(user_id)  # Get referral count from the database
        bot.answer_callback_query(call.id, "📊 Your referral stats selected!")
        bot.send_message(call.message.chat.id, f"📊 You have referred {referral_count} people!")
    else:
        bot.answer_callback_query(call.id, "❗ Unknown action!")

# Start polling (no webhook involved)
if __name__ == "__main__":
    print("Bot is running...")
    bot.polling(none_stop=True)
