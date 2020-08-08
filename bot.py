#!/usr/bin/env python
# -*- coding: utf-8 -*-
import config
import processing
import dbhelper
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentType
from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from threading import Thread
import csv
import time
import datetime
import os

bot = Bot(token=config.token) #bot and its atributes declaration
dp = Dispatcher(bot)

markup = InlineKeyboardMarkup()
markup.add(InlineKeyboardButton("Удалить", callback_data="delete"))

settings_markup = InlineKeyboardMarkup()
settings_markup.add(InlineKeyboardButton("Настройка валют", callback_data="cur"))
#settings_markup.add(InlineKeyboardButton("Настройка кнопки удаления", callback_data="delete_button"))
settings_markup.add(InlineKeyboardButton("Настройка прав", callback_data="edit"))
settings_markup.add(InlineKeyboardButton("Удалить", callback_data="delete"))

@dp.message_handler(commands=['echo'])
async def main_void(message: types.Message):
    if str(message.chat.id) in config.creator_id:
        text = (message.text).replace("/echo ", "")
        file_id = open("logs/id_private.ertb")
        list_id = file_id.readlines()
        for i in list_id:
            await bot.send_message(i, text)
        file_id.close()
        file_id = open("logs/id_groups.ertb")
        list_id = file_id.readlines()
        for i in list_id:
            await bot.send_message(i, text)
        file_id.close()

@dp.message_handler(commands=['about'])
async def main_void(message: types.Message):
    about_file = open("texts/about.ertb")
    about_text = about_file.read()
    if message.chat.type != "private":
        await message.reply(about_text, reply_markup = markup)
    else:
        await message.reply(about_text)

@dp.message_handler(commands=['help'])
async def main_void(message: types.Message):
    help_file = open("texts/help.ertb")
    help_text = help_file.read()
    if message.chat.type != "private":
        await message.reply(help_text, reply_markup = markup)
    else:
        await message.reply(help_text)

@dp.message_handler(commands=['settings'])
async def main_void(message: types.Message):
    settings = dbhelper.get_dict(str(message.chat.id))
    can_user_edit_settings = False #It`s var shows whether a person can control the bot 
    if message.chat.all_members_are_administrators != True and message.chat.type != "private": #Checking for the type of chat administration: all admins, or specific people
        member = await message.chat.get_member(message.from_user.id)
        if settings["edit"] == "creator" and member.status == "creator":
            can_user_edit_settings = True
        elif settings["edit"] == "admins" and (member.status == "creator" or member.status == "administrator"):
            can_user_edit_settings = True
        elif settings["edit"] == "everybody":
            can_user_edit_settings = True
        else:
            await message.reply("У тебя нет право на это", reply_markup = markup)
    else:
        can_user_edit_settings = True
    if can_user_edit_settings:
        if message.chat.type != "private":
            await message.reply("Выберите необходимый пункт настроек", reply_markup = settings_markup)
        else:
            await message.reply("Настройки появятся в ближайшем будущем")

@dp.message_handler(commands=['stats'])
async def main_void(message: types.Message):
    if str(message.chat.id) in config.creator_id:
        file_id = open("logs/id_private.ertb")
        list_id = file_id.readlines()
        len_private = len(list_id)
        file_id.close()
        file_id = open("logs/id_groups.ertb")
        list_id = file_id.readlines()
        len_groups = len(list_id)
        file_id.close()
        answer = "ЛС: " + str(len_private) + "\n" + "Группы: " + str(len_groups)
        await message.reply(answer)

@dp.message_handler(commands=['logs'])
async def main_void(message: types.Message):
    if str(message.chat.id) in config.creator_id:
        directory = 'logs'
        list_files = os.listdir(directory)
        for i in list_files:
            path = directory + '/' + i
            files = open(path, 'rb')
            try:
                await bot.send_document(message.chat.id, files)
            except:
                answer = "Ошибка отправки. Файл " + i + " пустой или не найден." 
                await message.reply(answer)

@dp.message_handler(commands=['report'])
async def main_void(message: types.Message):
    try:
        today = datetime.datetime.today()
        dt = today.strftime("%Y-%m-%d-%H.%M.%S")
        path = "reports/" + dt
        report = open(path, 'w')
        report.write(message.reply_to_message.text)
        report.close()
    except:
        await message.reply("Команду надо отправлять в ответ на сообщение, которое бот ошибочно распознал.")

