import telebot
import json
import os

# Bot Token and Channel Username
BOT_TOKEN = "7987098857:AAH_nwOlbdn5Sq3VsEML0UqTEAKQyQfEnqE"  # Replace with your bot token
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

# Function to create the main menu with a referral link option
def main_menu(user_id, language):
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    
    # Displaying different buttons based on the language selected
    if language == "en":
        btn1 = telebot.types.InlineKeyboardButton("📜 Plans", callback_data="plans")
        btn2 = telebot.types.InlineKeyboardButton("📅 Release Date", callback_data="release_date")
        btn3 = telebot.types.InlineKeyboardButton("🛒 Buy Token", callback_data="buy_token")
        btn4 = telebot.types.InlineKeyboardButton("🌍 Website", url="https://i.redd.it/ceetrhas51441.jpg")
        btn5 = telebot.types.InlineKeyboardButton("🌐 Change Language", callback_data="change_language")
        btn6 = telebot.types.InlineKeyboardButton("🎯 My Referral Link", callback_data="get_referral_link")
        btn7 = telebot.types.InlineKeyboardButton("📊 My Stat", callback_data="my_stat")  # New button for My Stat
    else:  # Russian
        btn1 = telebot.types.InlineKeyboardButton("📜 Планы", callback_data="plans")
        btn2 = telebot.types.InlineKeyboardButton("📅 Дата Выпуска", callback_data="release_date")
        btn3 = telebot.types.InlineKeyboardButton("🛒 Покупка Токена", callback_data="buy_token")
        btn4 = telebot.types.InlineKeyboardButton("🌍 Сайт", url="https://i.redd.it/ceetrhas51441.jpg")
        btn5 = telebot.types.InlineKeyboardButton("🌐 Изменить Язык", callback_data="change_language")
        btn6 = telebot.types.InlineKeyboardButton("🎯 Моя Реферальная Ссылка", callback_data="get_referral_link")
        btn7 = telebot.types.InlineKeyboardButton("📊 Моя Статистика", callback_data="my_stat")  # New button for My Stat

    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    markup.add(btn5, btn6)
    markup.add(btn7)  # Adding My Stat button to the layout
    return markup

# Function to create the language selection menu
def language_selection_menu():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("English", "Русский")
    return markup

# Handle '/start' command and referral link
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_data = load_user_data()
    user_id = str(message.chat.id)

    # Initialize user data if the user is not in the file
    if user_id not in user_data:
        user_data[user_id] = {'referred_by': None, 'referral_count': 0, 'language': None}  # Ensure 'language' key exists

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
        welcome_message = (
            "Добро Пожаловать! Меня зовут RiseCoin Bot 🤖! Моя цель - помочь создателям в продвижении монеты 🚀 Выберите команду которая вас интересует ⬇️Welcome! My name is RiseCoin Bot 🤖! My goal is to help my creators in promoting our coin 🚀 Choose the information that interests you ⬇️:"
            if language == "en" else
            "Welcome! My name is RiseCoin Bot 🤖! My goal is to help my creators in promoting our coin 🚀 Choose the information that interests you ⬇️:"
        )
        bot.send_message(message.chat.id, welcome_message, reply_markup=main_menu(user_id, language))

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
    language = user_data[user_id]['language']
    bot.send_message(message.chat.id, "Добро Пожаловать! Меня зовут RiseCoin Bot 🤖! Моя цель - помочь создателям в продвижении монеты 🚀 Выберите команду которая вас интересует ⬇️:", reply_markup=main_menu(user_id, language))

# Handle language change request
@bot.callback_query_handler(func=lambda call: call.data == "change_language")
def change_language(call):
    user_data = load_user_data()
    user_id = str(call.message.chat.id)

    # Reset the user's language to None
    user_data[user_id]['language'] = None

    # Save the updated user data
    save_user_data(user_data)

    # Send the language selection menu again
    bot.send_message(call.message.chat.id, "Please select your language ⬇️/ Пожалуйста, выберите язык ⬇️", reply_markup=language_selection_menu())

