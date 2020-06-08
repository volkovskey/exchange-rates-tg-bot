#!/usr/bin/env python
# -*- coding: utf-8 -*-
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import config
import check_and_search
import telebot
import json

bot = telebot.TeleBot(config.token, threaded = False)

@bot.message_handler(content_types=["text"])
def main_void(message):
    #bot.send_message(message.chat.id, "Запуск основного метода")
    s = check_and_search.delete_space(message)
    print(s)
    if check_and_search.check_for_numbers(s):
        h = check_and_search.check_vault(s)
        #print(h)
        if h != -1:
            sum = check_and_search.search(s, h)
            #print (sum)
            check_and_search.change_vaults(sum, h, message, bot)
        else:
            print("no vaults")
    else:
        print("no numbers")

if __name__ == '__main__':
    bot.infinity_polling()