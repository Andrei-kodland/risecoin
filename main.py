import telebot
import json
import os

# Bot Token and Channel Username
BOT_TOKEN = "7987098857:AAH_nwOlbdn5Sq3VsEML0UqTEAKQyQfEnqE"  # Replace with your actual bot token
CHANNEL_USERNAME = "@risecoinblum"  # Replace with your actual channel username

USER_DATA_FILE = 'user_data.json'
bot = telebot.TeleBot(BOT_TOKEN)

# Function to load user data from the file
def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as file:
            return json.load(file)
    return {}

# Function to save user data to the file
def save_user_data(user_data):
    try:
        with open(USER_DATA_FILE, 'w') as file:
            json.dump(user_data, file, indent=4)
    except Exception as e:
        print(f"Error saving user data: {e}")

# Function to create the main menu
def main_menu(user_id, language):
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    
    if language == "en":
        btn1 = telebot.types.InlineKeyboardButton("📜 Plans", callback_data="plans")
        btn2 = telebot.types.InlineKeyboardButton("📅 Release Date", callback_data="release_date")
        btn3 = telebot.types.InlineKeyboardButton("🛒 Buy Token", callback_data="buy_token")
        btn4 = telebot.types.InlineKeyboardButton("🌍 Website", url="https://i.redd.it/ceetrhas51441.jpg")
        btn5 = telebot.types.InlineKeyboardButton("🌐 Change Language", callback_data="change_language")
        btn6 = telebot.types.InlineKeyboardButton("🎯 My Referral Link", callback_data="get_referral_link")
        btn7 = telebot.types.InlineKeyboardButton("📊 My Stat", callback_data="my_stat")
    else:  # Russian
        btn1 = telebot.types.InlineKeyboardButton("📜 Планы", callback_data="plans")
        btn2 = telebot.types.InlineKeyboardButton("📅 Дата Выпуска", callback_data="release_date")
        btn3 = telebot.types.InlineKeyboardButton("🛒 Покупка Токена", callback_data="buy_token")
        btn4 = telebot.types.InlineKeyboardButton("🌍 Сайт", url="https://i.redd.it/ceetrhas51441.jpg")
        btn5 = telebot.types.InlineKeyboardButton("🌐 Изменить Язык", callback_data="change_language")
        btn6 = telebot.types.InlineKeyboardButton("🎯 Моя Реферальная Ссылка", callback_data="get_referral_link")
        btn7 = telebot.types.InlineKeyboardButton("📊 Моя Статистика", callback_data="my_stat")

    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    markup.add(btn5, btn6)
    markup.add(btn7)
    return markup

# Function to create the language selection menu
def language_selection_menu():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("English", "Русский")
    return markup

# Handle '/start' command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_data = load_user_data()
    user_id = str(message.chat.id)

    # Extract referrer ID if present in the command
    referrer_id = None
    if len(message.text.split()) > 1:
        referrer_id = message.text.split()[1]

    # Initialize user data if not present
    if user_id not in user_data:
        user_data[user_id] = {'referred_by': referrer_id, 'referral_count': 0, 'language': None}

    # If user was referred, update referrer's referral count
    if referrer_id and referrer_id in user_data:
        user_data[referrer_id]['referral_count'] += 1
        save_user_data(user_data)

    # If no language is selected, ask user to choose
    if user_data[user_id]['language'] is None:
        bot.send_message(message.chat.id, "Please select your language ⬇️/ Пожалуйста, выберите язык ⬇️", reply_markup=language_selection_menu())
    else:
        language = user_data[user_id]['language']
        welcome_message = (
            "Welcome! My name is RiseCoin Bot 🤖! My goal is to help my creators in promoting our coin 🚀 Choose the information that interests you ⬇️:"
            if language == "en" else
            "Добро Пожаловать! Меня зовут RiseCoin Bot 🤖! Моя цель - помочь создателям в продвижении монеты 🚀 Выберите команду которая вас интересует ⬇️:"
        )
        bot.send_message(message.chat.id, welcome_message, reply_markup=main_menu(user_id, language))

    save_user_data(user_data)

# Handle language selection
@bot.message_handler(func=lambda message: message.text in ["English", "Русский"])
def set_language(message):
    user_data = load_user_data()
    user_id = str(message.chat.id)

    user_data[user_id]['language'] = "en" if message.text == "English" else "ru"
    save_user_data(user_data)

    language = user_data[user_id]['language']
    welcome_message = (
        "Welcome! My name is RiseCoin Bot 🤖! My goal is to help my creators in promoting our coin 🚀 Choose the information that interests you ⬇️:"
        if language == "en" else
        "Добро Пожаловать! Меня зовут RiseCoin Bot 🤖! Моя цель - помочь создателям в продвижении монеты 🚀 Выберите команду которая вас интересует ⬇️:"
    )

    bot.send_message(message.chat.id, welcome_message, reply_markup=main_menu(user_id, language))

# Handle referral link request
@bot.callback_query_handler(func=lambda call: call.data == "get_referral_link")
def get_referral_link(call):
    user_id = str(call.message.chat.id)
    referral_link = f"https://t.me/risecoinblum?start={user_id}"
    bot.send_message(call.message.chat.id, f"🎯 Share your referral link: {referral_link}")

# Handle user statistics
@bot.callback_query_handler(func=lambda call: call.data == "my_stat")
def my_stat(call):
    user_data = load_user_data()
    user_id = str(call.message.chat.id)
    referral_count = user_data.get(user_id, {}).get('referral_count', 0)
    bot.send_message(call.message.chat.id, f"📊 You have invited {referral_count} people!")

# Handle button clicks
@bot.callback_query_handler(func=lambda call: call.data in ["plans", "release_date", "buy_token"])
def callback_query(call):
    language = load_user_data().get(str(call.message.chat.id), {}).get('language', 'en')

    responses = {
        "plans": ("📜 Our plans are to innovate in the crypto space.", "📜 Наши планы - инновации в криптопространстве."),
        "release_date": ("📅 The release date will be announced soon!", "📅 Дата выпуска будет объявлена скоро!"),
        "buy_token": ("🛒 To buy, follow these steps:\n1️⃣ Create a wallet\n2️⃣ Buy tokens\n3️⃣ Hold & trade!", "🛒 Для покупки выполните следующие шаги:\n1️⃣ Создайте кошелек\n2️⃣ Купите токены\n3️⃣ Держите и торгуйте!")
    }

    bot.send_message(call.message.chat.id, responses[call.data][0] if language == "en" else responses[call.data][1])

# Start polling
if __name__ == "__main__":
    print("Bot is running...")
    bot.polling(none_stop=True)























  







































