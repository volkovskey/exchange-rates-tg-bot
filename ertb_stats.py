import dbhelper
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentType
import time
from datetime import datetime, timedelta
import csv

def check_chat(message):
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

def bot_stats():
    while True:
        with open('logs/stats.csv') as f:
            reader = csv.reader(f)
            data_list = list(reader)
        try:
            #записываем количество чатов
            now = datetime.now()
            m=[str(now), chat_count("private"), chat_count("groups")]
            data_list.append(m)
            new_data_list = []
            for i in range(len(data_list) - 1):
                #print(data_list[i][0])
                if str(data_list[i][0])[0:10] != str(data_list[i + 1][0])[0:10]:
                    new_data_list.append(data_list[i])
            new_data_list.append(data_list[len(data_list) - 1])
            with open('logs/stats.csv', 'w') as f:
                writer = csv.writer(f)
                for row in new_data_list:
                    writer.writerow(row)
            
            #записываем количество распознаваний за предыдущие сутки
            now = datetime.now()
            yesterday = str(now - timedelta(days=1))
            index = yesterday.find(" ")
            yesterday = yesterday[0:index]
            kol=0

            with open('logs/rec_logs.csv') as f:
                reader = csv.reader(f)
                data_list = list(reader)
            k = True
            i = len(data_list) - 1
            while k:
                index = str(data_list[i]).find(" ")
                date = str(data_list[i][0][0:10])
                if date == yesterday:
                    i -= 1
                    kol += 1
                else:
                    k = False

            with open('logs/rec_stats.csv') as f:
                reader = csv.reader(f)
                rec_stats = list(reader)
            m=[yesterday, kol]
            rec_stats.append(m)
            new_data_list = []
            for i in range(len(rec_stats) - 1):
                if len(rec_stats) == 1:
                    new_data_list.append(rec_stats[i])
                elif str(rec_stats[i][0])[0:10] != str(rec_stats[i + 1][0])[0:10]:
                    new_data_list.append(rec_stats[i])
            new_data_list.append(rec_stats[len(rec_stats) - 1])
            print(new_data_list)
            with open('logs/rec_stats.csv', 'w') as f:
                writer = csv.writer(f)
                for row in new_data_list:
                    writer.writerow(row)

        except:
            print("Error")
        time.sleep(86400)

def chat_count(type_of_chats):
    answer = 0
    if type_of_chats == "private" or type_of_chats == "all":
        file_id = open("logs/id_private.ertb")
        list_id = file_id.readlines()
        len_private = len(list_id)
        file_id.close()
        answer += len_private
    if type_of_chats == "groups" or type_of_chats == "all":
        file_id = open("logs/id_groups.ertb")
        list_id = file_id.readlines()
        len_groups = len(list_id)
        file_id.close()
        answer += len_groups
    return answer

def update_rec_logs(cur, chat_type):
    if chat_type == "private":
        with open('logs/rec_logs_private.csv') as f:
            reader = csv.reader(f)
            data_list = list(reader)
    else:
        with open('logs/rec_logs_groupe.csv') as f:
            reader = csv.reader(f)
            data_list = list(reader)
    
    now = datetime.now()
    m=[str(now), cur, chat_type]
    data_list.append(m)
    with open('logs/rec_logs.csv', 'w') as f:
        writer = csv.writer(f)
        for row in data_list:
            writer.writerow(row)
    
    if chat_type == "private":
        with open('logs/rec_logs_private.csv', 'w') as f:
            writer = csv.writer(f)
            for row in data_list:
                writer.writerow(row)
    else:
        with open('logs/rec_logs_group.csv', 'w') as f:
            writer = csv.writer(f)
            for row in data_list:
                writer.writerow(row)