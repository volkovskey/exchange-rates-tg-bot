#!/usr/bin/env python
# -*- coding: utf-8 -*-
import config

def special_split(s):
    s = s.replace("\n", ",") #Replace hyphenation with comma

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
        if a[i] == "к" and a[i - 1][0].isdigit(): #2.5к = 2500
            a[i - 1] = str(float(a[i - 1]) * 1000)
            del a[i]
        elif a[i] == "кк" and a[i - 1][0].isdigit(): #2.5кк = 2500000
            a[i - 1] = str(float(a[i - 1]) * 1000000)
            del a[i]
        i -= 1
    print("")
    print("Result array:")
    print(a)
    return a

def search_numbers_and_vaults(l):
    r = [] #содержит индексы местонахождения
    t = [] #содержит номера валют
    i = 0
    j = 0
    while i < len(config.ar_vault):
        while j < len(config.ar_vault[i]):
            for u in range(len(l)):
                if l[u].find(config.ar_vault[i][j]) != -1:
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
    suma.reverse()
    for i in range(len(m[1])):
        m[1][i] = config.cur_dict[m[1][i]]
    answ_ar = [suma, m[1]]
    return answ_ar

def output(a, j):
    s=""
    money = float(a[0][j])
    s = config.flags_dict[a[1][j]] + str(money) + " " + a[1][j] + "\n"
    for i in config.cur_dict:
        if config.cur_dict[i] == a[1][j]:
            pass
        elif config.cur_dict[i] == "UAH" and a[1][j] != "UAH":
            ua = round(money * (config.exchange_rates[a[1][j]]), 2)
            s = s + "\n" + config.flags_dict["UAH"] + str(ua) + " UAH"
        elif a[1][j] != "UAH":
            val = round(money * (config.exchange_rates[a[1][j]]/config.exchange_rates[config.cur_dict[i]]), 2)
            s = s + "\n" + config.flags_dict[config.cur_dict[i]] + str(val) + " " + config.cur_dict[i]
        else:
            val = round(money * (1/config.exchange_rates[config.cur_dict[i]]), 2)
            s = s + "\n" + config.flags_dict[config.cur_dict[i]] + str(val) + " " + config.cur_dict[i]
    return s