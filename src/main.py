import re
import time
import telebot
import logging
from decouple import config
from name_make import poster, lang_check, text_plain

# logging info
logging.basicConfig(filename='info.log', filemode='a', level=logging.INFO, format='%(asctime)s - %(filename)s - %(message)s')

# Token
TOKEN = config('TOKEN')

# initial
bot = telebot.TeleBot(TOKEN)
print('bot is online!')


# Checks that the submitted text is not a link
def url_check(text):
    regex = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    check = re.findall(regex, text)
    if check != []:
        return False
    else:
        return True

# start function
@bot.message_handler(commands=['start'])
def start(msg):
    logging.info(f'{msg.chat.first_name} - {msg.chat.id}') # add user to info.log

    # Specify the texts to be sent to the user
    persian = 'سلام این بات تبدیل لوگوی بتمن 2020 است، لطفا اسم خود را به انگلیسی یا فارسی وارد کنید.'
    english = 'Hi, this bot is a name conversion to Batman 2020 logo, please enter your name in English or Persian.'
    github_link = 'https://github.com/Hr-ArshA/BatName_bot'
    youtube_link = 'https://youtu.be/2jLZfh-Ge6E'

    text = f'{persian}\n\n{english}\n\n[GitHub repository link]({github_link})\n\n[YouTube video link]({youtube_link})\n\n\n@BatNameBot'

    # Send a start message to the user
    bot.reply_to(msg, text, parse_mode='markdown')


# Recognize text and send photo
@bot.message_handler(func=lambda message: True, content_types=['text'])
def text_detector(msg):

    bot.reply_to(msg, "چند لحظه صبر کنید...")

    error_text = 'لطفا یک متن معتبر وارد کنید.' 
    if url_check(text_plain(msg.text)):
        if lang_check(text_plain(msg.text)):
            pic = poster(text_plain(msg.text))
            time.sleep(10)
            photo = open(pic, 'rb')
            bot.send_photo(msg.chat.id, photo)
            bot.send_message(msg.chat.id, f'{msg.chat.first_name}')
            time.sleep(2)

        else:
            bot.send_message(msg.chat.id, error_text)

    else:
        bot.send_message(msg.chat.id, error_text)


bot.infinity_polling()