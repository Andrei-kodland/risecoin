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
        json.dump(user_data, file, indent=4)
    print("User data saved.")  # Debugging line to confirm saving

# Function to create the menu
def main_menu(user_id):
    markup = InlineKeyboardMarkup(row_width=2)
    
    # Create a referral link for the user
    referral_link = f"https://t.me/risetokenblum?start={user_id}"
    btn1 = InlineKeyboardButton("📜 Планы", callback_data="планы")
    btn2 = InlineKeyboardButton("📅 Дата Выпуска", callback_data="датавыпускамонеты")
    btn3 = InlineKeyboardButton("🛒 Покупка Токена", callback_data="каккупитьмонету?")    
    btn4 = InlineKeyboardButton("🌍 Веб-сайт", url="https://i.redd.it/ceetrhas51441.jpg")  # External link
    btn5 = InlineKeyboardButton("🔗 Ваша реферальная ссылка", callback_data="referral_link")
    btn6 = InlineKeyboardButton(f"📊 Моя Статистика", callback_data="referral_count")  # New button for referral stats

    markup.add(btn1, btn2)
    markup.add(btn3, btn4)  # Adding buttons in a new row
    markup.add(btn5, btn6)  # Add referral stats button

    return markup

# Handle '/start' command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_data = load_user_data()
    user_id = str(message.chat.id)
    
    print(f"User {user_id} started the bot.")  # Debugging line to confirm start

    # Initialize the user if it's the first time they use the bot
    if user_id not in user_data:
        user_data[user_id] = {'referred_by': None, 'referral_count': 0}
        print(f"New user initialized: {user_id}")  # Debugging line
        save_user_data(user_data)

    # Check if the user was referred by someone else via the referral link
    referrer_id = message.text.split('start=')[1] if 'start=' in message.text else None
    if referrer_id:
        referrer_id = referrer_id.strip()
        print(f"Referral detected. Referrer ID: {referrer_id}")  # Debugging line
        if referrer_id in user_data:
            # Referrer found, update referral count and data
            user_data[user_id]['referred_by'] = referrer_id  # Track who referred this user
            user_data[referrer_id]['referral_count'] += 1  # Increment the referrer's count
            print(f"Referrer {referrer_id} referral count updated to {user_data[referrer_id]['referral_count']}")  # Debugging line
            bot.send_message(message.chat.id, "🎉 Вас пригласили! Спасибо, что присоединились!")
        else:
            print(f"Referrer {referrer_id} not found in user data.")

    # Send welcome message with main menu
    bot.send_message(message.chat.id, "Добро Пожаловать! Меня зовут RiseCoin Bot 🤖! Моя цель - помочь создателям в продвижении монеты 🚀 Выберите команду которая вас интересует ⬇️:", reply_markup=main_menu(user_id))
    
    save_user_data(user_data)  # Save user data after checking referrals

# Handle button clicks
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    user_data = load_user_data()
    user_id = str(call.message.chat.id)

    if call.data == "планы":
        bot.answer_callback_query(call.id, "📜 Plans selected!")
        bot.send_message(call.message.chat.id, "📜 Our plans are to innovate in the crypto space.")
    elif call.data == "датавыпускамонеты":
        bot.answer_callback_query(call.id, "📅 Release date selected!")
        bot.send_message(call.message.chat.id, "📅 The release date will be announced soon!")
    elif call.data == "каккупитьмонету?":
        bot.answer_callback_query(call.id, "🛒 Steps to buy selected!")
        bot.send_message(call.message.chat.id, "🛒 To buy, follow these steps:\n1️⃣ Create a wallet\n2️⃣ Buy tokens\n3️⃣ Hold & trade!")
    elif call.data == "referral_link":
        # Generate the referral link for the user
        referral_link = f"https://t.me/risetokenblum?start={user_id}"  # Create referral link here
        print(f"Referral link sent to user: {referral_link}")  # Debugging line
        bot.answer_callback_query(call.id, "📲 Your referral link copied!")
        bot.send_message(call.message.chat.id, f"📲 Your referral link is: {referral_link}")
    elif call.data == "referral_count":
        # Get the referral count for the user
        referral_count = user_data.get(user_id, {}).get('referral_count', 0)
        bot.answer_callback_query(call.id, "📊 Your referral stats selected!")
        bot.send_message(call.message.chat.id, f"📊 You have referred {referral_count} people!")
    else:
        bot.answer_callback_query(call.id, "❗ Unknown action!")

    save_user_data(user_data)  # Ensure the data is saved after each interaction

# Start polling (no webhook involved)
if __name__ == "__main__":
    print("Bot is running...")
    bot.polling(none_stop=True)
