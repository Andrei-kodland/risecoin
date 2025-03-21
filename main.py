import os
import json
import telebot
from telebot.apihelper import ApiTelegramException

# Основные настройки
BOT_TOKEN = "7987098857:AAH_nwOlbdn5Sq3VsEML0UqTEAKQyQfEnqE"
CHANNEL_USERNAME = "@risecoinblum"
CHANNEL_LINK = "https://t.me/risecoinblum"
USER_DATA_FILE = 'user_data.json'

# Ваш Telegram user ID или username
YOUR_USER_ID = "2083730569"  # или используйте свой user_id, если у вас его нет

# Инициализация бота
bot = telebot.TeleBot(BOT_TOKEN)

# Загрузка данных пользователей
def load_user_data():
    try:
        with open(USER_DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for user_id in data:
                if 'username' not in data[user_id]:
                    data[user_id]['username'] = None
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Сохранение данных пользователей
def save_user_data(user_data):
    try:
        with open(USER_DATA_FILE, 'w', encoding='utf-8') as file:
            json.dump(user_data, file, indent=4, ensure_ascii=False)
        print("Data saved")
    except Exception as e:
        print(f"Error saving data: {e}")

# Главное меню
def main_menu(user_id, lang):
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    buttons = {
        "ru": [
            ("📜 Планы", "plans"),
            ("📅 Дата выпуска", "release_date"),
            ("🛒 Покупка токена", "buy_token"),
            ("🌐 Сменить язык", "change_language"),
            ("🎯 Реф ссылка", "get_referral_link"),
            ("📊 Стата", "my_stat")
        ],
        "en": [
            ("📜 Plans", "plans"),
            ("📅 Release Date", "release_date"),
            ("🛒 Buy Token", "buy_token"),
            ("🌐 Change Language", "change_language"),
            ("🎯 Referral Link", "get_referral_link"),
            ("📊 Stats", "my_stat")
        ]
    }
    for text, callback, *url in buttons[lang]:
        btn = telebot.types.InlineKeyboardButton(text, url=url[0] if url else None, callback_data=callback if not url else None)
        markup.add(btn) if url else markup.add(btn, row_width=2)
    return markup

# Меню выбора языка
def language_selection_menu():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("Русский", "English")
    return markup

# Обработка команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_data = load_user_data()
    user_id = str(message.chat.id)
    ref_id = message.text.split()[1] if len(message.text.split()) > 1 else None
    if ref_id == user_id or ref_id not in user_data:
        ref_id = None

    if user_id not in user_data or ref_id:
        user_data[user_id] = {
            'username': None,
            'referred_by': ref_id,
            'referral_count': user_data.get(user_id, {}).get('referral_count', 0),
            'referrals': user_data.get(user_id, {}).get('referrals', []),
            'language': None,
            'processed_referral': user_data.get(user_id, {}).get('processed_referral', None),
            'is_new': True
        }
        bot.send_message(user_id, "Введи свой ник, чтобы начать!\nEnter your nickname to start!")
        save_user_data(user_data)
        return

    lang = user_data[user_id].get('language', 'ru')
    if user_data[user_id].get('username') is None:
        bot.send_message(user_id, "Введи свой ник, чтобы начать!\nEnter your nickname to start!")
    elif not user_data[user_id]['language']:
        bot.send_message(user_id, "Выбери язык ⬇️\nSelect language ⬇️", reply_markup=language_selection_menu())
    elif user_data[user_id].get('is_new', False):
        msg = f"Подпишись на группу {CHANNEL_LINK}, чтобы завершить регистрацию!" if lang == "ru" else f"Join our group {CHANNEL_LINK} to complete registration!"
        bot.send_message(user_id, msg)
        markup = telebot.types.InlineKeyboardMarkup()
        text = "Проверить подписку" if lang == "ru" else "Check subscription"
        markup.add(telebot.types.InlineKeyboardButton(text, callback_data="check_subscription"))
        bot.send_message(user_id, "После подписки жми сюда:\nClick after joining:", reply_markup=markup)
    else:
        msg = "С возвращением! Выбери что хочешь ⬇️" if lang == "ru" else "Welcome back! Pick what you want ⬇️"
        bot.send_message(user_id, msg, reply_markup=main_menu(user_id, lang))

# Установка ника
@bot.message_handler(func=lambda msg: str(msg.chat.id) in load_user_data() and load_user_data()[str(msg.chat.id)].get('username') is None)
def set_nickname(msg):
    user_data = load_user_data()
    user_id = str(msg.chat.id)
    nick = msg.text.strip()

    if not nick or len(nick) < 3 or len(nick) > 20 or not nick.isalnum():
        bot.send_message(user_id, "Ник от 3 до 20 символов, только буквы и цифры!\nNickname 3-20 chars, letters and numbers only!")
        return

    user_data[user_id]['username'] = nick
    bot.send_message(user_id, "Ник готов! Выбери язык ⬇️\nNickname set! Pick language ⬇️", reply_markup=language_selection_menu())
    save_user_data(user_data)

# Выбор языка
@bot.message_handler(func=lambda msg: msg.text in ["Русский", "English"])
def set_language(msg):
    user_data = load_user_data()
    user_id = str(msg.chat.id)

    if user_data[user_id].get('username') is None:
        bot.send_message(user_id, "Сначала ник выбери!\nSet nickname first!")
        return

    user_data[user_id]['language'] = "ru" if msg.text == "Русский" else "en"
    lang = user_data[user_id]['language']

    if lang == "en":
        bot.send_message(user_id, "The language is English, everything will be shown in this language.")
    else:
        bot.send_message(user_id, "Язык установлен на русский, все будет на этом языке.")

    if user_data[user_id].get('is_new'):
        msg = f"Подпишись на группу {CHANNEL_LINK} для завершения!" if lang == "ru" else f"Join our group {CHANNEL_LINK} to finish!"
        bot.send_message(user_id, msg)
        markup = telebot.types.InlineKeyboardMarkup()
        text = "Проверить" if lang == "ru" else "Check"
        markup.add(telebot.types.InlineKeyboardButton(text, callback_data="check_subscription"))
        bot.send_message(user_id, "Жми после подписки:\nClick after joining:", reply_markup=markup)
    else:
        msg = "Привет! Я RiseCoin Bot 🤖 Помогаю продвигать монету 🚀 Выбери что надо ⬇️" if lang == "ru" else "Hey! I’m RiseCoin Bot 🤖 Here to promote our coin 🚀 Pick something ⬇️"
        bot.send_message(user_id, msg, reply_markup=main_menu(user_id, lang))

    save_user_data(user_data)

# Проверка подписки
@bot.callback_query_handler(func=lambda call: call.data == "check_subscription")
def check_subscription(call):
    user_data = load_user_data()
    user_id = str(call.message.chat.id)

    if user_data[user_id].get('username') is None:
        text = "Сначала ник!\nNickname first!" if user_data[user_id].get('language', 'ru') == "ru" else "Nickname first!"
        bot.send_message(user_id, text)
        bot.answer_callback_query(call.id)
        return

    if not user_data[user_id]['language']:
        text = "Выбери язык сначала!\nPick language first!" if user_data[user_id].get('language', 'ru') == "ru" else "Pick language first!"
        bot.send_message(user_id, text)
        bot.answer_callback_query(call.id)
        return                                   

    lang = user_data[user_id]['language']
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        if member.status in ["member", "administrator", "creator"]:
            user_data[user_id]['is_new'] = False

            ref_id = user_data[user_id]['referred_by']
            if ref_id and user_data[user_id]['processed_referral'] != ref_id:
                user_data[ref_id]['referral_count'] = user_data[ref_id].get('referral_count', 0) + 1
                user_data[ref_id]['referrals'] = user_data[ref_id].get('referrals', []) + [user_id]
                user_data[user_id]['processed_referral'] = ref_id
                ref_msg = f"Круто! @{user_data[user_id]['username']} пришел по твоей ссылке!" if lang == "ru" else f"Cool! @{user_data[user_id]['username']} joined via your link!"
                try:
                    bot.send_message(ref_id, ref_msg)
                except ApiTelegramException as e:
                    print(f"Failed to notify referrer {ref_id}: {e}")

            msg = "Добро пожаловать! Я RiseCoin Bot 🤖 Тут для продвижения монеты 🚀 Выбери что хочешь ⬇️" if lang == "ru" else "Welcome! I’m RiseCoin Bot 🤖 Helping promote our coin 🚀 Pick something ⬇️"
            bot.send_message(user_id, msg, reply_markup=main_menu(user_id, lang))
            bot.answer_callback_query(call.id, "Готово!" if lang == "ru" else "Done!")
        else:
            bot.answer_callback_query(call.id, "Подпишись сначала!" if lang == "ru" else "Join first!")
    except ApiTelegramException as e:
        print(f"Subscription check error: {e}")
        if e.error_code == 400 and "chat not found" in str(e):
            text = f"Группа {CHANNEL_USERNAME} не найдена! Пиши в поддержку!" if lang == "ru" else f"Group {CHANNEL_USERNAME} not found! Contact support!"
            bot.answer_callback_query(call.id, text)
        else:
            bot.answer_callback_query(call.id, "Ошибка, попробуй еще!" if lang == "ru" else "Error, try again!")
    save_user_data(user_data)

# Смена языка
@bot.callback_query_handler(func=lambda call: call.data == "change_language")
def change_language(call):
    user_data = load_user_data()
    user_id = str(call.message.chat.id)
    lang = user_data[user_id]['language']
    user_data[user_id]['language'] = None
    save_user_data(user_data)
    msg = "Выбери язык ⬇️\nSelect language ⬇️" if lang == "ru" else "Select language ⬇️"
    bot.send_message(user_id, msg, reply_markup=language_selection_menu())
    bot.answer_callback_query(call.id)

# Обработка фотографии
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    user_id = str(message.chat.id)
    
    # Получаем ID фотографии
    photo_id = message.photo[-1].file_id  # Скачиваем самое большое изображение (в photo list есть несколько вариантов)
    
    # Получаем файл фотографии
    file_info = bot.get_file(photo_id)
    file_url = f'https://api.telegram.org/file/bot{BOT_TOKEN}/{file_info.file_path}'
    
    # Отправляем фото на ваш аккаунт
    try:
        # Forward the photo to your admin (without sending user ID to the user)
        bot.forward_message(YOUR_USER_ID, user_id, message.message_id)
        
        # Send confirmation message to the user
        bot.send_message(user_id, "Your photo has been sent to the admin.")
    except ApiTelegramException as e:
        print(f"Failed to forward photo: {e}")
        bot.send_message(user_id, "There was an error sending the photo to the admin. Please try again later.")

# Запуск бота
if __name__ == "__main__":
    print("Bot started...")
    try:
        bot.polling(none_stop=True)
    except ApiTelegramException as e:
        print(f"Telegram API error: {e}")
        if e.error_code == 409:
            print("Conflict: Another bot instance is running. Stop it.")
        save_user_data(load_user_data())
    except Exception as e:
        print(f"Something went wrong: {e}")
        import traceback
        traceback.print_exc()
        save_user_data(load_user_data())




















  







































