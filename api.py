import telebot
import requests
import flask
import json
import time
from py1337x import py1337x
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from googletrans import Translator
translator = Translator()
bot = telebot.TeleBot('6549292499:AAGmD7uf5R1wgYYgJP8E5yx0okQb7egfQsI', threaded=False)
torrents = py1337x(proxy='1337x.to', cacheTime=0)
bot.remove_webhook()
bot.set_webhook('https://testrender-o7s9.onrender.com/')

LANGUAGES = { 'af': 'afrikaans', 'sq': 'albanian', 'am': 'amharic', 'ar': 'arabic', 'hy': 'armenian', 'az': 'azerbaijani', 'eu': 'basque', 'be': 'belarusian', 'bn': 'bengali', 'bs': 'bosnian', 'bg': 'bulgarian', 'ca': 'catalan', 'ceb': 'cebuano', 'ny': 'chichewa', 'zh-cn': 'chinese (simplified)', 'zh-tw': 'chinese (traditional)', 'co': 'corsican', 'hr': 'croatian', 'cs': 'czech', 'da': 'danish', 'nl': 'dutch', 'en': 'english', 'eo': 'esperanto', 'et': 'estonian', 'tl': 'filipino', 'fi': 'finnish', 'fr': 'french', 'fy': 'frisian', 'gl': 'galician', 'ka': 'georgian', 'de': 'german', 'el': 'greek', 'gu': 'gujarati', 'ht': 'haitian creole', 'ha': 'hausa', 'haw': 'hawaiian', 'iw': 'hebrew', 'he': 'hebrew', 'hi': 'hindi', 'hmn': 'hmong', 'hu': 'hungarian', 'is': 'icelandic', 'ig': 'igbo', 'id': 'indonesian', 'ga': 'irish', 'it': 'italian', 'ja': 'japanese', 'jw': 'javanese', 'kn': 'kannada', 'kk': 'kazakh', 'km': 'khmer', 'ko': 'korean', 'ku': 'kurdish (kurmanji)', 'ky': 'kyrgyz', 'lo': 'lao', 'la': 'latin', 'lv': 'latvian', 'lt': 'lithuanian', 'lb': 'luxembourgish', 'mk': 'macedonian', 'mg': 'malagasy', 'ms': 'malay', 'ml': 'malayalam', 'mt': 'maltese', 'mi': 'maori', 'mr': 'marathi', 'mn': 'mongolian', 'my': 'myanmar (burmese)', 'ne': 'nepali', 'no': 'norwegian', 'or': 'odia', 'ps': 'pashto', 'fa': 'persian', 'pl': 'polish', 'pt': 'portuguese', 'pa': 'punjabi', 'ro': 'romanian', 'ru': 'russian', 'sm': 'samoan', 'gd': 'scots gaelic', 'sr': 'serbian', 'st': 'sesotho', 'sn': 'shona', 'sd': 'sindhi', 'si': 'sinhala', 'sk': 'slovak', 'sl': 'slovenian', 'so': 'somali', 'es': 'spanish', 'su': 'sundanese', 'sw': 'swahili', 'sv': 'swedish', 'tg': 'tajik', 'ta': 'tamil', 'te': 'telugu', 'th': 'thai', 'tr': 'turkish', 'uk': 'ukrainian', 'ur': 'urdu', 'ug': 'uyghur', 'uz': 'uzbek', 'vi': 'vietnamese', 'cy': 'welsh', 'xh': 'xhosa', 'yi': 'yiddish', 'yo': 'yoruba', 'zu': 'zulu', }


app = flask.Flask(__name__)
@app.route('/translate', methods=['GET', 'POST'])
def translate():
    query = flask.request.args.get('query', '')  # /
    if translator.detect(query).lang != 'en':
        detected_lang_name = LANGUAGES.get(translator.detect(query).lang, 'Unknown')
        return {"User Query ": query, "Response": translator.translate(query).text,"Lang" : detected_lang_name, "status": 1}
    else:
        return {"User Query ": query, "Response": "Already in English","Lang" : "english", "status": 2}

@app.route('/', methods=['GET', 'POST'])
def webhook():
    if flask.request.method == 'POST':
        update = telebot.types.Update.de_json(flask.request.stream.read().decode('utf-8'))
        bot.process_new_updates([update])
        return 'ok', 200
    else:
        return 'Hello', 200
@app.route('/test', methods=['POST'])
def test_webhook():
    return 'Working', 200

@bot.message_handler(commands=['start'])
def start(message):
  user_name = message.from_user.first_name
  print("start "+user_name)
  bot.reply_to(message, "Hey "+user_name +"")

@bot.message_handler(commands=['s'])
def start(message):
  user_name = message.from_user.first_name
  search = message.text.split(' ', 1)[1]
  # bot.reply_to(message, "Searching for "+search)
  search_result = torrents.search(search, sortBy='time', order='desc')
  search_result = json.dumps(search_result)
  # print(search_result)
  # Assuming search_result is a JSON string
  search_result_dict = json.loads(search_result)
  keyboard = InlineKeyboardMarkup(row_width=1)
  # Now you can iterate over the items and print only the 'name'
  name = []
  for item in search_result_dict['items']:
    i = 0
    button_name = "button" + str(i + 1)
    button_name = InlineKeyboardButton(item['name'], callback_data=item['torrentId'])
    name.append(item['name'])
    keyboard.add(button_name)
    i=+1
  # Create a single string with each name on a new line
  names_message = '\n'.join(name)
  bot.send_message(message.chat.id, 'Please choose:', reply_markup=keyboard)
  # bot.reply_to(message, names_message)

# Define the button click handler
@bot.callback_query_handler(func=lambda call: True)
def button_click(call):
    # Send different responses based on the button clicked
    magnet_info = torrents.info(torrentId=call.data)
    # Preparing message to send
    send_info = "Name : " + magnet_info['name'] + "\nSize : " + magnet_info['size'] + "\n\nMagnet Link : \n"
    magnetl = "`" + magnet_info['magnetLink'] + "`" 
    send_info = send_info + magnetl
    message = f"<b>Name:</b> {magnet_info['name']}<br/><b>Size:</b> {magnet_info['size']}<br/><br/><b>Magnet Link:</b><br/><a href='{magnet_info['magnetLink']}'>Click Here</a>"
    # bot.send_message(call.message.chat.id, message, parse_mode='ParseMode.HTML')
    bot.send_message(call.message.chat.id, send_info, parse_mode='Markdown')
    # bot.send_message(call.message.chat.id, send_info, parse_mode='MarkdownV2')
    # bot.send_message(call.message.chat.id, magnetl, parse_mode='MarkdownV2') #chat_id is another unique identifier
    bot.answer_callback_query(call.id, call.data)

    if call.data == 'button1':
        bot.answer_callback_query(call.id, 'You clicked Button 1')
    elif call.data == 'button2':
        bot.answer_callback_query(call.id, 'You clicked Button 2')

# bot.polling(non_stop=1)
        # Running app
if __name__ == '__main__':
    app.run(debug=True)
