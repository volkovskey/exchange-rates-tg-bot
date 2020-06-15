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
        elif s[i].isdigit() and not s[i + 1].isdigit() and s[i + 1] != " " and s[i + 1] != "." and s[i + 1] != ",":
            end = i + 1
            a.append(s[start:end])
            start = end
        elif not s[i].isdigit() and s[i + 1].isdigit() and s[i] != " " and s[i] != "," and s[i] != ".":
            end = i + 1
            a.append(s[start:end])
            start = end
    for i in range(len(a)):
        if a[i][0].isdigit():
            if a[i].find(",") != -1:
                a[i] = a[i].replace(",", ".")
    print(a)
    
    i = len(a) - 1
    while i > 0:
        if a[i] == "к" and a[i - 1][0].isdigit():
            a[i - 1] = str(float(a[i - 1]) * 1000)
            del a[i]
        elif a[i] == "кк" and a[i - 1][0].isdigit():
            a[i - 1] = str(float(a[i - 1]) * 1000000)
            del a[i]
        i -= 1
    #print(a)
    return a

def search_numbers_and_vaults(l):
    for i in range(len(l)):
        if l[i][0].isdigit():
            k = True
    if k:
        r = [] #содержит индексы местонахождения
        t = [] #содержит номера валют
        i = 0
        j = 0
        while i < len(config.ar_vault):
            while j < len(config.ar_vault[i]):
                for u in range(len(l)):
                    if l[u].find(config.ar_vault[i][j]) != -1:
                        if u != len(l) - 1 and u != 0:
                            if l[u + 1].isdigit():
                                r.append(u)
                                t.append(i)
                            elif l[u - 1].isdigit():
                                r.append(u)
                                t.append(i)
                        elif u == len(l) - 1 and l[u - 1].isdigit():
                            r.append(u)
                            t.append(i)
                        elif u == 0 and l[u + 1].isdigit():
                            r.append(u)
                            t.append(i)
                j += 1
            i += 1
            j = 0
        i = 0
        j = 0
        while i < len(config.ar_vault_s):
            while j < len(config.ar_vault_s[i]):
                for u in range(len(l)):
                    if l[u] == config.ar_vault_s[i][j]:
                        if u != len(l) - 1 and u != 0:
                            if l[u + 1].isdigit():
                                r.append(u)
                                t.append(i)
                            elif l[u - 1].isdigit():
                                r.append(u)
                                t.append(i)
                        elif u == len(l) - 1 and l[u - 1].isdigit():
                            r.append(u)
                            t.append(i)
                        elif u == 0 and l[u + 1].isdigit():
                            r.append(u)
                            t.append(i)
                j += 1
            i += 1
            j = 0
        m = [r, t]
        print(m)
    return m

def search(a, m):
    suma = []
    i = len(m[0]) - 1
    while i >= 0:
        e = m[0][i]
        if e == len(a) - 1 and a[len(a) - 2][0].isdigit():
            suma.append(a[e - 1])
        elif a[e + 1][0].isdigit():
            suma.append(a[e + 1])
        elif a[e - 1][0].isdigit():
            suma.append(a[e - 1])
        i -= 1
    answ_ar = [suma, m[1]]
    return answ_ar


