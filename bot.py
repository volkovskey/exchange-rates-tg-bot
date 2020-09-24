#!/usr/bin/env python
# -*- coding: utf-8 -*-
import config
import processing
import dbhelper
import ertb_stats
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentType
from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from threading import Thread
import csv
import time
import datetime
import os
import random
import zipfile

#убрать баги +
#перенести статистику в отдельный файл +
#добавить настройки удаления +
#добавить количество активных групп и личек -
#добавить автопостройку графиков -
#сделать автоматический бэкап -

#добавить перевод -
#добавить крипту -
#добавить inline функционал -

#добавить донат -

bot = Bot(token=config.token) #bot and its atributes declaration
dp = Dispatcher(bot)

markup = InlineKeyboardMarkup()
markup.add(InlineKeyboardButton("Удалить", callback_data="delete"))

settings_markup = InlineKeyboardMarkup()
settings_markup.add(InlineKeyboardButton("Настройка валют", callback_data="cur"))
settings_markup.add(InlineKeyboardButton("Настройка кнопки удаления", callback_data="delbut_"))
settings_markup.add(InlineKeyboardButton("Настройка прав", callback_data="edit"))
settings_markup.add(InlineKeyboardButton("Удалить", callback_data="delete"))

private_markup = InlineKeyboardMarkup()
private_markup.add(InlineKeyboardButton("Настройка валют", callback_data="cur"))
private_markup.add(InlineKeyboardButton("Настройка кнопки удаления", callback_data="delbut_"))
private_markup.add(InlineKeyboardButton("Удалить", callback_data="delete"))

@dp.message_handler(commands=['echo'])
async def main_void(message: types.Message):
    if str(message.chat.id) in config.creator_id:
        text = (message.text).replace("/echo ", "")
        sent_msg = 0
        file_id = open("logs/id_private.ertb")
        list_id = file_id.readlines()
        for i in list_id:
            try:
                await bot.send_message(i, text)
                print("Sent "+str(sent_msg)+" messages")
                sent_msg+=1
            except:
                print("An error occured while sending message")
            time.sleep(random.choice([1,2,3]))
        file_id.close()
        file_id = open("logs/id_groups.ertb")
        list_id = file_id.readlines()
        for i in list_id:
            try:
                await bot.send_message(i, text)
                print("Sent "+str(sent_msg)+" messages")
                sent_msg+=1
            except:
                print("An error occured while sending message")
            time.sleep(random.choice([1,2,3]))
        file_id.close()

@dp.message_handler(commands=['about'])
async def main_void(message: types.Message):
    ertb_stats.check_chat(message)
    about_file = open("texts/about.ertb")
    about_text = about_file.read()
    if dbhelper.get_set(message.chat.id, "delete_button"):
        await message.reply(about_text, reply_markup = markup)
    else:
        await message.reply(about_text)

@dp.message_handler(commands=['help'])
async def main_void(message: types.Message):
    ertb_stats.check_chat(message)
    help_file = open("texts/help.ertb")
    help_text = help_file.read()
    if dbhelper.get_set(message.chat.id, "delete_button"):
        await message.reply(help_text, reply_markup = markup)
    else:
        await message.reply(help_text)

@dp.message_handler(commands=['settings'])
async def main_void(message: types.Message):
    ertb_stats.check_chat(message)
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
            await message.reply("Выберите необходимый пункт настроек", reply_markup = private_markup)

@dp.message_handler(commands=['stats'])
async def main_void(message: types.Message):
    if str(message.chat.id) in config.creator_id:
        #Количество чатов
        answer = "ЛС: " + str(ertb_stats.chat_count("private")) + "\n" + "Группы: " + str(ertb_stats.chat_count("groups"))
        await message.reply(answer)
        
        #статистика по включенным валютам
        cur_count_array = []
        for i in config.cur_dict:
            cur_count_array.append(config.cur_dict[i])
        cur_count = dict.fromkeys(cur_count_array, 0)
        cur_count_groups = dict.fromkeys(cur_count_array, 0)
        cur_count_private = dict.fromkeys(cur_count_array, 0)
        

        file_id = open("logs/id_private.ertb")
        list_id = file_id.readlines()
        file_id.close()
        file_id = open("logs/id_groups.ertb")
        list_id = list_id + file_id.readlines()
        file_id.close()
        for a in range(len(list_id)):
            list_id[a] = list_id[a].replace("\n","")
            i = list_id[a]
            set_dict = dbhelper.get_dict(i)
            for j in cur_count:
                if set_dict[j]:
                    cur_count[j] += 1
                    if i[0] == "-":
                        cur_count_groups[j] += 1
                    else:
                        cur_count_private[j] += 1
        
        answer = "Все чаты\n"
        for i in cur_count:
            answer += str(i) + ": " + str(cur_count[i]) + "\n"
        await message.reply(answer)

        answer = "Групповые чаты\n"
        for i in cur_count:
            answer += str(i) + ": " + str(cur_count_groups[i]) + "\n"
        await message.reply(answer)

        answer = "Личные чаты\n"
        for i in cur_count:
            answer += str(i) + ": " + str(cur_count_private[i]) + "\n"
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

