#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xmltodict
import urllib3
from datetime import date
import time
exchange_rates={}


def update_exchange_rate():
    while 1:
        print("Exchange rate update started!")
        url = "https://api.privatbank.ua/p24api/exchange_rates?date="+date.today().strftime("%d.%m.%Y")
        http = urllib3.PoolManager()
        response = http.request('GET', url)
        try:
            data = xmltodict.parse(response.data)
        except:
            print("Failed to parse xml from response (%s)" % traceback.format_exc())
        print(data['exchangerates']['exchangerate'][0])
        exchange_rates = {}
        for rate in data['exchangerates']['exchangerate']:
            try:
                exchange_rates[rate['@currency']]=float(rate['@saleRateNB'])
            except:
                print("couldnt parse part of exchange rates")
        print(exchange_rates)
        time.sleep(43200)

#update_exchange_rate()
token = '1182364187:AAG7PjbZoOKikc0JTEI9MTaMAX2YEW432II'
ar_vault = ["грн", "руб", "гривен", "р.", "дол", "бакс","$","₽"] #made global to avoid futher confusion