def output(a, i):
    s=""
    #print(config.exchange_rates)
    money = float(a[0][i])
    if a[1][i] == 1:
        print("Started convert")
        ua = round(money * (config.exchange_rates['RUB']), 2)
        en = round(money * (config.exchange_rates['RUB']/config.exchange_rates['USD']), 2)
        eu = round(money * (config.exchange_rates['RUB']/config.exchange_rates['EUR']), 2)
        bl = round(money * (config.exchange_rates['RUB']/config.exchange_rates['BYN']), 2)
        pl = round(money * (config.exchange_rates['RUB']/config.exchange_rates['PLN']), 2)
        s = "🇷🇺" + str(money) + " RUB:" + "\n" + "\n" + "🇺🇦" + str(ua) + " UAH" + "\n" + "🇺🇸" + str(en) + " USD" + "\n" + "🇪🇺" + str(eu) + " EUR" + "\n" + "🇧🇾" + str(bl) + " BYN" + "\n" + "🇵🇱" + str(pl) + " PLN" + "\n"
    elif a[1][i] == 0:
        ru = round(money * (1/config.exchange_rates['RUB']), 2)
        en = round(money * (1/config.exchange_rates['USD']), 2)
        eu = round(money * (1/config.exchange_rates['EUR']), 2)
        bl = round(money * (1/config.exchange_rates['BYN']), 2)
        pl = round(money * (1/config.exchange_rates['PLN']), 2)
        s = "🇺🇦" + str(money) + " UAH:" + "\n" + "\n" + "🇷🇺" + str(ru) + " RUB" + "\n" + "🇺🇸" + str(en) + " USD" + "\n" + "🇪🇺" + str(eu) + " EUR" + "\n" + "🇧🇾" + str(bl) + " BYN" + "\n" + "🇵🇱" + str(pl) + " PLN" + "\n"
    elif a[1][i] == 2:
        print("Started convert")
        ru = round(money * config.exchange_rates['USD']/config.exchange_rates['RUB'], 2)
        ua = round(money * config.exchange_rates['USD'], 2)
        eu = round(money * config.exchange_rates['USD']/config.exchange_rates['EUR'], 2)
        pl = round(money * config.exchange_rates['USD']/config.exchange_rates['PLN'], 2)
        bl = round(money * config.exchange_rates['USD']/config.exchange_rates['BYN'], 2)
        s = "🇺🇸" + str(money) + " USD:" + "\n" + "\n" + "🇷🇺" + str(ru) + " RUB" + "\n" + "🇺🇦" + str(ua) + " UAH" + "\n"  + "🇪🇺" + str(eu) + " EUR" + "\n" + "🇧🇾" + str(bl) + " BYN" + "\n" + "🇵🇱" + str(pl) + " PLN" + "\n"
    elif a[1][i] == 3:
        ru = round(money * config.exchange_rates['EUR']/config.exchange_rates['RUB'], 2)
        ua = round(money * config.exchange_rates['EUR'], 2)
        en = round(money * config.exchange_rates['EUR']/config.exchange_rates['USD'], 2)
        pl = round(money * config.exchange_rates['EUR']/config.exchange_rates['PLN'], 2)
        bl = round(money * config.exchange_rates['EUR']/config.exchange_rates['BYN'], 2)
        s = "🇪🇺" + str(money) + " EUR:" + "\n" + "\n" + "🇷🇺" + str(ru) + " RUB" + "\n" + "🇺🇦" + str(ua) + " UAH" + "\n"  + "🇺🇸" + str(en) + " USD" + "\n" + "🇧🇾" + str(bl) + " BYN" + "\n" + "🇵🇱" + str(pl) + " PLN" + "\n"
    elif a[1][i] == 5:
        ru = round(money * config.exchange_rates['BYN']/config.exchange_rates['RUB'], 2)
        ua = round(money * config.exchange_rates['BYN'], 2)
        en = round(money * config.exchange_rates['BYN']/config.exchange_rates['USD'], 2)
        eu = round(money * config.exchange_rates['BYN']/config.exchange_rates['EUR'], 2)
        pl = round(money * config.exchange_rates['BYN']/config.exchange_rates['PLN'], 2)
        s = "🇧🇾" + str(money) + " BYN:" + "\n" + "\n" + "🇷🇺" + str(ru) + " RUB" + "\n" + "🇺🇦" + str(ua) + " UAH" + "\n"  + "🇺🇸" + str(en) + " USD" + "\n" + "🇪🇺" + str(eu) + " EUR" + "\n" + "🇵🇱" + str(pl) + " PLN" + "\n"
    elif a[1][i] == 4:
        ru = round(money * config.exchange_rates['PLN']/config.exchange_rates['RUB'], 2)
        ua = round(money * config.exchange_rates['PLN'], 2)
        en = round(money * config.exchange_rates['PLN']/config.exchange_rates['USD'], 2)
        eu = round(money * config.exchange_rates['PLN']/config.exchange_rates['EUR'], 2)
        bl = round(money * config.exchange_rates['PLN']/config.exchange_rates['BYN'], 2)
        s = "🇵🇱" + str(money) + " PLN:" + "\n" + "\n" + "🇷🇺" + str(ru) + " RUB" + "\n" + "🇺🇦" + str(ua) + " UAH" + "\n"  + "🇺🇸" + str(en) + " USD" + "\n" + "🇪🇺" + str(eu) + " EUR" + "\n" + "🇧🇾" + str(bl) + " BYN" + "\n"
    return s

