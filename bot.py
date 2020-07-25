#!/usr/bin/env python
# -*- coding: utf-8 -*-
import config
import processing
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentType
from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from threading import Thread

bot = Bot(token=config.token) #bot and its atributes declaration
dp = Dispatcher(bot)
markup = InlineKeyboardMarkup()
markup.add(InlineKeyboardButton("Удалить", callback_data="delete"))

@dp.message_handler(commands=['about'])
async def main_void(message: types.Message):
    about_c_file = open("texts/about_command.ertb")
    about_c_text = about_c_file.read()
    await message.reply(about_c_text,reply_markup = markup)

@dp.message_handler(commands=['help'])
async def main_void(message: types.Message):
    help_c_file = open("texts/help_command.ertb")
    help_c_text = help_c_file.read()
    await message.reply(help_c_text,reply_markup = markup)

@dp.message_handler(content_types=ContentType.TEXT or ContentType.PHOTO)
async def main_void(message: types.Message):
    #Printing information about input message
    print("")
    print("******************************")
    print("Username: " + str(message.from_user.username) + ", ID: " + str(message.chat.id)+ ", Chat: "+str(message.chat.title))
    print("")
    print("Message: " + str(message.text))

    #statistics
    try:
        if message.chat.is_private():
            file_with_list_of_id = open("logs/id_private.ertb")
        else:
            file_with_list_of_id = open("logs/id_groups.ertb")
        list_of_id = file_with_list_of_id.readlines()
        for i in range(len(list_of_id) - 1):
            list_of_id[i] = list_of_id[i][0:len(list_of_id[i]) - 1]
        if str(message.chat.id) in list_of_id:
            print("fdg")
        else:
            file_with_list_of_id.close()
            if message.chat.is_private():
                file_with_list_of_id = open("logs/id_private.ertb", "w")
            else:
                file_with_list_of_id = open("logs/id_groups.ertb", "w")
            for i in range(len(list_of_id)):
                file_with_list_of_id.write(str(list_of_id[i]) + "\n")
            file_with_list_of_id.write(str(message.chat.id))
        file_with_list_of_id.close()
    except:
        print("Error")
    
    #Select the text that will be processed: a text message, or a description of the photo
    #if message.content_type() is ContentType.PHOTO:
    #    mes = message.caption
    #else:
        mes = message.text
    
    #To simplify processing, translate the message into lowercase
    mes = mes.lower()

    #Splitting the text of the message into the necessary components
    mes_ar = processing.special_split(mes)
    
    #Checking for commands from the bot
    try:
        if mes_ar[0] == "-help" or mes_ar[0] == "-h": #It`s information about main commands and functional
            help_file = open("texts/help.ertb")
            help_text = help_file.read()
            await message.reply(help_text,reply_markup = markup)
        elif mes_ar[0] == "-settings" or mes_ar[0] == "-s": #It`s settings for bot: list of currency, timer for delete message, tun on/off button "delete" and etc
            can_user_edit_settings = False #It`s var shows whether a person can control the bot 
            if message.chat.all_members_are_administrators != True: #Checking for the type of chat administration: all admins, or specific people
                if message.chat.get_member(message.from_user.id).is_chat_admin(): #Check for admin/creator
                    can_user_edit_settings = True
                else:
                    await message.reply("У тебя нет право на это",reply_markup = markup)
            else:
                can_user_edit_settings = True
            if can_user_edit_settings:
                await message.reply("Настройки появятся в ближайшем будущем",reply_markup = markup)
        elif mes_ar[0] == "-stats":
            if str(message.chat_id) in config.creator_id:
                file_with_list_of_id = open("logs/id_private.ertb")
                list_of_id = file_with_list_of_id.readlines()
                len_private = len(list_of_id)
                file_with_list_of_id.close()
                file_with_list_of_id = open("logs/id_groups.ertb")
                list_of_id = file_with_list_of_id.readlines()
                len_groups = len(list_of_id)
                file_with_list_of_id.close()
                answer = "ЛС: " + str(len_private) + "\n" + "Группы: " + str(len_groups)
                await message.reply(answer,reply_markup = markup)
    except:
        print("Error")
    #
    p = processing.search_numbers_and_vaults(mes_ar)
    if p != [[],[]]:
        SnV=processing.search(mes_ar, p)
        print(SnV)
        if SnV != [[],[]]:
            output=""
            i = 0
            while i < len(SnV[0]):
                print(i)
                output=output+ "======" + "\n" + processing.output(SnV, i)
                i += 1
            try:
                await message.reply(output,reply_markup = markup)
            except:
                print("Error")
            print("Answer: ")
            print(output)
    elif message.chat.type == "private":
        await message.reply("Эта валюта отсутствует в базе данных",reply_markup = markup)


@dp.callback_query_handler(lambda call: True)
async def cb_answer(call: types.CallbackQuery):
    can_user_delete_message = False #It`s var shows whether a person     can control the bot 
    print(call.message.chat.all_members_are_administrators)
    if call.message.chat.all_members_are_administrators == None:
        can_user_delete_message = True
    elif call.message.chat.all_members_are_administrators != True: #Checking for the type of chat administration: all admins, or specific people
        if call.message.chat.get_member(call.from_user.id).is_chat_admin(): #Check for admin/creator
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
        

if __name__ == '__main__':
    #config.update_exchange_rate()
    thread_main = Thread(target=executor.start_polling, args=(dp,))
    thread_main.start()
    thread_exchange_rate = Thread(target=config.schedule_update)
    thread_exchange_rate.start()