@dp.message_handler(commands=['reports'])
async def main_void(message: types.Message):
    if str(message.chat.id) in config.creator_id:
        directory = 'reports'
        list_files = os.listdir(directory)
        for i in list_files:
            path = directory + '/' + i
            files = open(path, 'rb')
            try:
                await bot.send_document(message.chat.id, files)
            except:
                answer = "Ошибка отправки. Файл " + i + " пустой или не найден." 
                await message.reply(answer)

@dp.message_handler(commands=['delete_reports'])
async def main_void(message: types.Message):
    if str(message.chat.id) in config.creator_id:
        directory = 'reports'
        list_files = os.listdir(directory)
        for i in list_files:
            path = directory + '/' + i
            try:
                os.remove(path)
            except:
                print("Error delete")

@dp.message_handler(content_types=ContentType.TEXT or ContentType.PHOTO or ContentType.VIDEO)
async def main_void(message: types.Message):
    #Printing information about input message
    print("")
    print("******************************")
    print("Username: " + str(message.from_user.username) + ", ID: " + str(message.chat.id)+ ", Chat: "+str(message.chat.title))
    print("")
    print("Message: " + str(message.text))

    #statistics
    try:
        if message.chat.type == "private":
            file_id = open("logs/id_private.ertb")
        else:
            file_id = open("logs/id_groups.ertb")
        list_id = file_id.readlines()
        for i in range(len(list_id) - 1):
            list_id[i] = list_id[i][0:len(list_id[i]) - 1]
        if str(message.chat.id) in list_id:
            pass
        else:
            file_id.close()
            if message.chat.type == "private":
                file_id = open("logs/id_private.ertb", "w")
            else:
                file_id = open("logs/id_groups.ertb", "w")
            for i in range(len(list_id)):
                file_id.write(str(list_id[i]) + "\n")
            file_id.write(str(message.chat.id))

            #settings
            dbhelper.create_data(str(message.chat.id), str(message.chat.type))
        file_id.close()
    except:
        print("Error stats")
    
    mes = message.text
    
    #To simplify processing, translate the message into lowercase
    mes = mes.lower()

    #Splitting the text of the message into the necessary components
    mes_ar = processing.special_split(mes)
    
    try:
        #Checking for commands from the bot
        k = False
        for i in range(len(mes_ar)):
            if mes_ar[i][0].isdigit():
                k = True
                break
        if k:
            p = processing.search_numbers_and_vaults(mes_ar)
        else:
            p = [[],[]]
        if p != [[],[]]:
            SnV=processing.search(mes_ar, p)
            print(SnV)
            if SnV != [[],[]]:
                output = ""
                i = 0
                while i < len(SnV[0]):
                    print(i)
                    output=output + "\n" + "======" + "\n" + processing.output(SnV, i, dbhelper.get_dict(message.chat.id))
                    i += 1
                try:
                    if message.chat.type != "private":
                        await message.reply(output,reply_markup = markup)
                    else:
                        await message.reply(output)
                except:
                    print("Error")
                print("Answer: ")
                print(output)
        elif message.chat.type == "private":
            await message.reply("Валюта или число не обнаружены.\nПопробуйте написать '5 баксов'.")
    except:
        print("Error")

