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
    return int(str2[first:last])

def change_vaults(money, h):
    s=""
    print(config.exchange_rates)
    if h == 1 or h == 3 or h == 7 or 14 <= h <= 17:
        ua = round(money * (config.exchange_rates['RUB']), 2)
        en = round(money * (config.exchange_rates['RUB']/config.exchange_rates['USD']), 2)
        eu = round(money * (config.exchange_rates['RUB']/config.exchange_rates['EUR']), 2)
        bl = round(money * (config.exchange_rates['RUB']/config.exchange_rates['BYN']), 2)
        pl = round(money * (config.exchange_rates['RUB']/config.exchange_rates['PLZ']), 2)
        s = "🇷🇺" + str(money) + " RUB:" + "\n" + "\n" + "🇺🇦" + str(ua) + " UAH" + "\n" + "🇺🇸" + str(en) + " USD" + "\n" + "🇪🇺" + str(eu) + " EUR" + "\n" + "🇧🇾" + str(bl) + " BYN" + "\n" + "🇵🇱" + str(pl) + " PLN" + "\n"
    elif h == 0 or h == 2 or h == 8 or h == 9:
        ru = round(money * (1/config.exchange_rates['RUB']), 2)
        en = round(money * (1/config.exchange_rates['USD']), 2)
        eu = round(money * (1/config.exchange_rates['EUR']), 2)
        bl = round(money * (1/config.exchange_rates['BYN']), 2)
        pl = round(money * (1/config.exchange_rates['PLZ']), 2)
        s = "🇺🇦" + str(money) + " UAH:" + "\n" + "\n" + "🇷🇺" + str(ru) + " RUB" + "\n" + "🇺🇸" + str(en) + " USD" + "\n" + "🇪🇺" + str(eu) + " EUR" + "\n" + "🇧🇾" + str(bl) + " BYN" + "\n" + "🇵🇱" + str(pl) + " PLN" + "\n"
    elif h == 4 or h == 5 or h == 6 or h == 19:
        ru = round(money * config.exchange_rates['USD']/config.exchange_rates['RUB'], 2)
        ua = round(money * config.exchange_rates['USD'], 2)
        eu = round(money * config.exchange_rates['USD']/config.exchange_rates['EUR'], 2)
        pl = round(money * config.exchange_rates['USD']/config.exchange_rates['PLZ'], 2)
        bl = round(money * config.exchange_rates['USD']/config.exchange_rates['BYN'], 2)
        s = "🇺🇸" + str(money) + " USD:" + "\n" + "\n" + "🇷🇺" + str(ru) + " RUB" + "\n" + "🇺🇦" + str(ua) + " UAH" + "\n"  + "🇪🇺" + str(eu) + " EUR" + "\n" + "🇧🇾" + str(bl) + " BYN" + "\n" + "🇵🇱" + str(pl) + " PLN" + "\n"
    elif h == 20 or h == 18 or h == 13 or h == 12:
        ru = round(money * config.exchange_rates['EUR']/config.exchange_rates['RUB'], 2)
        ua = round(money * config.exchange_rates['EUR'], 2)
        en = round(money * config.exchange_rates['EUR']/config.exchange_rates['USD'], 2)
        pl = round(money * config.exchange_rates['EUR']/config.exchange_rates['PLZ'], 2)
        bl = round(money * config.exchange_rates['EUR']/config.exchange_rates['BYN'], 2)
        s = "🇪🇺" + str(money) + " EUR:" + "\n" + "\n" + "🇷🇺" + str(ru) + " RUB" + "\n" + "🇺🇦" + str(ua) + " UAH" + "\n"  + "🇺🇸" + str(en) + " USD" + "\n" + "🇧🇾" + str(bl) + " BYN" + "\n" + "🇵🇱" + str(pl) + " PLN" + "\n"
    elif h == 21 or h == 22:
        ru = round(money * config.exchange_rates['BYN']/config.exchange_rates['RUB'], 2)
        ua = round(money * config.exchange_rates['BYN'], 2)
        en = round(money * config.exchange_rates['BYN']/config.exchange_rates['USD'], 2)
        en = round(money * config.exchange_rates['BYN']/config.exchange_rates['EUR'], 2)
        pl = round(money * config.exchange_rates['BYN']/config.exchange_rates['PLZ'], 2)
        s = "🇧🇾" + str(money) + " BYN:" + "\n" + "\n" + "🇷🇺" + str(ru) + " RUB" + "\n" + "🇺🇦" + str(ua) + " UAH" + "\n"  + "🇺🇸" + str(en) + " USD" + "\n" + "🇪🇺" + str(bl) + " EUR" + "\n" + "🇵🇱" + str(pl) + " PLN" + "\n"
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