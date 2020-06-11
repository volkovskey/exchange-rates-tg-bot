#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xmltodict
import urllib3
from datetime import date, timedelta
import time


def schedule_update():
    global exchange_rates
    while True:
        exchange_rates = update_exchange_rate()
        time.sleep(43200)


def update_exchange_rate():
    print("Exchange rate update started!")
    url = "https://api.privatbank.ua/p24api/exchange_rates?date=" + \
        date.today().strftime("%d.%m.%Y")
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    try:
        data = xmltodict.parse(response.data)
    except:
        print("Failed to parse xml from response (%s)" %
              traceback.format_exc())
    try:
        check = data['exchangerates']['exchangerate'][0]
    except:
        url = "https://api.privatbank.ua/p24api/exchange_rates?date=" + \
            (date.today()-timedelta(days=1)).strftime("%d.%m.%Y")
        http = urllib3.PoolManager()
        response = http.request('GET', url)
        data = xmltodict.parse(response.data)

    exchange_rates_temp = {}
    for rate in data['exchangerates']['exchangerate']:
        try:
            exchange_rates_temp[rate['@currency']] = float(rate['@saleRateNB'])
        except:
            print("couldnt parse part of exchange rates")
    print(exchange_rates_temp)
    return exchange_rates_temp.copy()


#update_exchange_rate()
token = 'token'
# made global to avoid futher confusion
ar_vault = [["uah", "грн", "гривн", "гривен", "₴"],
            ["rub", "rur", "рубль", "рубля", "рублю", "рублём", "рублем", "рубли", "рублей", "рублям", "рублях", "₽"],
            ["usd", "доллар", "$"],
            ["eur", "евро", "€"],
            ["plz", "pln", "злотый", "злотого", "злотому", "злотым", "злотые", "злотых", "злотыми"],
            ["byn"]]
ar_vault_s = [[""],
            ["руб", "руб.", "р."],
            ["дол", "долл", "дол.", "долл."],
            [""],
            ["зл", "зл."],
            ["бр", "бр."]]
