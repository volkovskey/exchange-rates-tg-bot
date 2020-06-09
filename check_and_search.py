#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import telebot
import config
def search(str2, h):
    vault = config.ar_vault[h]
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
    elif str2[index - 1] == 'к' and str2[index - 2].isdigit():
        str3 = str2[0:index - 1] + "000" + str2[index:len(str2) + 1]
        str2 = str3
        index = str3.find(vault)
        last = index
        first = 0
        m = 1
        j = True
        while j:
            if str3[index - m].isdigit():
                m = m + 1
                j = True
            else:
                j = False
                first = index - m + 1
    #print(str2[last:])
    return int(str2[first:last])

def change_vaults(money, h):
    s=""
    print(config.exchange_rates)
    if h == 1 or h == 3 or h == 7:
        #print(type(money))
        ua = round(money * (config.exchange_rates['RUB']), 2)
        en = round(money * (config.exchange_rates['RUB']/config.exchange_rates['USD']), 2)
        s = str(money) + " RUB:" + "\n" + "\n" + "-" + str(ua) + " UAH" + "\n" + "-" + str(en) + " USD" + "\n"
    elif h == 0 or h == 2:
        #print("ua")
        ru = round(money * (1/config.exchange_rates['RUB']), 2)
        en = round(money * (1/config.exchange_rates['USD']), 2)
        s = str(money) + " UAH:" + "\n" + "\n" + "-" + str(ru) + " RUB" + "\n" + "-" + str(en) + " USD" + "\n"
    elif h == 4 or h == 5 or h == 6:
        #print("en")
        ru = round(money * config.exchange_rates['USD']/config.exchange_rates['RUB'], 2)
        ua = round(money * config.exchange_rates['USD'], 2)
        s = str(money) + " USD:" + "\n" + "\n" + "-" + str(ru) + " RUB" + "\n" + "-" + str(ua) + " UAH" + "\n"
    return s

def delete_space(message):
    s = message.text
    s = s.replace(' ', '')
    return s    

def check_for_numbers(r):
    k = False
    for i in r:
        if i.isdigit():
            k = True
            break
    return k

def check_vault(str1):
    r = [] #contain all currencies that were found in message
    for cur in range(len(config.ar_vault)):
        if str1.find(config.ar_vault[cur]) != -1:
            r.append(cur)
    return r