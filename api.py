# Filename - server.py

# Import flask and datetime module for showing date and time
from flask import *
from main1 import openairun
import datetime
import json

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

# Running app
if __name__ == '__main__':
    app.run(debug=True)
