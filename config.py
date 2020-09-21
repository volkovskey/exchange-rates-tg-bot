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

token = '' #here your token
creator_id = ["no"] #Here you need to enter the ID of the person / chat who will have access to statistics
# made global to avoid futher confusion

ar_vault = [["грн", "гривн", "гривен", "₴"],
            ["рубл", "₽"],
            ["доллар", "бакс", "бачей", "зелен", "$"],
            ["евро", "€"],
            ["злот", "zł"],
            ["белрубл"],
            ["юан", "жэньминьби"],
            ["фунт", "£"],
            ["сум", "сўм"],
            ["лари", "₾"],
            ["тенге", "₸"],
            ["крон", "Kč"],
            ["вон", "₩", "원", "元", "圓s"],
            ["манат", "₼"]]
ar_vault_s = [["uah"],
            ["rub", "rur", "руб", "р"],
            ["usd", "дол", "долл"],
            ["eur"],
            ["plz", "pln", "зл",],
            ["byn", "бр"],
            ["cny", "rmb"],
            ["gbp"],
            ["uzs"],
            ["gel"],
            ["kzt"],
            ["czk"],
            ["krw"],
            ["azn"]]
cur_dict = {0:'UAH', 1:'RUB', 2:'USD', 3:'EUR', 4:'PLN', 5:'BYN', 6:'CNY', 7:'GBP', 8:'UZS', 9:'GEL', 10:'KZT', 11:'CZK', 12:'KRW', 13:'AZN'}
flags_dict = {'UAH':"🇺🇦", 'RUB':"🇷🇺", 'USD':"🇺🇸", 'EUR':"🇪🇺", 'PLN':"🇵🇱", 'BYN':"🇧🇾", 'CNY':"🇨🇳", 'GBP':"🇬🇧", 'UZS':"🇺🇿", 'GEL':"🇬🇪", 'KZT':"🇰🇿", 'CZK':"🇨🇿", 'KRW':"🇰🇷", 'AZN':"🇦🇿"}