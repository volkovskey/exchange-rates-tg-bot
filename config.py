#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xmltodict
import urllib3
import time

def schedule_update():
    global exchange_rates
    while True:
        exchange_rates = update_exchange_rate()
        time.sleep(43200)

def update_exchange_rate():
    print("Exchange rate update started!")
    url = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange"
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    try:
        data = xmltodict.parse(response.data)
    except:
        print("Failed to parse xml from response (%s)" %traceback.format_exc())
    exchange_rates_temp = {}
    for rate in data['exchange']['currency']:
        try:
            exchange_rates_temp[rate['cc']] = float(rate['rate'])
        except:
            print("couldnt parse part of exchange rates")
    print(exchange_rates_temp)
    
    return exchange_rates_temp.copy()

#update_exchange_rate()
token = '' #here your token
creator_id = "no" #Here you need to enter the ID of the person / chat who will have access to statistics
# made global to avoid futher confusion
ar_vault = [["грн", "гривн", "гривен", "₴"],
            ["rur", "рубль", "рубля", "рублю", "рублём", "рублем", "рубли", "рублей", "рублям", "рублях", "₽"],
            ["доллар", "бакс", "бачей", "зелен", "$"],
            ["евро", "€"],
            ["злотый", "злотого", "злотому", "злотым", "злотые", "злотых", "злотыми"],
            ["белрубль"]]
ar_vault_s = [["uah"],
            ["rub", "руб", "р"],
            ["usd", "дол", "долл"],
            ["eur"],
            ["plz", "pln", "зл",],
            ["byn", "бр",]]