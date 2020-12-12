#!/usr/bin/env python
# -*- coding: utf-8 -*-
import config

def special_split(s):
    s = s.replace("\n", ", ") #Replace hyphenation with comma

    while s.find("  ") != -1: #Removing double spaces
        s = s.replace("  ", " ")

    s = s.replace(",", ".") #comma to dot

    a = [] #The main array to which the result will be written
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
        elif not s[i].isdigit() and s[i + 1] == "." or not s[i].isdigit() and s[i + 1] == "/": #separating letters from symbols
            end = i + 1
            a.append(s[start:end])
            start = end
        elif s[i].isdigit() and not s[i + 1].isdigit() and s[i + 1] != " " and s[i + 1] != ".": #separating a digit from a letter
            end = i + 1
            a.append(s[start:end])
            start = end
        elif not s[i].isdigit() and s[i + 1].isdigit() and s[i] != " " and s[i] != ".": #separating a letter from a digit
            end = i + 1
            a.append(s[start:end])
            start = end
    
    i = len(a) - 1
    while i > 0:
        if (a[i] == "к" or a[i] == "k") and a[i - 1][0].isdigit(): #2.5к = 2500
            a[i - 1] = str(float(a[i - 1]) * 1000)
            del a[i]
        elif (a[i] == "кк" or a[i] == "kk") and a[i - 1][0].isdigit(): #2.5кк = 2500000
            a[i - 1] = str(float(a[i - 1]) * 1000000)
            del a[i]
        elif (a[i] == "ккк" or a[i] == "kkk") and a[i - 1][0].isdigit(): #2.5ккк = 2500000000
            a[i - 1] = str(float(a[i - 1]) * 1000000000)
            del a[i]
        i -= 1
    return a

def search_numbers_and_vaults(l):
    r = [] #содержит индексы местонахождения
    t = [] #содержит номера валют
    i = 0
    j = 0
    while i < len(config.ar_vault):
        while j < len(config.ar_vault[i]):
            for u in range(len(l)):
                if l[u].find(config.ar_vault[i][j]) == 0:
                    if u != len(l) - 1 and u != 0:
                        if l[u + 1][0].isdigit():
                            r.append(u)
                            t.append(i)
                        elif l[u - 1][0].isdigit():
                            r.append(u)
                            t.append(i)
                    elif u == len(l) - 1 and l[u - 1][0].isdigit():
                        r.append(u)
                        t.append(i)
                    elif u == 0 and l[u + 1][0].isdigit():
                        r.append(u)
                        t.append(i)

                if len(r)>=50:
                    return [[],[]]
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
                        if l[u + 1][0].isdigit():
                            r.append(u)
                            t.append(i)
                        elif l[u - 1][0].isdigit():
                            r.append(u)
                            t.append(i)
                    elif u == len(l) - 1 and l[u - 1][0].isdigit():
                        r.append(u)
                        t.append(i)
                    elif u == 0 and l[u + 1][0].isdigit():
                        r.append(u)
                        t.append(i)
                if len(r)>=50:
                    return [[],[]]
            j += 1
        i += 1
        j = 0
    
    suma = []
    i = len(r) - 1
    while i >= 0:
        e = r[i]
        if e == len(l) - 1 and l[len(l) - 2][0].isdigit():
            suma.append(l[e - 1])
        elif l[e + 1][0].isdigit():
            suma.append(l[e + 1])
        elif l[e - 1][0].isdigit():
            suma.append(l[e - 1])
        i -= 1
    suma.reverse()
    answ_ar = [suma, t]
    return answ_ar

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
    suma.reverse()
    for i in range(len(m[1])):
        m[1][i] = config.cur_dict[0][m[1][i]]
    answ_ar = [suma, m[1]]
    return answ_ar

def output(a, j, settings):
    s=""
    cur = a[1][j]
    money = float(a[0][j])
    s = config.cur_dict[1][cur] + str(money) + " " + config.cur_dict[0][cur] + "\n"
    for i in range(len(config.cur_dict[0])):
        if config.cur_dict[0][i] == config.cur_dict[0][cur]:
            pass
        elif config.cur_dict[0][i] == 'UAH' and config.cur_dict[0][cur] != 'UAH' and settings['UAH']:
            ua = round(money * (config.exchange_rates[config.cur_dict[0][cur]]), 2)
            s = s + "\n" + config.cur_dict[1][i] + str(ua) + " UAH"
        elif config.cur_dict[0][cur] != 'UAH' and settings[config.cur_dict[0][i]]:
            val = round(money * (config.exchange_rates[config.cur_dict[0][cur]]/config.exchange_rates[config.cur_dict[0][i]]), 2)
            s = s + "\n" + config.cur_dict[1][i] + str(val) + " " + config.cur_dict[0][i]
        elif settings[config.cur_dict[0][i]]:
            val = round(money * (1/config.exchange_rates[config.cur_dict[0][i]]), 2)
            s = s + "\n" + config.cur_dict[1][i] + str(val) + " " + config.cur_dict[0][i]
    if config.cur_dict[0][cur] == 'UAH' and money == 40.0:
        s += "\n👖1 штаны"
    elif config.cur_dict[0][cur] == 'USD' and money == 22062012.0:
        s += "\n"
        s += "<code>_________ _______  _______  _        _______ " + "\n"
        s += "\__   __/(  ____ \(  ____ \( \      (  ___  )" + "\n"
        s += "   ) (   | (    \/| (    \/| (      | (   ) |" + "\n"
        s += "   | |   | (__    | (_____ | |      | (___) |" + "\n"
        s += "   | |   |  __)   (_____  )| |      |  ___  |" + "\n"
        s += "   | |   | (            ) || |      | (   ) |" + "\n"
        s += "   | |   | (____/\/\____) || (____/\| )   ( |" + "\n"
        s += "   )_(   (_______/\_______)(_______/|/     \|</code>" + "\n"
    return s