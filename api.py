# Filename - server.py

# Import flask and datetime module for showing date and time
from flask import *
from main1 import openairun
import datetime
import json
from py1337x import py1337x
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
bot = telebot.TeleBot('6549292499:AAGmD7uf5R1wgYYgJP8E5yx0okQb7egfQsI', threaded=False)
torrents = py1337x(proxy='1377x.to', cacheTime=0)
x = datetime.datetime.now()

# Initializing flask app
app = Flask(__name__)

# Route for seeing a data
@app.route('/')
def start():
    return "hello"

@app.route('/data/')
def getopenai():
    user_query = str(request.args.get('query'))  # /data/?query=USER SENTENCE
    openaires = openairun(user_query)
    openairesponse = {"User Query ": user_query, "Response": openaires}
    json_response = json.dumps(openairesponse)

    return json_response
@app.route('/', methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    bot.process_new_updates([update])
    return 'ok', 200

@bot.message_handler(commands=['start'])
def start(message):
  user_name = message.from_user.first_name
  print("start "+user_name)
  bot.reply_to(message, "Hey "+user_name +"")
    
# Running app
if __name__ == '__main__':
    app.run(debug=True)
