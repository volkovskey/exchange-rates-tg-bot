#!/usr/bin/env python
# -*- coding: utf-8 -*-
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import config
import check_and_search
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
    print(message.text)
    s = check_and_search.delete_space(message)
    #print(s)
    if check_and_search.check_for_numbers(s):
        #print("Nums is ok")
        h = check_and_search.check_vault(s)
        print(h)
        if h != [[],[]]:
            #print("V is ok")
            output=""
            for currency in range(len(h[0])):
                sum = check_and_search.search(s, h[0][currency])
                #print(sum)
                output=output+ "======" + "\n"+check_and_search.change_vaults(sum, h[1][currency])
            bot.send_message(message.chat.id,output)
            print("Answer: ")
            print(output)
        else:
            print("no vaults")
    else:
        print("no numbers")
    print("=================")





if __name__ == '__main__':
    #config.update_exchange_rate()
    thread_main = Thread(target=bot.infinity_polling, args=(True,))
    thread_main.start()
    thread_exchange_rate = Thread(target=config.schedule_update)
    thread_exchange_rate.start()