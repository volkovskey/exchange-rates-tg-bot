import os
import config

default_cur = ["RUB", "USD", "EUR", "UAH"]

def create_data(chat_id, chat_type):
    path = "settings/" + str(chat_id) + ".ertb"

    currency = []
    for i in config.cur_dict[0]:
        currency.append(i)
    settings = dict.fromkeys(currency, False)
    for i in default_cur:
        settings[i] = True
    
    if chat_type != "private":
        file_with_default = open("logs/settings_groups.ertb")
    else:
        file_with_default = open("logs/settings_private.ertb")
    default_settings = file_with_default.readlines()

    for i in range(len(default_settings)):
        default_settings[i] = default_settings[i].replace("\n", "")
        index = default_settings[i].find(" ")
        key = default_settings[i][0:index]
        value = default_settings[i][index + 1:]
        settings[key] = value
    file_with_default.close()
    file_dict = open(path, "w")
    file_dict.write(str(settings))
    file_dict.close()

def change_value(chat_id, key, new_value):
    path = "settings/" + str(chat_id) + ".ertb"
    file_dict = open(path)
    settings = eval(file_dict.read())
    try:
        settings[key] = new_value
        file_dict.close()
        file_dict = open(path, "w")
        file_dict.write(str(settings))
    except:
        print("Error")
    file_dict.close()

def get_dict(chat_id):
    path = "settings/" + str(chat_id) + ".ertb"
    file_dict = open(path)
    settings = eval(file_dict.read())
    return settings

def get_set(chat_id, set):
    path = "settings/" + str(chat_id) + ".ertb"
    file_dict = open(path)
    settings = eval(file_dict.read())
    return settings[set]
