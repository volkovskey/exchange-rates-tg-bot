#!/usr/bin/env python
# -*- coding: utf-8 -*-
import config
import processing
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import json
from threading import Thread

bot = telebot.TeleBot(config.token, threaded = False) #bot and its atributes declaration
markup = InlineKeyboardMarkup()
markup.add(InlineKeyboardButton("Удалить", callback_data="delete"))

@bot.message_handler(commands=['about'])
def main_void(message):
    s = "Привет, я бот! Моя задача - распознавать в тексте суммы денег и переводить их в нужные валюты. Это может значительно упростить вам общение." + "\n" + "Авторы:" + "\n" + "@vladikko" + "\n" + "@volkovskey" + "\n"+ "Версия: 1.0.1"
    bot.send_message(message.chat.id, s)

@bot.message_handler(content_types=["text", "photo"])
def main_void(message):
    #Printing information about input message
    print("")
    print("******************************")
    print("Username: " + str(message.chat.username) + ", ID: " + str(message.chat.id))
    print("")
    print("Message: " + str(message.text))
    print(message.chat)
    
    #Select the text that will be processed: a text message, or a description of the photo
    if message.content_type == "photo":
        mes = message.caption
    else:
        mes = message.text
    
    #To simplify processing, translate the message into lowercase
    mes = mes.lower()

    #Splitting the text of the message into the necessary components
    mes_ar = processing.special_split(mes)
    
    #Checking for commands from the bot
    if mes_ar[0] == "-help" or mes_ar[0] == "-h": #It`s information about main commands and functional
        bot.reply_to(message, "Тут текст сообщения")
    elif mes_ar[0] == "-settings" or mes_ar[0] == "-s": #It`s settings for bot: list of currency, timer for delete message, tun on/off button "delete" and etc
        can_user_edit_settings = False #It`s var shows whether a person can control the bot 
        if message.chat.all_members_are_administrators != True: #Checking for the type of chat administration: all admins, or specific people
            us_id = message.from_user.id #Get person`s ID
            user = bot.get_chat_member(message.chat.id, us_id) #Get information about person
            if user.status == "administrator" or user.status == "creator": #Check for admin/creator
                can_user_edit_settings = True
            else:
                bot.reply_to(message, "У тебя нет право на это")
        else:
            can_user_edit_settings = True
        if can_user_edit_settings:
            bot.reply_to(message, "Настройки появятся в ближайшем будущем")
    #
    p = processing.search_numbers_and_vaults(mes_ar)
    if p != [[],[]]:
        SnV=processing.search(mes_ar, p)
        print(SnV)
        if SnV != [[],[]]:
            output=""
            i = 0
            while i < len(SnV[0]):
                print(i)
                output=output+ "======" + "\n" + processing.output(SnV, i)
                i += 1
            try:
                bot.reply_to(message, output, reply_markup=markup)
            except:
                print("Error")
            print("Answer: ")
            print(output)
    elif message.chat.type == "private":
        bot.reply_to(message,"Эта валюта отсутствует в базе данных",reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def cb_answer(call):
    can_user_delete_message = False #It`s var shows whether a person can control the bot 
    if call.message.chat.all_members_are_administrators != True: #Checking for the type of chat administration: all admins, or specific people
        us_id = call.from_user.id #Get person`s ID
        user = bot.get_chat_member(call.message.chat.id, us_id) #Get information about person
        if user.status == "administrator" or user.status == "creator": #Check for admin/creator
            can_user_delete_message = True
        else:
            print("Access denied")
    else:
        can_user_delete_message = True
    if can_user_delete_message:
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except:
            print("Error")
        
              
if __name__ == '__main__':
    #config.update_exchange_rate()
    thread_main = Thread(target=bot.infinity_polling, args=(True,))
    thread_main.start()
    thread_exchange_rate = Thread(target=config.schedule_update)
    thread_exchange_rate.start()
