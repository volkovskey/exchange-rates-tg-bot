#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import telebot
import config

def special_split(s):
    while s.find("  ") != -1:
        s = s.replace("  ", " ")
    
    a = []
    start = 0
    end = 0
    for i in range(len(s)):
        if s[i] == " ":
            end = i
            a.append(s[start:end])
            start = end + 1
        elif i == len(s) - 1:
            end = len(s)
            a.append(s[start:end])
        elif s[i].isdigit() and s[i + 1].isalpha():
            end = i + 1
            a.append(s[start:end])
            start = end
        elif s[i].isalpha() and s[i + 1].isdigit():
            end = i + 1
            a.append(s[start:end])
            start = end
    #print(a)
    return a

def search_numbers_and_vaults(l):
    k = False
    for i in range(len(l)):
        if l[i][0].isdigit():
            k = True
            break
    if k:
        r = [] #содержит индексы местонахождения
        t = [] #содержит номера валют
        cur = 0
        while cur < len(config.ar_vault):
            for u in range(len(l)):
                if l[u].find(config.ar_vault[cur]) != -1:
                    r.append(u)
                    t.append(cur)
            cur = cur + 1
            #print(cur)
        m = [r, t]
        print(m)
    return m

def search(a, m):
    suma = []
    currency = []
    i = len(m[0]) - 1
    while i >= 0:
        e = m[0][i]
        if e == len(a) - 1 and a[len(a) - 2][0].isdigit():
            suma.append(a[e - 1])
            currency.append(change_vault(m[1][i]))
        elif a[e + 1][0].isdigit():
            suma.append(a[e + 1])
            currency.append(change_vault(m[1][i]))
        elif a[e - 1][0].isdigit():
            suma.append(a[e - 1])
            currency.append(change_vault(m[1][i]))
        i -= 1
    answ_ar = [suma, currency]
    return answ_ar

def check_k(a):
    i = len(a) - 1
    while i > 0:
        if a[i] == "к" and a[i - 1][0].isdigit():
            if a[i].find(",") != -1:
                a[i] = a[i].replace(",", ".")
            a[i] = str(float(a[i - 1]) * 1000)
        i -= 1
    return a