@dp.callback_query_handler(lambda call: True)
async def cb_answer(call: types.CallbackQuery):
    if call.data == "delete":
        can_user_delete_message = False #It`s var shows whether a person     can control the bot 
        if call.message.chat.all_members_are_administrators == True:
            can_user_delete_message = True
        elif call.message.chat.all_members_are_administrators != True: #Checking for the type of chat administration: all admins, or specific people
            member = await call.message.chat.get_member(call.from_user.id)
            if member.status == "administrator" or member.status == "creator": #Check for admin/creator
                can_user_delete_message = True
            else:
                print("Access denied")
        else:
            can_user_delete_message = True
        if can_user_delete_message:
            try:
                await call.message.delete()
            except:
                print("Error")
    elif call.data == "edit":
        enru_dict = {"creator":"Создатель", "admins":"Администраторы", "everybody":"Все участники"}
        settings = dbhelper.get_dict(call.message.chat.id)
        text = "Выберите категорию людей, которые смогут изменять настройки бота:"
        edit_markup = InlineKeyboardMarkup()

        for i in enru_dict:
            mes_text = enru_dict[i]
            if settings["edit"] == i:
                mes_text += " ✅"
            else:
                mes_text += " ❌"
            call_data = "edit_" + i
            edit_markup.add(InlineKeyboardButton(mes_text, callback_data=call_data))
        edit_markup.add(InlineKeyboardButton("Удалить", callback_data="delete"))
        await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=edit_markup)
    elif str(call.data).find("edit") == 0:
        settings = dbhelper.get_dict(call.message.chat.id)
        index = str(call.data).find("_") + 1
        value = str(call.data)[index:len(str(call.data))]
        if value != settings["edit"]:
            dbhelper.change_value(call.message.chat.id, "edit", value)
            enru_dict = {"creator":"Создатель", "admins":"Администраторы", "everybody":"Все участники"}
            settings = dbhelper.get_dict(call.message.chat.id)
            text = "Выберите категорию людей, которые смогут изменять настройки бота:"
            edit_markup = InlineKeyboardMarkup()

            for i in enru_dict:
                mes_text = enru_dict[i]
                if settings["edit"] == i:
                    mes_text += " ✅"
                else:
                    mes_text += " ❌"
                call_data = "edit_" + i
                edit_markup.add(InlineKeyboardButton(mes_text, callback_data=call_data))
            edit_markup.add(InlineKeyboardButton("Удалить", callback_data="delete"))
            await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=edit_markup)
    elif call.data == "cur":
        settings = dbhelper.get_dict(call.message.chat.id)
        text = "Настройте валюту для перевода."
        cur_markup = InlineKeyboardMarkup()
        for i in config.flags_dict:
            mes_text = config.flags_dict[i] + i
            if settings[i]:
                mes_text += " ✅"
            else:
                mes_text += " ❌"
            call_data = "cur_" + i
            cur_markup.add(InlineKeyboardButton(mes_text, callback_data=call_data))
        cur_markup.add(InlineKeyboardButton("Удалить", callback_data="delete"))
        await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=cur_markup)

    elif str(call.data).find("cur") == 0:
        index = str(call.data).find("_") + 1
        key = str(call.data)[index:len(str(call.data))]
        settings = dbhelper.get_dict(call.message.chat.id)
        dbhelper.change_value(call.message.chat.id, key, not settings[key])
        settings = dbhelper.get_dict(call.message.chat.id)
        text = "Настройте валюту для перевода."
        cur_markup = InlineKeyboardMarkup()
        for i in config.flags_dict:
            mes_text = config.flags_dict[i] + i
            if settings[i]:
                mes_text += " ✅"
            else:
                mes_text += " ❌"
            call_data = "cur_" + i
            cur_markup.add(InlineKeyboardButton(mes_text, callback_data=call_data))
        cur_markup.add(InlineKeyboardButton("Удалить", callback_data="delete"))
        await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=cur_markup)

    elif call.data == "delete_button":
        enru_dict = {"creator":"Создатель", "admins":"Администраторы", "sender":"Администраторы и отправитель", "everybody":"Все участники"}
        settings = dbhelper.get_dict(call.message.chat.id)
        text = "Настройте кнопку удаления. Выберите категорию людей, которые смогут удалять сообщения от бота:"
        delete_markup = InlineKeyboardMarkup()

        mes_text = "Кнопка 'Удалить'"
        if settings["delete_button"]:
            mes_text += " ✅"
            call_data = "delbut_button"
            delete_markup.add(InlineKeyboardButton(mes_text, callback_data=call_data))
            for i in enru_dict:
                mes_text = enru_dict[i]
                if settings["delete"] == i:
                    mes_text += " ✅"
                else:
                    mes_text += " ❌"
                call_data = "delbut_" + i
                delete_markup.add(InlineKeyboardButton(mes_text, callback_data=call_data))
        else:
            mes_text += " ❌"
            call_data = "delbut_button"
            delete_markup.add(InlineKeyboardButton(mes_text, callback_data=call_data))
        delete_markup.add(InlineKeyboardButton("Удалить", callback_data="delete"))
        await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=delete_markup)

    elif str(call.data).find("delbut_") == 0:
        index = str(call.data).find("_") + 1
        value = str(call.data)[index:len(str(call.data))]
        if value == "button":
            settings = dbhelper.get_dict(call.message.chat.id)
            dbhelper.change_value(call.message.chat.id, "delete_button", not settings["delete_button"])
            settings = dbhelper.get_dict(call.message.chat.id)
        else:
            settings = dbhelper.get_dict(call.message.chat.id)
            dbhelper.change_value(call.message.chat.id, "delete", value)
            settings = dbhelper.get_dict(call.message.chat.id)
        enru_dict = {"creator":"Создатель", "admins":"Администраторы", "sender":"Администраторы и отправитель", "everybody":"Все участники"}
        settings = dbhelper.get_dict(call.message.chat.id)
        text = "Настройте кнопку удаления. Выберите категорию людей, которые смогут удалять сообщения от бота:"
        delete_markup = InlineKeyboardMarkup()

        mes_text = "Кнопка 'Удалить'"
        if settings["delete_button"]:
            mes_text += " ✅"
            call_data = "delbut_button"
            delete_markup.add(InlineKeyboardButton(mes_text, callback_data=call_data))
            for i in enru_dict:
                mes_text = enru_dict[i]
                if settings["delete"] == i:
                    mes_text += " ✅"
                else:
                    mes_text += " ❌"
                call_data = "delbut_" + i
                delete_markup.add(InlineKeyboardButton(mes_text, callback_data=call_data))
        else:
            mes_text += " ❌"
            call_data = "delbut_button"
            delete_markup.add(InlineKeyboardButton(mes_text, callback_data=call_data))
        delete_markup.add(InlineKeyboardButton("Удалить", callback_data="delete"))
        await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=delete_markup)