# Handle button clicks
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    user_data = load_user_data()
    user_id = str(call.message.chat.id)
    language = user_data[user_id]['language']

    if call.data == "plans":
        bot.answer_callback_query(call.id, "📜 Plans selected!" if language == "en" else "📜 Планы выбраны!")
        bot.send_message(call.message.chat.id, 
                         "📜 Our plans are to innovate in the crypto space." if language == "en" 
                         else "📜 Наши планы - инновации в криптопространстве.")
    elif call.data == "release_date":
        bot.answer_callback_query(call.id, "📅 Release date selected!" if language == "en" else "📅 Дата выпуска выбрана!")
        bot.send_message(call.message.chat.id, 
                         "📅 The release date will be announced soon!" if language == "en" 
                         else "📅 Дата выпуска будет объявлена скоро!")
    elif call.data == "buy_token":
        bot.answer_callback_query(call.id, "🛒 Steps to buy selected!" if language == "en" else "🛒 Шаги по покупке выбраны!")
        bot.send_message(call.message.chat.id, 
                         "🛒 To buy, follow these steps:\n1️⃣ Create a wallet\n2️⃣ Buy tokens\n3️⃣ Hold & trade!" if language == "en" 
                         else "🛒 Для покупки выполните следующие шаги:\n1️⃣ Создайте кошелек\n2️⃣ Купите токены\n3️⃣ Держите и торгуйте!")
    elif call.data == "get_referral_link":
        # Generate referral link
        referral_link = f"https://t.me/risetokenblum?ref={user_id}"

        bot.answer_callback_query(call.id, "🎯 Your referral link!" if language == "en" else "🎯 Ваша реферальная ссылка!")
        bot.send_message(call.message.chat.id, 
                         f"🎯 Share your referral link with others: {referral_link}" if language == "en" 
                         else f"🎯 Поделитесь вашей реферальной ссылкой с другими: {referral_link}")
    elif call.data == "my_stat":
        # Show user their referral count
        referral_count = user_data[user_id]['referral_count']
        bot.answer_callback_query(call.id, "📊 Your stat!" if language == "en" else "📊 Ваша статистика!")
        bot.send_message(call.message.chat.id, 
                         f"🎯 You have invited {referral_count} person(s)!" if language == "en" 
                         else f"🎯 Вы пригласили {referral_count} человек(а)!")

# Handle user subscription tracking
@bot.message_handler(content_types=['text'])
def check_referral(message):
    # Check if the message includes a referral parameter
    if "ref=" in message.text:
        referrer_id = message.text.split('ref=')[1]

        # Check if user joined the channel
        try:
            user_id = str(message.chat.id)
            chat_member = bot.get_chat_member(CHANNEL_USERNAME, user_id)

            if chat_member.status in ["member", "administrator", "creator"]:  # User is subscribed to the channel
                # Increase the referral count for the referrer
                user_data = load_user_data()
                if referrer_id in user_data:
                    user_data[referrer_id]['referral_count'] += 1
                    save_user_data(user_data)
                    
                    # Send the congratulatory message
                    language = user_data[referrer_id]['language']
                    congratulatory_message = (
                        "Congrats! You are a step closer to winning the challenge!" 
                        if language == "en" else "Поздравляем! Вы на шаг ближе к победе в челлендже!"
                    )
                    bot.send_message(referrer_id, congratulatory_message)
        except Exception as e:
            print(f"Error checking subscription or increasing referral count: {e}")
  # Generate referral link
        referral_link = f"https://t.me/risetokenblum?start={user_id}"
        
        if language == "en":
            bot.send_message(call.message.chat.id, f"Your referral link: {referral_link}\nShare it with others to earn referral points!")
        else:
            bot.send_message(call.message.chat.id, f"Ваша реферальная ссылка: {referral_link}\nПоделитесь ею с другими, чтобы зарабатывать реферальные очки!")

    elif call.data == "my_stat":
        # Display referral count (stats)
        referral_count = user_data[user_id]['referral_count']
        
        if language == "en":
            bot.send_message(call.message.chat.id, f"You've invited {referral_count} people to the channel! Keep up the great work!")
        else:
            bot.send_message(call.message.chat.id, f"Вы пригласили {referral_count} людей в канал! Продолжайте в том же духе!")

    save_user_data(user_data)  # Ensure the user data is saved

# Handle referral link click and subscription to the channel
@bot.message_handler(commands=['start'])
def handle_start(message):
    user_data = load_user_data()
    user_id = str(message.chat.id)

    # Check if the user clicked the referral link and if the referral_id exists
    if message.text.startswith('/start'):
        referral_id = message.text.split('=')[-1]
        if referral_id and referral_id != user_id:
            # If the user has a valid referral ID and it is not the same as the current user
            if referral_id in user_data:
                user_data[referral_id]['referral_count'] += 1
                bot.send_message(user_data[referral_id]['language'], "Congrats! You are a step closer to winning the challenge!")
                save_user_data(user_data)

# Start polling (no webhook involved)
if __name__ == "__main__":
    print("Bot is running...")
    bot.polling(none_stop=True)






















  







































