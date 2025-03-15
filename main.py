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
    btn1 = InlineKeyboardButton("📜 Планы", callback_data="планы")
    btn2 = InlineKeyboardButton("📅 Дата Выпуска", callback_data="датавыпускамонеты")
    btn3 = InlineKeyboardButton("🛒 Покупка Токена", callback_data="каккупитьмонету?")
    btn4 = InlineKeyboardButton("🌍 Веб-сайт", url="https://i.redd.it/ceetrhas51441.jpg")  # External link
    btn5 = InlineKeyboardButton(f"🔗 Ваша реферальная ссылка", callback_data="реферальная_ссылка")
    btn6 = InlineKeyboardButton(f"📊 Моя Статистика", callback_data="статистика_рефералов")  # New button for referral stats

    markup.add(btn1, btn2)
    markup.add(btn3, btn4)  # Adding buttons in a new row
    markup.add(btn5, btn6)  # Add referral stats button

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

    # Send welcome message with main menu
    bot.send_message(message.chat.id, "Добро Пожаловать! Меня зовут RiseCoin Bot 🤖! Моя цель - помочь создателям в продвижении монеты 🚀 Выберите команду которая вас интересует ⬇️:", reply_markup=main_menu(user_id))

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
    elif call.data == "реферальная_ссылка":
        bot.answer_callback_query(call.id, "📲 Your referral link copied!")
        bot.send_message(call.message.chat.id, f"📲 Your referral link is: https://t.me/risetokenblum?start={user_id}")
    elif call.data == "статистика_рефералов":
        # Get the referral count for the user
        referral_count = user_data.get(user_id, {}).get('referral_count', 0)
        bot.answer_callback_query(call.id, "📊 Your referral stats selected!")
        bot.send_message(call.message.chat.id, f"📊 You have referred {referral_count} people!")
    else:
        bot.answer_callback_query(call.id, "❗ Unknown action!")

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
            user_data[referrer_id]['статистика_рефералов'] += 1
            save_user_data(user_data)

            bot.send_message(message.chat.id, "🎉 Вас пригласили! Спасибо, что присоединились!")

# Start polling (no webhook involved)
if __name__ == "__main__":
    print("Bot is running...")
    bot.polling(none_stop=True)
