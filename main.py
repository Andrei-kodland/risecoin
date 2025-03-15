import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import json
import os

# Replace with your actual bot token
BOT_TOKEN = "7987098857:AAH_nwOlbdn5Sq3VsEML0UqTEAKQyQfEnqE"
CHANNEL_USERNAME = "@risetokenblum"  # Change this to your channel's username
bot = telebot.TeleBot(BOT_TOKEN)

USER_DATA_FILE = 'user_data.json'

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
        print("User data saved successfully.")  # Debugging line to confirm saving
    except Exception as e:
        print(f"Error saving user data: {e}")  # Debugging line to capture errors

# Function to create the main menu
def main_menu(user_id):
    markup = InlineKeyboardMarkup(row_width=2)
    referral_link = f"https://t.me/risetokenblum?start={user_id}"
    btn1 = InlineKeyboardButton("📜 Планы", callback_data="планы")
    btn2 = InlineKeyboardButton("📅 Дата Выпуска", callback_data="датавыпускамонеты")
    btn3 = InlineKeyboardButton("🛒 Покупка Токена", callback_data="каккупитьмонету?")    
    btn4 = InlineKeyboardButton("🌍 Веб-сайт", url="https://i.redd.it/ceetrhas51441.jpg")
    btn5 = InlineKeyboardButton(f"🔗 Ваша реферальная ссылка", callback_data="referral_link")
    btn6 = InlineKeyboardButton(f"📊 Моя Статистика", callback_data="referral_count")

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
        user_data[user_id] = {'referred_by': None, 'referral_count': 0}
        print(f"New user initialized: {user_id}")  # Debugging line

    # Check if the user was referred by someone else via the referral link
    referrer_id = message.text.split('start=')[1] if 'start=' in message.text else None
    if referrer_id:
        referrer_id = referrer_id.strip()
        print(f"Referral detected. Referrer ID: {referrer_id}")  # Debugging line
        if referrer_id in user_data:
            user_data[user_id]['referred_by'] = referrer_id  # Track who referred this user
            print(f"User {user_id} referred by {referrer_id}")  # Debugging line
            save_user_data(user_data)  # Save data after updating referral relationship

    # Send welcome message with main menu
    bot.send_message(message.chat.id, "Добро Пожаловать! Меня зовут RiseCoin Bot 🤖! Моя цель - помочь создателям в продвижении монеты 🚀 Выберите команду которая вас интересует ⬇️:", reply_markup=main_menu(user_id))

# Handle subscription to channel and update referral count
@bot.message_handler(func=lambda message: True)
def handle_subscription(message):
    user_data = load_user_data()
    user_id = str(message.chat.id)
    
    try:
        # Check if the user is a member of the channel
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        
        if member.status in ["member", "administrator", "creator"]:
            # User is subscribed to the channel
            print(f"User {user_id} is subscribed to the channel.")  # Debugging line
            
            # Check if the user has a referrer
            if user_data.get(user_id, {}).get('referred_by'):
                referrer_id = user_data[user_id]['referred_by']
                if referrer_id and referrer_id in user_data:
                    # Update the referrer's referral count
                    user_data[referrer_id]['referral_count'] += 1
                    save_user_data(user_data)  # Save data after updating referral count
                    print(f"Referrer {referrer_id} referral count updated to {user_data[referrer_id]['referral_count']}")  # Debugging line
                    
                    # Send confirmation to the referrer
                    bot.send_message(referrer_id, f"🎉 One of your referrals has successfully joined the channel! Your referral count has been updated to {user_data[referrer_id]['referral_count']}")
            
            # Send message to the person who clicked the link
            bot.send_message(message.chat.id, "🎉 You've successfully joined the channel through the referral link!")
        
        else:
            bot.send_message(message.chat.id, "❗ You need to join the channel to confirm your referral.")
    
    except Exception as e:
        print(f"Error checking subscription: {e}")

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

# Remove any webhooks before polling
bot.remove_webhook()

# Start polling (no webhook involved)
if __name__ == "__main__":
    print("Bot is running...")
    bot.polling(none_stop=True)