def output(a, i):
    s=""
    #print(config.exchange_rates)
    money = float(a[0][i])
    if a[1][i] == "RU":
        print("Started convert")
        ua = round(money * (config.exchange_rates['RUB']), 2)
        en = round(money * (config.exchange_rates['RUB']/config.exchange_rates['USD']), 2)
        eu = round(money * (config.exchange_rates['RUB']/config.exchange_rates['EUR']), 2)
        bl = round(money * (config.exchange_rates['RUB']/config.exchange_rates['BYN']), 2)
        pl = round(money * (config.exchange_rates['RUB']/config.exchange_rates['PLZ']), 2)
        s = "🇷🇺" + str(money) + " RUB:" + "\n" + "\n" + "🇺🇦" + str(ua) + " UAH" + "\n" + "🇺🇸" + str(en) + " USD" + "\n" + "🇪🇺" + str(eu) + " EUR" + "\n" + "🇧🇾" + str(bl) + " BYN" + "\n" + "🇵🇱" + str(pl) + " PLN" + "\n"
    elif a[1][i] == "UA":
        ru = round(money * (1/config.exchange_rates['RUB']), 2)
        en = round(money * (1/config.exchange_rates['USD']), 2)
        eu = round(money * (1/config.exchange_rates['EUR']), 2)
        bl = round(money * (1/config.exchange_rates['BYN']), 2)
        pl = round(money * (1/config.exchange_rates['PLZ']), 2)
        s = "🇺🇦" + str(money) + " UAH:" + "\n" + "\n" + "🇷🇺" + str(ru) + " RUB" + "\n" + "🇺🇸" + str(en) + " USD" + "\n" + "🇪🇺" + str(eu) + " EUR" + "\n" + "🇧🇾" + str(bl) + " BYN" + "\n" + "🇵🇱" + str(pl) + " PLN" + "\n"
    elif a[1][i] == "US":
        print("Started convert")
        ru = round(money * config.exchange_rates['USD']/config.exchange_rates['RUB'], 2)
        ua = round(money * config.exchange_rates['USD'], 2)
        eu = round(money * config.exchange_rates['USD']/config.exchange_rates['EUR'], 2)
        pl = round(money * config.exchange_rates['USD']/config.exchange_rates['PLZ'], 2)
        bl = round(money * config.exchange_rates['USD']/config.exchange_rates['BYN'], 2)
        s = "🇺🇸" + str(money) + " USD:" + "\n" + "\n" + "🇷🇺" + str(ru) + " RUB" + "\n" + "🇺🇦" + str(ua) + " UAH" + "\n"  + "🇪🇺" + str(eu) + " EUR" + "\n" + "🇧🇾" + str(bl) + " BYN" + "\n" + "🇵🇱" + str(pl) + " PLN" + "\n"
    elif a[1][i] == "EU":
        ru = round(money * config.exchange_rates['EUR']/config.exchange_rates['RUB'], 2)
        ua = round(money * config.exchange_rates['EUR'], 2)
        en = round(money * config.exchange_rates['EUR']/config.exchange_rates['USD'], 2)
        pl = round(money * config.exchange_rates['EUR']/config.exchange_rates['PLZ'], 2)
        bl = round(money * config.exchange_rates['EUR']/config.exchange_rates['BYN'], 2)
        s = "🇪🇺" + str(money) + " EUR:" + "\n" + "\n" + "🇷🇺" + str(ru) + " RUB" + "\n" + "🇺🇦" + str(ua) + " UAH" + "\n"  + "🇺🇸" + str(en) + " USD" + "\n" + "🇧🇾" + str(bl) + " BYN" + "\n" + "🇵🇱" + str(pl) + " PLN" + "\n"
    elif a[1][i] == "BY":
        ru = round(money * config.exchange_rates['BYN']/config.exchange_rates['RUB'], 2)
        ua = round(money * config.exchange_rates['BYN'], 2)
        en = round(money * config.exchange_rates['BYN']/config.exchange_rates['USD'], 2)
        eu = round(money * config.exchange_rates['BYN']/config.exchange_rates['EUR'], 2)
        pl = round(money * config.exchange_rates['BYN']/config.exchange_rates['PLZ'], 2)
        s = "🇧🇾" + str(money) + " BYN:" + "\n" + "\n" + "🇷🇺" + str(ru) + " RUB" + "\n" + "🇺🇦" + str(ua) + " UAH" + "\n"  + "🇺🇸" + str(en) + " USD" + "\n" + "🇪🇺" + str(eu) + " EUR" + "\n" + "🇵🇱" + str(pl) + " PLN" + "\n"
    elif a[1][i] == "PL":
        ru = round(money * config.exchange_rates['PLZ']/config.exchange_rates['RUB'], 2)
        ua = round(money * config.exchange_rates['PLZ'], 2)
        en = round(money * config.exchange_rates['PLZ']/config.exchange_rates['USD'], 2)
        eu = round(money * config.exchange_rates['PLZ']/config.exchange_rates['EUR'], 2)
        bl = round(money * config.exchange_rates['PLZ']/config.exchange_rates['BYN'], 2)
        s = "🇵🇱" + str(money) + " PLN:" + "\n" + "\n" + "🇷🇺" + str(ru) + " RUB" + "\n" + "🇺🇦" + str(ua) + " UAH" + "\n"  + "🇺🇸" + str(en) + " USD" + "\n" + "🇪🇺" + str(eu) + " EUR" + "\n" + "🇧🇾" + str(bl) + " BYN" + "\n"
    return s


def change_vault(h):
    v = ""
    if h == 1 or h == 3 or h == 7 or 14 <= h <= 17:
        v = "RU"
    elif h == 0 or h == 2 or h == 8 or h == 9 or h == 23:
        v = "UA"
    elif h == 4 or h == 5 or h == 6 or h == 19 or h == 10 or h == 11:
        v = "US"
    elif h == 20 or h == 18 or h == 13 or h == 12:
        v = "EU"
    elif h == 21 or h == 22 or h == 29:
        v = "BY"
    elif 24 <= h <= 28:
        v = "PL"
    print("Change vault is ok")
    return v

