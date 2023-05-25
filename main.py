import telebot
from googletrans import Translator, LANGUAGES

# Вставьте здесь ваш токен Telegram-бота
TOKEN = '6297587605:AAFqJxhe29mznwgarwmCIsVgm918EDkU7Vw'

bot = telebot.TeleBot(TOKEN)
translator = Translator()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот-переводчик. Введите текст для перевода.")

@bot.message_handler(func=lambda message: True)
def translate_text(message):
    try:
        chat_id = message.chat.id
        text = message.text

        # Определение языка исходного текста
        source_lang = translator.detect(text).lang

        # Клавиатура для выбора языка перевода
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2)
        for lang_code, lang_name in LANGUAGES.items():
            keyboard.add(lang_name)

        bot.send_message(chat_id, 'Выберите язык перевода:', reply_markup=keyboard)

        # Сохранение информации о тексте и исходном языке для дальнейшего использования
        bot.register_next_step_handler(message, process_translation, text=text, source_lang=source_lang)

    except Exception as e:
        handle_error(message, e)

def process_translation(message, text, source_lang):
    try:
        chat_id = message.chat.id
        target_lang = message.text

        # Проверка, выбран ли доступный язык перевода
        if target_lang not in LANGUAGES.values():
            raise ValueError('Выбран недопустимый язык перевода.')

        # Перевод текста
        translated = translator.translate(text, src=source_lang, dest=target_lang)
        bot.send_message(chat_id, f'Перевод: {translated.text}')

    except Exception as e:
        handle_error(message, e)

def handle_error(message, error):
    error_message = f'Произошла ошибка: {str(error)}'
    bot.send_message(message.chat.id, error_message)

@bot.message_handler(content_types=['text'])
def handle_unknown(message):
    bot.send_message(message.chat.id, 'Извините, я не распознал вашу команду. Пожалуйста, воспользуйтесь командой /start для начала перевода.')

bot.polling()
