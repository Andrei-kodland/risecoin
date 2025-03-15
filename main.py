import telebot
import json
import os

# Bot Token and Channel Username
BOT_TOKEN = "7987098857:AAH_nwOlbdn5Sq3VsEML0UqTEAKQyQfEnqE"
CHANNEL_USERNAME = "@risetokenblum"  # Replace with your channel username

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
        print("User data saved successfully.")  # Debugging line
    except Exception as e:
        print(f"Error saving user data: {e}")  # Debugging line

# Function to create the main menu
def main_menu(user_id, language):
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    if language == "en":
        btn1 = telebot.types.InlineKeyboardButton("📜 Plans", callback_data="plans")
        btn2 = telebot.types.InlineKeyboardButton("📅 Release Date", callback_data="release_date")
        btn3 = telebot.types.InlineKeyboardButton("🛒 Buy Token", callback_data="buy_token")
    else:
        btn1 = telebot.types.InlineKeyboardButton("📜 Планы", callback_data="plans")
        btn2 = telebot.types.InlineKeyboardButton("📅 Дата Выпуска", callback_data="release_date")
        btn3 = telebot.types.InlineKeyboardButton("🛒 Покупка Токена", callback_data="buy_token")

    btn4 = telebot.types.InlineKeyboardButton("🌍 Website", url="https://i.redd.it/ceetrhas51441.jpg")
    btn5 = telebot.types.InlineKeyboardButton("🎯 Referral Link", callback_data="get_referral_link")
    btn6 = telebot.types.InlineKeyboardButton("📊 My Stats", callback_data="my_stat")
    btn7 = telebot.types.InlineKeyboardButton("🌐 Change Language", callback_data="change_language")
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

    # Initialize user data if the user is not in the file
    if user_id not in user_data:
        user_data[user_id] = {'referred_by': None, 'referral_count': 0, 'language': None}

    # Ensure 'language' is initialized for the user
    if 'language' not in user_data[user_id]:
        user_data[user_id]['language'] = None

    # Check if user has already selected a language
    if user_data[user_id]['language'] is None:
        # If no language has been selected, show the language selection menu
        bot.send_message(message.chat.id, "Please select your language ⬇️/ Пожалуйста, выберите язык ⬇️", reply_markup=language_selection_menu())
    else:
        # Proceed with main menu if the language is set
        language = user_data[user_id]['language']
        bot.send_message(message.chat.id, "Welcome! My name is RiseCoin Bot 🤖! My goal is to help my creators in promoting our coin 🚀 Choose the information that interests you ⬇️:", reply_markup=main_menu(user_id, language))

    save_user_data(user_data)  # Ensure the user data is saved

# Handle language selection
@bot.message_handler(func=lambda message: message.text in ["English", "Русский"])
def set_language(message):
    user_data = load_user_data()
    user_id = str(message.chat.id)

    if message.text == "English":
        user_data[user_id]['language'] = "en"
    else:
        user_data[user_id]['language'] = "ru"

    # Save user data after language is set
    save_user_data(user_data)

    # Send main menu after language is set
    bot.send_message(message.chat.id, "Добро Пожаловать! Меня зовут RiseCoin Bot 🤖! Моя цель - помочь создателям в продвижении монеты 🚀 Выберите команду, которая вас интересует ⬇️:", reply_markup=main_menu(user_id, user_data[user_id]['language']))

# Handle referral link generation
@bot.callback_query_handler(func=lambda call: call.data == "get_referral_link")
def get_referral_link(call):
    user_data = load_user_data()
    user_id = str(call.message.chat.id)

    # Generate referral link
    referral_link = f"https://t.me/risetokenblum?start={user_id}"
    language = user_data[user_id]['language']

    if language == "en":
        bot.send_message(call.message.chat.id, f"Your referral link: {referral_link}\nShare it with others to earn referral points!")
    else:
        bot.send_message(call.message.chat.id, f"Ваша реферальная ссылка: {referral_link}\nПоделитесь ею с другими, чтобы зарабатывать реферальные очки!")

# Handle user joining channel through a referral link
@bot.channel_post_handler(content_types=['new_chat_members'])
def handle_new_user_joining(post):
    user_data = load_user_data()

    # Check if user joined the channel through a referral link
    for member in post.new_chat_members:
        user_id = str(member.id)
        referral_id = None

        # Extract the referral ID from the user that invited them (check if it's in the link)
        if member.username:
            referral_id = member.username.split('?start=')[-1]  # Extract referral ID from the link

        if referral_id and referral_id in user_data:
            # Increment referral count of the user who referred
            user_data[referral_id]['referral_count'] += 1
            bot.send_message(user_data[referral_id]['language'], "Congrats! You are a step closer to winning the challenge!")
            save_user_data(user_data)

# Handle showing stats (how many users they referred)
@bot.callback_query_handler(func=lambda call: call.data == "my_stat")
def show_stats(call):
    user_data = load_user_data()
    user_id = str(call.message.chat.id)

    referral_count = user_data[user_id]['referral_count']
    language = user_data[user_id]['language']

    if language == "en":
        bot.send_message(call.message.chat.id, f"You've invited {referral_count} people to the channel! Keep up the great work!")
    else:
        bot.send_message(call.message.chat.id, f"Вы пригласили {referral_count} людей в канал! Продолжайте в том же духе!")

    save_user_data(user_data)  # Save the user data after callback handling

# Handle changing language
@bot.callback_query_handler(func=lambda call: call.data == "change_language")
def change_language(call):
    bot.send_message(call.message.chat.id, "Please select your language ⬇️/ Пожалуйста, выберите язык ⬇️", reply_markup=language_selection_menu())

# Start polling (no webhook involved)
if __name__ == "__main__":
    print("Bot is running...")
    bot.polling(none_stop=True)
























  







































