import telebot
import json
import os
import sys

# Replace with your actual bot token
BOT_TOKEN = "7987098857:AAH_nwOlbdn5Sq3VsEML0UqTEAKQyQfEnqE"  # Replace this with your bot token
CHANNEL_USERNAME = "@risetokenblum"  # Replace with your channel username

USER_DATA_FILE = 'user_data.json'
bot = telebot.TeleBot(BOT_TOKEN)

# Function to check if another instance is running
def is_already_running():
    lock_file = os.path.join(os.getcwd(), "bot.lock")
    if os.path.exists(lock_file):
        print("Another instance of the bot is already running.")
        sys.exit(1)
    else:
        print("Creating lock file...")
        with open(lock_file, "w") as f:
            f.write(str(os.getpid()))

# Function to clean up the lock file
def cleanup_lock_file():
    lock_file = os.path.join(os.getcwd(), "bot.lock")
    if os.path.exists(lock_file):
        print("Cleaning up lock file...")
        os.remove(lock_file)

# Function to load user data from the file
def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        try:
            with open(USER_DATA_FILE, 'r') as file:
                return json.load(file)
        except Exception as e:
            print(f"Error loading user data: {e}")
            return {}
    return {}

# Function to save user data to the file
def save_user_data(user_data):
    try:
        with open(USER_DATA_FILE, 'w') as file:
            json.dump(user_data, file, indent=4)
        print("User data saved successfully.")  # Debugging line to confirm saving
    except Exception as e:
        print(f"Error saving user data: {e}")  # Debugging line to capture errors

# Function to create the main menu
def main_menu(user_id):
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    referral_link = f"https://t.me/risetokenblum?start={user_id}"
    btn1 = telebot.types.InlineKeyboardButton("📜 Планы", callback_data="планы")
    btn2 = telebot.types.InlineKeyboardButton("📅 Дата Выпуска", callback_data="датавыпускамонеты")
    btn3 = telebot.types.InlineKeyboardButton("🛒 Покупка Токена", callback_data="каккупитьмонету?")    
    btn4 = telebot.types.InlineKeyboardButton("🌍 Веб-сайт", url="https://i.redd.it/ceetrhas51441.jpg")
    btn5 = telebot.types.InlineKeyboardButton(f"🔗 Ваша реферальная ссылка", callback_data="referral_link")
    btn6 = telebot.types.InlineKeyboardButton(f"📊 Моя Статистика", callback_data="referral_count")

    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    markup.add(btn5, btn6)

    return markup

# Handle '/start' command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_data = load_user_data()
    user_id = str(message.chat.id)
    print(f"User {user_id} started the bot.")  # Debugging line

    # Initialize the user if it's the first time they use the bot
    if user_id not in user_data:
        user_data[user_id] = {'referred_by': None, 'referral_count': 0, 'has_subscribed': False}
        print(f"New user initialized: {user_id}")  # Debugging line

    # Check if the user was referred by someone else via the referral link
    referrer_id = message.text.split('start=')[1] if 'start=' in message.text else None
    if referrer_id:
        referrer_id = referrer_id.strip()
        print(f"Referral detected. Referrer ID: {referrer_id}")  # Debugging line
        if referrer_id in user_data and referrer_id != user_id:  # Prevent self-referral
            user_data[user_id]['referred_by'] = referrer_id  # Track who referred this user
            print(f"User {user_id} referred by {referrer_id}")  # Debugging line
            save_user_data(user_data)  # Save data after updating referral relationship

    # Check if the user is subscribed to the channel
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        print(f"Subscription check for user {user_id}. Status: {member.status}")  # Debugging line
        if member.status in ["member", "administrator", "creator"]:
            print(f"User {user_id} is subscribed to the channel.")  # Debugging line

            # Update referral count for the referrer if applicable
            if user_data[user_id]['referred_by'] and not user_data[user_id]['has_subscribed']:
                referrer_id = user_data[user_id]['referred_by']
                if referrer_id in user_data:
                    user_data[referrer_id]['referral_count'] += 1
                    user_data[user_id]['has_subscribed'] = True  # Mark as subscribed to prevent duplicate updates
                    save_user_data(user_data)  # Save data after updating referral count
                    print(f"Referrer {referrer_id} referral count updated to {user_data[referrer_id]['referral_count']}")  # Debugging line

                    # Send confirmation to the referrer
                    bot.send_message(referrer_id, f"🎉 Congrats! Your referral count has increased by 1. Your total referrals: {user_data[referrer_id]['referral_count']}")
        else:
            bot.send_message(message.chat.id, "❗ You need to join the channel to confirm your referral.")
    except Exception as e:
        print(f"Error checking subscription: {e}")

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
    elif call.data == "referral_link":
        bot.answer_callback_query(call.id, "📲 Your referral link copied!")
        referral_link = f"https://t.me/risetokenblum?start={user_id}"
        bot.send_message(call.message.chat.id, f"📲 Your referral link is: {referral_link}")
    elif call.data == "referral_count":
        referral_count = user_data.get(user_id, {}).get('referral_count', 0)
        bot.answer_callback_query(call.id, "📊 Your referral stats selected!")
        bot.send_message(call.message.chat.id, f"📊 You have referred {referral_count} people!")
    else:
        bot.answer_callback_query(call.id, "❗ Unknown action!")

    save_user_data(user_data)

# Start polling (no webhook involved)
if __name__ == "__main__":
    # Check if another instance is running
    is_already_running()

    try:
        print("Bot is running...")
        bot.polling(none_stop=True, non_strict=True)
    finally:
        # Clean up the lock file when the bot stops
        cleanup_lock_file()
  







































