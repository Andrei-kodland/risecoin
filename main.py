import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import json
import os

# Replace this with your actual bot token from BotFather
BOT_TOKEN = "7987098857:AAH_nwOlbdn5Sq3VsEML0UqTEAKQyQfEnqE"

# Initialize bot
bot = telebot.TeleBot(BOT_TOKEN)

# File to store user data (referral tracking)
USER_DATA_FILE = 'user_data.json'

# Function to load user data from the file
def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as file:
            return json.load(file)
    return {}

# Function to save user data to the file
def save_user_data(user_data):
    with open(USER_DATA_FILE, 'w') as file:
        json.dump(user_data, file)

# Function to create the menu
def main_menu(user_id):
    markup = InlineKeyboardMarkup(row_width=2)
    
    # Create a referral link for the user
    referral_link = f"https://t.me/risetokenblum?start={user_id}"
    btn1 = InlineKeyboardButton("📜 Plans", callback_data="plans")
    btn2 = InlineKeyboardButton("📅 Release Date", callback_data="releasedate")
    btn3 = InlineKeyboardButton("🛒 Steps to Buy", callback_data="stepstobuy")
    btn4 = InlineKeyboardButton("🌍 Website", url="https://i.redd.it/ceetrhas51441.jpg")  # External link
    btn5 = InlineKeyboardButton(f"🔗 Your Referral Link: {referral_link}", callback_data="referral_link")

    markup.add(btn1, btn2)
    markup.add(btn3, btn4)  # Adding buttons in a new row
    markup.add(btn5)

    return markup

# Handle '/start' command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_data = load_user_data()
    user_id = str(message.chat.id)

    # Initialize the user if it's the first time they use the bot
    if user_id not in user_data:
        user_data[user_id] = {'referred_by': None, 'referral_count': 0}
        save_user_data(user_data)
    
    bot.send_message(message.chat.id, "Добро Пожаловать! Меня зовут RiseCoin Bot 🤖! Моя цель - помочь создателям в продвижении монеты 🚀 Выберите команду которая вас интересует ⬇️:", reply_markup=main_menu(user_id))

# Handle button clicks
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    user_data = load_user_data()
    user_id = str(call.message.chat.id)

    if call.data == "plans":
        bot.answer_callback_query(call.id, "📜 Plans selected!")
        bot.send_message(call.message.chat.id, "📜 Our plans are to innovate in the crypto space.")
    elif call.data == "releasedate":
        bot.answer_callback_query(call.id, "📅 Release date selected!")
        bot.send_message(call.message.chat.id, "📅 The release date will be announced soon!")
    elif call.data == "stepstobuy":
        bot.answer_callback_query(call.id, "🛒 Steps to buy selected!")
        bot.send_message(call.message.chat.id, "🛒 To buy, follow these steps:\n1️⃣ Create a wallet\n2️⃣ Buy tokens\n3️⃣ Hold & trade!")
    elif call.data == "referral_link":
        bot.answer_callback_query(call.id, "📲 Your referral link copied!")
        bot.send_message(call.message.chat.id, f"📲 Your referral link is: https://t.me/risetokenblum?start={user_id}")
    
    save_user_data(user_data)

# Handle users joining from a referral link
@bot.message_handler(commands=['start'])
def handle_referral(message):
    user_data = load_user_data()
    referrer_id = message.text.split('start=')[1] if 'start=' in message.text else None

    if referrer_id:
        referrer_id = referrer_id.strip()
        if referrer_id in user_data:
            # Increment the referral count for the referrer
            user_data[referrer_id]['referral_count'] += 1
            save_user_data(user_data)

            bot.send_message(message.chat.id, "🎉 You were invited by someone! Thank you for joining!")

# Start polling
if __name__ == "__main__":
    print("Bot is running...")
    bot.polling(none_stop=True)











# Start the bot
bot.polling(none_stop=True)
