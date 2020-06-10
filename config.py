#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xmltodict
import urllib3
from datetime import date
import time


def schedule_update():
    global exchange_rates
    while True:
        exchange_rates = update_exchange_rate()
        time.sleep(43200)

def update_exchange_rate():
    print("Exchange rate update started!")
    #url = "https://api.privatbank.ua/p24api/exchange_rates?date="+date.today().strftime("%d.%m.%Y")
    url = "https://api.privatbank.ua/p24api/exchange_rates?date=10.06.2020"
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    try:
        data = xmltodict.parse(response.data)
    except:
        print("Failed to parse xml from response (%s)" % traceback.format_exc())
    print(data['exchangerates']['exchangerate'][0])
    exchange_rates_temp = {}
    for rate in data['exchangerates']['exchangerate']:
        try:
            exchange_rates_temp[rate['@currency']]=float(rate['@saleRateNB'])
        except:
            print("couldnt parse part of exchange rates")
    print(exchange_rates_temp)
    return exchange_rates_temp.copy()

#update_exchange_rate()
token = '1182364187:AAG7PjbZoOKikc0JTEI9MTaMAX2YEW432II'
ar_vault = ["грн", "руб", "гривен", "р.", "дол", "бакс","$","₽", "UAH", "uah", "USD", "usd", "EUR", "eur", "RUR", "RUB", "rur", "rub", "евро", "₴", "€", "BYN", "byn", "гривна", "зл", "pln", "PLN", "plz", "PLZ", "бр"] #made global to avoid futher confusion