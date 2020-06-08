#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import telebot
import config

def search(str2, h):
    ar_vault = ["грн", "руб", "гривен", "р.", "дол", "бакс"]
    vault = ar_vault[h]
    index = str2.find(vault)
    if str2[index - 1].isdigit():
        last = index
        first = 0
        m = 1
        j = True
        while j:
            if str2[index - m].isdigit():
                m = m + 1
                j = True
            else:
                j = False
                first = index - m + 1
    return int(str2[first:last])

def change_vaults(money, h, message, bot):
    #ar_vault = ["грн", "руб", "гривен", "р.", "дол", "бакс"]
    if h == 1 or h == 3:
        #print(type(money))
        ua = round(money * 0.39, 2)
        en = round(money * 0.015, 2)
        s = str(money) + " руб. = " + str(ua) + " грн или " + str(en) + " $"
        bot.send_message(message.chat.id, s)
    elif h == 0 or h == 2:
        #print("ua")
        ru = round(money * 2.57, 2)
        en = round(money * 0.038, 2)
        s = str(money) + " грн. = " + str(ru) + " руб или " + str(en) + " $"
        bot.send_message(message.chat.id, s)
    elif h == 4 or h == 5:
        #print("en")
        ru = round(money * 68.32, 2)
        ua = round(money * 26.58, 2)
        s = str(money) + " дол. = " + str(ru) + " руб или " + str(ua) + " грн."
        bot.send_message(message.chat.id, s)

def delete_space(message):
    s = message.text
    s = s.replace(' ', '')
    return s    

def check_for_numbers(r):
    k = False
    for i in range(0, len(r)):
        if r[i].isdigit():
            k = True
            break
    return k

def check_vault(str1):
    r = -1
    if str1.find("грн") != -1:
        r = 0
    elif str1.find("руб") != -1:
        r = 1
    elif str1.find("гривен") != -1:
        r = 2
    elif str1.find("р.") != -1:
        r = 3
    elif str1.find("дол") != -1:
        r = 4
    elif str1.find("бакс") != -1:
        r = 5
    return r