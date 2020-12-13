# exchange-rates-tg-bot
<b>Requirements:</b>
<ul>
  <li>Python 3.7+</li>
  <li>Aiogram (2.11+), uvloop, ujson, cchardet, aiodns, aiohttp[speedups]</li>
  <li>urllib3</li>
  <li>xmltodict</li>
</ul>
<b>ENGLISH VERSION:</b><br>
ERTB – exchange rates telegram bot.<br>
The bot recognizes currencies and amounts in the text, and then sends a message with other currencies. An example of a working bot: <a href="https://t.me/exchange_rates_vsk_bot">ERTB</a><br><br>
<b>An example of how the bot works:</b><br>
Your message:<br>
<pre>5 euro</pre>
Bot's answer:
<pre>🇪🇺5.0 EUR

🇨🇭5.39 CHF
🇮🇱19.73 ILS
🇺🇸6.06 USD</pre><br>
<b>Bot run</b><br>
You can run the bot like this: <pre>python3 bot.py</pre> By default, you will not see any output other than errors. To see the full output, run the bot like this: <pre>python3 bot.py -l on</pre> or <pre>python3 bot.py --logs on</pre><br>
<b>List of commands for users:</b><br>
<dl>
  <dt>about</dt>
    <dd>Short information about bot and creators.</dd>
  <dt>help</dt>
    <dd>Help on using and configuring the bot.</dd>
  <dt>settings</dt>
    <dd>Here you can configure some parameters for your chat.</dd>
  <dt>donate</dt>
    <dd>You can support the development of the bot.</dd>
  <dt>wrong</dt>
    <dd>Reply the message is incorrectly recognized.</dd>
  <dt>source</dt>
    <dd>A little about the source code.</dd>
</dl><br>
<b>List of commands for developers / administrators:</b><br>
<dl>
  <dt>count</dt>
    <dd>Getting information about the number of bot users.</dd>
  <dt>echo</dt>
    <dd>Sending messages to all chats. After the command, you need to write the text that you want to send.</dd>
  <dt>unban</dt>
    <dd>Unban user by ID.</dd>
  <dt>stats</dt>
    <dd>Getting information on the number of group and personal chats, on the number of enabled currencies in the settings.</dd>
  <dt>logs</dt>
    <dd>Getting all files from the "logs" folder.</dd>
  <dt>backup</dt>
    <dd>Archive with all settings and logs.</dd>
  <dt>reports</dt>
    <dd>Getting all reports on misrecognition.</dd>
  <dt>delete_reports</dt>
    <dd>Removing all reports from the folder.</dd>
</dl><br>
<b>RUSSIAN VERSION:</b><br>
ERTB – exchange rates telegram bot.<br>
Бот распознает в тексте валюты и суммы, а затем присылает сообщение уже с другими валютами. Пример работающего бота: <a href="https://t.me/exchange_rates_vsk_bot">ERTB</a><br><br>
<b>Пример работы бота:</b><br>
Ваше сообщение:<br>
<pre>5 баксов</pre>
Ответ бота:
<pre>🇺🇸5.0 USD

🇪🇺4.13 EUR
🇷🇺365.98 RUB
🇺🇦139.83 UAH</pre><br>
<b>Запуск бота</b><br>
Запустить бота можно так: <pre>python3 bot.py</pre> По умолчанию вы не увидите никакого вывода, кроме ошибок. Чтобы видеть полный вывод запустите бота так: <pre>python3 bot.py -l on</pre> или <pre>python3 bot.py --logs on</pre><br>
<b>Список команд для пользователей:</b><br>
<dl>
  <dt>about</dt>
    <dd>Краткая информация про бота и создателей.</dd>
  <dt>help</dt>
    <dd>Помощь в использовании и настройки бота.</dd>
  <dt>settings</dt>
    <dd>Тут можно настроить бота для вашего чата.</dd>
  <dt>donate</dt>
    <dd>Вы можете поддержать разработку бота чеканной монетой.</dd>
  <dt>wrong</dt>
    <dd>Ответьте на сообщение, которое бот неправильно распознал данной командой.</dd>
  <dt>source</dt>
    <dd>Немного про исходный код бота.</dd>
</dl><br>
<b>Список команд для разработчиков/администраторов:</b><br>
<dl>
  <dt>count</dt>
    <dd>Получение информации про количество пользователей бота.</dd>
  <dt>echo</dt>
    <dd>Рассылка сообщения по всем чатам. После команды нужно написать текст, который желаете разослать.</dd>
  <dt>unban</dt>
    <dd>Разбанить пользователя по ID.</dd>
  <dt>stats</dt>
    <dd>Получение информации по количеству чатов групповых и личных, по количеству включенных валют в настройках.</dd>
  <dt>logs</dt>
    <dd>Получение всех файлов из папки logs.</dd>
  <dt>backup</dt>
    <dd>Архив со всеми настройками и логами.</dd>
  <dt>reports</dt>
    <dd>Получение всех репортов по неправильному распознаванию.</dd>
  <dt>delete_reports</dt>
    <dd>Удаление всех репортов из папки.</dd>
</dl>
