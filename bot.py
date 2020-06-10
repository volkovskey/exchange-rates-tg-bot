#!/usr/bin/env python
# -*- coding: utf-8 -*-
import config
import processing
import telebot
import json
from threading import Thread

bot = telebot.TeleBot(config.token, threaded = False)

@bot.message_handler(commands=['about'])
def main_void(message):
    s = "Привет, я бот! Моя задача - распознавать в тексте суммы денег и переводить их в нужные валюты. Это может значительно упростить вам общение." + "\n" + "Авторы:" + "\n" + "@vladikko" + "\n" + "@volkovskey"
    bot.send_message(message.chat.id, s)

@bot.message_handler(content_types=["text"])
def main_void(message):
    #bot.send_message(message.chat.id, "Запуск основного метода")
    print("Message:")
    print(message.chat.id)
    print(message.text)
    
    mes = message.text
    mes = mes.lower()
    mes_ar = processing.special_split(mes)
    mes_ar = processing.check_k(mes_ar)
    print(mes_ar)
    p = processing.search_numbers_and_vaults(mes_ar)
    if p != [[],[]]:
        SnV=processing.search(mes_ar, p)
        print(SnV)
        if SnV != [[],[]]:
            output=""
            i = 0
            while i < len(SnV[0]):
                print(i)
                output=output+ "======" + "\n"+processing.output(SnV, i)
                i += 1
            bot.reply_to(message, output)
            print("Answer: ")
            print(output)
    print("=================")
    print("\n")

if __name__ == '__main__':
    #config.update_exchange_rate()
    thread_main = Thread(target=bot.infinity_polling, args=(True,))
    thread_main.start()
    thread_exchange_rate = Thread(target=config.schedule_update)
    thread_exchange_rate.start()