@dp.message_handler(commands=['wrong'])
async def main_void(message: types.Message):
    ertb_stats.check_chat(message)
    try:
        today = datetime.datetime.today()
        dt = today.strftime("%Y-%m-%d-%H.%M.%S")
        try:
            path = "reports/" + dt + ".txt"
        except:
            os.mkdir("reports")
            path = "reports/" + dt + ".txt"
        report = open(path, 'w')
        msg_text = message.reply_to_message.text
        if message.photo or message.video is not None or message.document is not None:
            msg_text = message.reply_to_message.caption
        report.write(msg_text)
        report.close()
    except:
        text = "Команду надо отправлять в ответ на сообщение, которое бот ошибочно распознал."
        if dbhelper.get_set(message.chat.id, "delete_button"):
            await message.reply(text, reply_markup = markup)
        else:
            await message.reply(text)

@dp.message_handler(commands=['backup'])
async def main_void(message: types.Message):
    if str(message.chat.id) in config.creator_id:
        zip_arch = zipfile.ZipFile('backup.zip', 'w')

        directory = 'logs'
        list_files = os.listdir(directory)
        for i in list_files:
            path = directory + "/" + i
            try:
                zip_arch.write(path)
            except:
                answer = "Ошибка добавления. Файл " + i + " пустой или не найден." 
                print(answer)
        directory = 'settings'
        list_files = os.listdir(directory)
        for i in list_files:
            path = directory + "/" + i
            try:
                zip_arch.write(path)
            except:
                answer = "Ошибка добавления. Файл " + i + " пустой или не найден." 
                print(answer)
        zip_arch.close()
        path = "backup.zip"
        report_file = open(path, 'rb')
        await bot.send_document(message.chat.id, report_file)
        os.remove(path)

@dp.message_handler(commands=['reports'])
async def main_void(message: types.Message):
    if str(message.chat.id) in config.creator_id:
        directory = 'reports'
        list_files = os.listdir(directory)
        zip_arch = zipfile.ZipFile('logs/reports.zip', 'w')
        for i in list_files:
            path = directory + "/" + i
            try:
                zip_arch.write(path)
            except:
                answer = "Ошибка добавления. Файл " + i + " пустой или не найден." 
                print(answer)
        zip_arch.close()
        path = "logs/reports.zip"
        report_file = open(path, 'rb')
        await bot.send_document(message.chat.id, report_file)
        os.remove(path)

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

@dp.message_handler(commands=['start'])
async def main_void(message: types.Message):
    if message.chat.type == "private":
        ertb_stats.check_chat(message)
        await message.reply("Вы можете настроить валюты или начать пользоваться ботом", reply_markup = private_markup)

@dp.message_handler(content_types=ContentType.ANY)
async def main_void(message: types.Message):
    msg_text = message.text
    if message.photo or message.video is not None or message.document is not None:
        msg_text = message.caption

    if msg_text is None or msg_text == "":
        return

    #Printing information about input message
    print("")
    print("******************************")
    print("Username: " + str(message.from_user.username) + ", ID: " + str(message.chat.id)+ ", Chat: "+str(message.chat.title))
    print("")
    print("Message: " + str(msg_text))

    #statistics
    ertb_stats.check_chat(message)
    
    #To simplify processing, translate the message into lowercase
    mes = msg_text.lower()

    #Splitting the text of the message into the necessary components
    mes_ar = processing.special_split(mes)
    
    try:
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
                    ertb_stats.update_rec_logs(SnV[1][i], str(message.chat.type))
                    output=output + "\n" + "======" + "\n" + processing.output(SnV, i, dbhelper.get_dict(message.chat.id))
                    i += 1
                try:
                    await message.reply(output,reply_markup = markup)
                except:
                    print("Error")
                print("Answer: ")
                print(output)
        elif message.chat.type == "private":
            text = "Валюта или число не обнаружены.\nПопробуйте написать '5 баксов'."
            if dbhelper.get_set(message.chat.id, "delete_button"):
                await message.reply(text, reply_markup = markup)
            else:
                await message.reply(text)
    except:
        print("Error")

