import os
import config

default_cur = ["RUB", "USD", "EUR"]

def create_data(chat_id, chat_type):
    path = "settings/" + str(chat_id) + ".ertb"
    currency = []
    for i in config.cur_dict:
        currency.append(config.cur_dict[i])
    settings = dict.fromkeys(currency, False)
    for i in default_cur:
        settings[i] = True
    if chat_type != "private":
        settings["delete"] = "admins" #creator, admins, sender, everybody
        settings["delete_button"] = True
        settings["edit"] = "admins" #creator, admins, everybody
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
