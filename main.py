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

    # If the user is not in the data file, initialize them
    if user_id not in user_data:
        user_data[user_id] = {'referred_by': None, 'referral_count': 0}

    # Parse the referral link (if any)
    referrer_id = message.text.split('start=')[-1] if 'start=' in message.text else None
    if referrer_id and referrer_id != user_id:  # Avoid self-referrals
        referrer_id = referrer_id.strip()
        if referrer_id in user_data:
            user_data[user_id]['referred_by'] = referrer_id
            save_user_data(user_data)  # Save the user data after assigning the referrer

            # Check if the user is subscribed to the channel (subscription check happens after referral assignment)
            check_subscription(user_id, referrer_id)

    # Send main menu to the user
    bot.send_message(message.chat.id, "Добро Пожаловать! Выберите команду ⬇️:", reply_markup=main_menu(user_id))

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

    save_user_data(user_data)

# Check if the user is subscribed to the channel and update referrer
def check_subscription(user_id, referrer_id):
    user_data = load_user_data()
    try:
        # Check if the user is a member of the channel
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        print(f"DEBUG: Membership status of {user_id}: {member}")  # Log the full member info for debugging
        if member.status in ["member", "administrator", "creator"]:
            print(f"User {user_id} is subscribed to the channel.")  # Debugging line

            # Increment the referral count of the referrer
            user_data[referrer_id]['referral_count'] += 1
            save_user_data(user_data)  # Save the updated referral count
            bot.send_message(referrer_id, f"🎉 One of your referrals has joined the channel! Your referral count is now {user_data[referrer_id]['referral_count']}")

            # Send a confirmation message to the referred user
            bot.send_message(user_id, "🎉 You've successfully joined the channel through the referral link!")
        else:
            bot.send_message(user_id, "❗ You need to join the channel to confirm your referral.")
    except Exception as e:
        print(f"Error checking subscription: {e}")

# Start polling (no webhook involved)
if __name__ == "__main__":
    print("Bot is running...")
    bot.polling(none_stop=True)







