@dp.callback_query_handler(lambda call: True)
async def cb_answer(call: types.CallbackQuery):
    if call.data == "delete":
        can_user_delete_message = False #It`s var shows whether a person     can control the bot 
        settings = dbhelper.get_dict(call.message.chat.id)
        rule_for_delete = settings["delete"]
        if call.message.chat.all_members_are_administrators == True or call.message.chat.type == "private":
            can_user_delete_message = True
        elif call.message.chat.all_members_are_administrators != True: #Checking for the type of chat administration: all admins, or specific people
            member = await call.message.chat.get_member(call.from_user.id)
            if rule_for_delete == "creator" and member.status == "creator":
                can_user_delete_message = True
            elif rule_for_delete == "admins" and (member.status == "administrator" or member.status == "creator"): #Check for admin/creator
                can_user_delete_message = True
            elif rule_for_delete == "everybody":
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
        edit_markup.add(InlineKeyboardButton("Назад", callback_data="settings"))
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
            edit_markup.add(InlineKeyboardButton("Назад", callback_data="settings"))
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
        cur_markup.add(InlineKeyboardButton("Назад", callback_data="settings"))
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
        cur_markup.add(InlineKeyboardButton("Назад", callback_data="settings"))
        await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=cur_markup)

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
        #enru_dict = {"creator":"Создатель", "admins":"Администраторы", "sender":"Администраторы и отправитель", "everybody":"Все участники"}
        enru_dict = {"creator":"Создатель", "admins":"Администраторы", "everybody":"Все участники"}
        settings = dbhelper.get_dict(call.message.chat.id)
        text = "Настройте кнопку удаления. Выберите категорию людей, которые смогут удалять сообщения от бота:"
        delete_markup = InlineKeyboardMarkup()

        mes_text = "Кнопка 'Удалить'"
        if settings["delete_button"]:
            mes_text += " ✅"
            call_data = "delbut_button"
            delete_markup.add(InlineKeyboardButton(mes_text, callback_data=call_data))
            if call.message.chat.type != "private":
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
        delete_markup.add(InlineKeyboardButton("Назад", callback_data="settings"))
        await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=delete_markup)

    elif call.data == "settings":
        text = "Выберите необходимый пункт настроек"
        if call.message.chat.type != "private":
            await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=settings_markup)
        else:
            await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=private_markup)
    

def assignment_of_settings():
    directory = 'settings'
    try:
        list_files = os.listdir(directory)
    except:
        os.mkdir("settings")
        list_files = os.listdir(directory)
    
    file_id = open("logs/id_private.ertb")
    list_id = file_id.readlines()
    file_id.close()
    file_id = open("logs/id_groups.ertb")
    list_id = list_id + file_id.readlines()
    file_id.close()
    for a in range(len(list_id)):
        list_id[a] = list_id[a].replace("\n","")
        i = list_id[a]
        filename = i + ".ertb"
        if filename in list_files:
            settings = dbhelper.get_dict(i)
            for j in config.cur_dict:
                try:
                    a = settings[config.cur_dict[j]]
                except:
                    dbhelper.change_value(i, config.cur_dict[j], False)
            if filename[0] == "-":
                file_with_default = open("logs/settings_groups.ertb")
            else:
                file_with_default = open("logs/settings_private.ertb")
            default_settings = file_with_default.readlines()
            for j in range(len(default_settings)):
                default_settings[j] = default_settings[j].replace("\n", "")
                index = default_settings[j].find(" ")
                key = default_settings[j][0:index]
                value = default_settings[j][index + 1:]
                try:
                    a = settings[key]
                except:
                    dbhelper.change_value(i, key, value)
        else:
            if filename[0] == "-":
                dbhelper.create_data(i, "group")
            else:
                dbhelper.create_data(i, "private")

if __name__ == '__main__':
    #config.update_exchange_rate()
    thread_main = Thread(target=executor.start_polling, args=(dp,))
    thread_main.start()
    thread_exchange_rate = Thread(target=config.schedule_update)
    thread_exchange_rate.start()
    thread_stats = Thread(target=ertb_stats.bot_stats)
    thread_stats.start()
    assignment_of_settings()