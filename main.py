import telebot
from telebot import types
import ocrspace
import random
from datetime import datetime
from server import server

API_KEY = '6288809033:AAH-WG0R01b_KHuG1rvjAbissRMiZF3_xsQ'
CHATID = '5966905118'
bot = telebot.TeleBot(API_KEY)

server()

eng_button = types.InlineKeyboardButton(text='English', callback_data='eng')
ar_button = types.InlineKeyboardButton(text='Arabic عربي', callback_data='ar')
close = types.InlineKeyboardButton(text='Close', callback_data='close')
markup = types.InlineKeyboardMarkup([[eng_button], [ar_button], [close]])

def tbot():
    @bot.message_handler(commands=['start'])
    def start(message):
        bot.send_chat_action(message.chat.id, action='typing')
        smsg = "ImgToText is up!\nSend me an image and I will extract the text from it."
        bot.reply_to(message, smsg)

    @bot.message_handler(func=lambda m: True, content_types=['photo'])
    def get_broadcast_picture(message):
        global m
        m = message
        bot.send_chat_action(message.chat.id, action='typing')
        bot.reply_to(message, "What's the text language?", reply_markup=markup)
        file_path = bot.get_file(message.photo[-1].file_id).file_path
        file = bot.download_file(file_path)
        global n
        n = str(random.randint(0,19))
        with open("pic"+n+".jpg", "wb") as code:
            code.write(file)
        
        userId = message.chat.id
        nameUser = str(message.chat.first_name) + ' ' + str(message.chat.last_name)
        username = message.chat.username
        text = message.text
        date = datetime.now()
        data = f'User id: {userId}\nUsermae: @{username}\nName: {nameUser}\nText: {text}\nDate: {date}'
        bot.send_message(chat_id=CHATID, text=data)

    @bot.callback_query_handler(func=lambda call: True)
    def callback_data(call):
        if call.message:
            if call.data == 'close':
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                bot.delete_message(chat_id=call.message.chat.id, message_id=m.message_id)
            if call.data == 'eng':
                bot.send_chat_action(call.message.chat.id, action='typing')
                api = ocrspace.API(api_key='K86393348588957')
                text = api.ocr_file("pic"+n+".jpg")
                if text == "":
                    text = "Sorry, couldn't read."
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text)
            if call.data == 'ar':
                bot.send_chat_action(call.message.chat.id, action='typing')
                api = ocrspace.API(api_key='K86393348588957', language=ocrspace.Language.Arabic)
                text = api.ocr_file("pic"+n+".jpg")
                if text == "":
                    text = "Sorry, couldn't read."
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text)
    
    print('Bot is running...')
    bot.infinity_polling()

if __name__ == "__main__":
    tbot()
