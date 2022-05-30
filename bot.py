import telebot
from telebot import types
import data
import os

help_message = '''Добро пожаловать в бот Kanji Master! 🌸 Он создан для удобного повторения японских иероглифов и слов, 
связанных с ними! Пока что здесь есть два режима: повторение непосредственно иероглифов и повторение слов \n\n 
1️⃣ Повторение иероглифов: для запуска этого режима нажми кнопку "Случайный кандзи". Бот предложит тебе случайный 
кандзи из базы, а также возможность посмотреть его чтения, порядок черт и связанные с ним слова. \n\n 2️⃣ Повторение 
слов: для запуска этого режима нажми кнопку "Случайное слово". Повторять слова можно тремя разными способами — по 
самому слову непосредственно, по чтению или по переводу — как будет удобнее. \n\nВ дальнейшем планируется добавить 
возможность повторять иероглифы по уровням — N5, N4 и так далее. А, может, что-нибудь еще ☺️  \n\n Обо всех ошибках, связанных с ботом, сообщайте 
в телеграме: @dorichan'''

if __name__ == '__main__':
    TOKEN = str(os.environ['TOKEN'])
    bot = telebot.TeleBot(TOKEN, skip_pending=True)
    start_markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    exit_btn = types.KeyboardButton('Выход')
    start_markup_btn1 = types.KeyboardButton('Начать')
    start_markup_btn2 = types.KeyboardButton('Помощь')
    start_markup.add(start_markup_btn1, start_markup_btn2)

    exercise_markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    choose_markup_btn1 = types.KeyboardButton('Случайный кандзи')
    choose_markup_btn2 = types.KeyboardButton('Случайное слово')
    exercise_markup.add(choose_markup_btn1, choose_markup_btn2, exit_btn)

    words_learning_mod_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    words_learning_start_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    words_learning_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    words_learning_markup_btn5 = types.KeyboardButton('Сначала слово')
    words_learning_markup_btn6 = types.KeyboardButton('Сначала перевод')
    words_learning_markup_btn7 = types.KeyboardButton('Сначала чтение')
    words_learning_markup_btn1 = types.KeyboardButton('Чтение')
    words_learning_markup_btn2 = types.KeyboardButton('Перевод')
    words_learning_markup_btn3 = types.KeyboardButton('Дальше')
    words_learning_markup_btn8 = types.KeyboardButton('Слово')

    words_learning_mod_markup.add(words_learning_markup_btn5, words_learning_markup_btn6, words_learning_markup_btn7,
                                  exit_btn)
    words_learning_start_markup.add(words_learning_markup_btn3, exit_btn)
    words_learning_markup.add(words_learning_markup_btn8, words_learning_markup_btn1, words_learning_markup_btn2,
                              words_learning_markup_btn3,
                              exit_btn)

    kanji_learning_start_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    kanji_learning_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    kanji_learning_markup_btn1 = types.KeyboardButton('Новый кандзи')
    kanji_learning_markup_btn2 = types.KeyboardButton('Чтение')
    kanji_learning_markup_btn3 = types.KeyboardButton('Слова с этим кандзи')
    kanji_learning_markup_btn5 = types.KeyboardButton('Порядок черт')

    kanji_learning_start_markup.add(kanji_learning_markup_btn1, exit_btn)
    kanji_learning_markup.add(kanji_learning_markup_btn2, kanji_learning_markup_btn3, kanji_learning_markup_btn5,
                              kanji_learning_markup_btn1, exit_btn)


    @bot.message_handler(commands=['start', 'go'])
    def start_handler(message):
        chat_id = message.chat.id
        if chat_id in data.users:
            msg = bot.send_message(message.chat.id, 'Чем займемся?', reply_markup=exercise_markup)
            bot.register_next_step_handler(msg, choose_exercise)
        else:
            data.add_user(chat_id)
            msg = bot.send_message(message.chat.id, help_message, reply_markup=exercise_markup)
            bot.register_next_step_handler(msg, choose_exercise)


    @bot.message_handler(content_types=['text'])
    def start_handler(message):
        chat_id = message.chat.id
        text = message.text

        if not chat_id in data.users:
            data.add_user(chat_id)
        # print(data.get_user(chat_id).isTalking)
        if data.get_user(chat_id).isTalking == 1:
            return
        else:
            data.get_user(chat_id).isTalking = 1
        if text == 'Выход':
            bot.send_message(chat_id, 'До встречи!', reply_markup=start_markup)
            data.get_user(chat_id).isTalking = 0
            return
        elif text == 'Помощь':
            msg = bot.send_message(chat_id, help_message, reply_markup=exercise_markup)
            bot.register_next_step_handler(msg, choose_exercise)
            data.get_user(chat_id).isTalking = 0
            return
        else:
            msg = bot.send_message(chat_id, 'Чем займемся?', reply_markup=exercise_markup)
            bot.register_next_step_handler(msg, choose_exercise)
            data.get_user(chat_id).isTalking = 0
            # print(message.text, data.get_user(chat_id).isTalking)


    def choose_exercise(message):
        chat_id = message.chat.id
        text = message.text
        if data.get_user(chat_id).isTalking == 1:
            return
        else:
            data.get_user(chat_id).isTalking = 1
        if text == 'Случайный кандзи':
            msg = bot.send_message(chat_id, 'Понял-принял, начинаем!', reply_markup=kanji_learning_start_markup)
            bot.register_next_step_handler(msg, kanji_learning)
            data.get_user(chat_id).isTalking = 0
        elif text == 'Случайное слово':
            msg = bot.send_message(chat_id, 'Как ты хочешь учить слова?', reply_markup=words_learning_mod_markup)
            bot.register_next_step_handler(msg, words_learning_mod)
            data.get_user(chat_id).isTalking = 0
        elif text == 'Выход':
            bot.send_message(message.chat.id, 'До встречи!', reply_markup=start_markup)
            data.get_user(chat_id).isTalking = 0
        else:
            msg = bot.send_message(chat_id, 'Я не знаю такую команду. Используй клавиатуру!',
                                   reply_markup=exercise_markup)
            bot.register_next_step_handler(msg, choose_exercise)
            data.get_user(chat_id).isTalking = 0


    def kanji_learning(message):

        chat_id = message.chat.id
        text = message.text
        if data.get_user(chat_id).isTalking == 1:
            return
        else:
            data.get_user(chat_id).isTalking = 1

        if text == 'Выход':
            exit_to_menu(chat_id)
        elif text == 'Порядок черт':
            txt = data.kanji_handler(text, chat_id)
            msg = bot.send_video(chat_id, txt, reply_markup=kanji_learning_markup)
            bot.register_next_step_handler(msg, kanji_learning)
            data.get_user(chat_id).isTalking = 0
        else:
            txt = data.kanji_handler(text, chat_id)
            if txt == 'Error':
                msg = bot.send_message(chat_id, 'Я не знаю такую команду. Используй клавиатуру!',
                                       reply_markup=kanji_learning_markup)
                bot.register_next_step_handler(msg, kanji_learning)
                data.get_user(chat_id).isTalking = 0
                return
            msg = bot.send_message(chat_id, txt,
                                   reply_markup=kanji_learning_markup)
            bot.register_next_step_handler(msg, kanji_learning)
            data.get_user(chat_id).isTalking = 0


    def words_learning_mod(message):
        chat_id = message.chat.id
        text = message.text
        if data.get_user(chat_id).isTalking == 1:
            return
        else:
            data.get_user(chat_id).isTalking = 1
        if text == 'Сначала слово':
            msg = bot.send_message(chat_id, 'Для управления используй кнопки',
                                   reply_markup=words_learning_start_markup)
            data.get_user(chat_id).change_word_mod('by_original')
            bot.register_next_step_handler(msg, words_learning)
            data.get_user(chat_id).isTalking = 0
        elif text == 'Сначала перевод':
            msg = bot.send_message(chat_id, 'Для управления используй кнопки',
                                   reply_markup=words_learning_start_markup)
            data.get_user(chat_id).change_word_mod('by_translation')
            bot.register_next_step_handler(msg, words_learning)
            data.get_user(chat_id).isTalking = 0
        elif text == 'Сначала чтение':
            msg = bot.send_message(chat_id, 'Для управления используй кнопки',
                                   reply_markup=words_learning_start_markup)
            data.get_user(chat_id).change_word_mod('by_reading')
            bot.register_next_step_handler(msg, words_learning)
            data.get_user(chat_id).isTalking = 0
        elif text == 'Выход':
            exit_to_menu(chat_id)
        else:
            msg = bot.send_message(chat_id, 'Я не знаю такую команду. Используй клавиатуру!',
                                   reply_markup=words_learning_mod_markup)
            bot.register_next_step_handler(msg, words_learning_mod)
            data.get_user(chat_id).isTalking = 0


    def words_learning(message):
        chat_id = message.chat.id
        text = message.text

        if data.get_user(chat_id).isTalking == 1:
            return
        else:
            data.get_user(chat_id).isTalking = 1
        if text == 'Выход':
            exit_to_menu(chat_id)

        else:
            txt = data.word_handler(text, chat_id)
            if txt == 'Error':
                msg = bot.send_message(chat_id, 'Я не знаю такую команду. Используй клавиатуру!',
                                       reply_markup=words_learning_markup)
                bot.register_next_step_handler(msg, words_learning)
                data.get_user(chat_id).isTalking = 0
                return
            msg = bot.send_message(chat_id, txt,
                                   reply_markup=words_learning_markup)
            bot.register_next_step_handler(msg, words_learning)
            data.get_user(chat_id).isTalking = 0


    def exit_to_menu(chat_id):
        data.get_user(chat_id).isTalking = 0
        msg = bot.send_message(chat_id, 'Хочешь выбрать другую тренировку?', reply_markup=exercise_markup)
        bot.register_next_step_handler(msg, choose_exercise)


    bot.polling()
