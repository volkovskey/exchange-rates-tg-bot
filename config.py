#!/usr/bin/env python
# -*- coding: utf-8 -*-
from SpecialPrint import Print
import xmltodict
import urllib3
import time

def schedule_update():
    global exchange_rates
    while True:
        exchange_rates = update_exchange_rate()
        time.sleep(7200)

def update_exchange_rate():
    url = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange"
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    try:
        data = xmltodict.parse(response.data)
    except:
        Print("Failed to parse xml from response (%s)" %traceback.format_exc())
    exchange_rates_temp = {}
    for rate in data['exchange']['currency']:
        try:
            exchange_rates_temp[rate['cc']] = float(rate['rate'])
        except:
            Print("Couldnt parse part of exchange rates")
    return exchange_rates_temp.copy()

creator_id = ["348826721", "361240585"] #Here you need to enter the ID of the person / chat who will have access to statistics

# made global to avoid futher confusion
ar_vault = [["манат", "₼"],
            ["белрубл"],
            ["франк", "₣"],
            ["юан", "жэньминьби"],
            ["евро", "€"],
            ["крон", "Kč"],
            ["фунт", "£"],
            ["лари", "₾"],
            ["шекел", "₪"],
            ["рупи", "₹"],
            ["вон", "₩", "원", "元", "圓s"],
            ["тенге", "₸"],
            ["рубл", "₽"],
            ["злот", "zł"],
            ["грн", "гривн", "гривен", "₴"],
            ["доллар", "бакс", "бачей", "зелен", "$"],
            ["сума", "суму", "сумо", "сумы", "сума", "сўм"]]
ar_vault_s = [["azn"],
            ["byn", "бр"],
            ["chf"],
            ["cny", "rmb"],
            ["czk"],
            ["eur"],
            ["gbp"],
            ["gel"],
            ["ils"],
            ["inr"],
            ["krw"],
            ["kzt", "тг", "тнг"],
            ["rub", "rur", "руб", "р."],
            ["plz", "pln", "зл"],
            ["uah"],
            ["usd", "дол", "долл"],
            ["uzs", "сум"]]
cur_dict = [['AZN', 'BYN', 'CHF', 'CNY', 'CZK', 'EUR', 'GBP', 'GEL', 'ILS', 'INR', 'KRW', 'KZT', 'RUB', 'PLN', 'UAH', 'USD', 'UZS'],
            ["🇦🇿", "🇧🇾", "🇨🇭", "🇨🇳", "🇨🇿", "🇪🇺", "🇬🇧", "🇬🇪", "🇮🇱", "🇮🇳", "🇰🇷", "🇰🇿", "🇷🇺", "🇵🇱", "🇺🇦", "🇺🇸", "🇺🇿"]]
_eng_chars = u"~!@#$%^&qwertyuiop[]asdfghjkl;'zxcvbnm,./QWERTYUIOP{}ASDFGHJKL:\"|ZXCVBNM<>?"
_rus_chars = u"ё!\"№;%:?йцукенгшщзхъфывапролджэячсмитьбю.ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭ/ЯЧСМИТЬБЮ,"
 
def fix_layout(s):
    for i in range(len(s)):
        if s[i] in _eng_chars:
            index = _eng_chars.find(s[i])
            s = s[0:i] + _rus_chars[index] + s[i + 1:len(s)]
        elif s[i] in _rus_chars:
            index = _rus_chars.find(s[i])
            s = s[0:i] + _eng_chars[index] + s[i + 1:len(s)]
    return s