def bot_stats():
    while True:
        with open('logs/stats.csv') as f:
            reader = csv.reader(f)
            data_list = list(reader)
        try:
            file_id = open("logs/id_private.ertb")
            list_id = file_id.readlines()
            len_private = len(list_id)
            file_id.close()
            file_id = open("logs/id_groups.ertb")
            list_id = file_id.readlines()
            len_groups = len(list_id)
            file_id.close()
            now = datetime.datetime.now()
            m=[str(now), len_private, len_groups]
            data_list.append(m)
            with open('logs/stats.csv', 'w') as f:
                writer = csv.writer(f)
                for row in data_list:
                    writer.writerow(row)
        except:
            print("Error")
        time.sleep(86400)
        
def assignment_of_settings():
    directory = 'settings'
    list_files = os.listdir(directory)

    file_id = open("logs/id_private.ertb")
    list_id = file_id.readlines()
    file_id.close()
    for i in list_id:
        filename = i[0:len(i) - 2] + ".ertb"
        if filename in list_files:
            settings = dbhelper.get_dict(i[0:len(i) - 2])
            for j in config.cur_dict:
                try:
                    a = settings[config.cur_dict[j]]
                except:
                    dbhelper.change_value(i[0:len(i) - 2], config.cur_dict[j], False)
        else:
            dbhelper.create_data(i, "private")
    
    file_id = open("logs/id_groups.ertb")
    list_id = file_id.readlines()
    file_id.close()
    for i in list_id:
        filename = i[0:len(i) - 2] + ".ertb"
        if filename in list_files:
            settings = dbhelper.get_dict(i[0:len(i) - 2])
            for j in config.cur_dict:
                try:
                    a = settings[config.cur_dict[j]]
                except:
                    dbhelper.change_value(i[0:len(i) - 2], config.cur_dict[j], False)
        else:
            dbhelper.create_data(i, "group")

if __name__ == '__main__':
    #config.update_exchange_rate()
    thread_main = Thread(target=executor.start_polling, args=(dp,))
    thread_main.start()
    thread_exchange_rate = Thread(target=config.schedule_update)
    thread_exchange_rate.start()
    thread_stats = Thread(target=bot_stats)
    thread_stats.start()
    assignment_of_settings()
