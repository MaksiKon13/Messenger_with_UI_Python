import time
from itertools import groupby

from flask import Flask, request, abort

app = Flask(__name__)

database = [
    {
        'name': 'Jack',
        'text': 'hi man',
        'time': 0.01
    },
    {
        'name': 'Mary',
        'text': 'yyyyyooo, Jack!',
        'time': 0.01
    },
]


@app.route("/")
def hello():
    return "Hello, Skillbox! <a href='/status'>Статус</a>"   #<a href='/messages'>Сообщения</a>

#@app.route("/messages")
#def messages():
 #   return {
  #      'status': True,
   #     'messages': database,
    #    'time': time.asctime(),
     #   'count_messages': i,
      #  'count_users': o
   # }


@app.route("/status")
def status():
    r = groupby(sorted(database, key=lambda x: x['text']), lambda x: x['text'])
    i = 0
    for k, g in r:
        i += 1
        print(k, len(list(g)))
    users = groupby(sorted(database, key=lambda x: x['name']), lambda x: x['name'])
    o = 0
    for userk, userg in users:
        o += 1
        print(userk, len(list(userg)))
    return {
        'status': True,
        'name': 'Messenger',
        'time': time.asctime(),
        'count_messages': i,
        'count_users': o
    }


@app.route("/send", methods=['POST'])
def send_message():
    data = request.json  # TODO validate

    if not isinstance(data, dict):
        return abort(400)
    if 'name' not in data or 'text' not in data:
        return abort(400)

    name = data['name']
    text = data['text']

    if not isinstance(name, str) or not isinstance(text, str):
        return abort(400)
    if not (0 < len(name) < 128):
        return abort(400)
    if not (0 < len(text) < 128):
        return abort(400)
    message = {
        'name': name,
        'text': text,
        'time': time.time()
    }
    database.append(message)
    print(database)  # TODO remove
    return {'ok': True}


@app.route("/messages")
def get_messages():
    try:
        after = float(request.args['after'])
    except:
        return abort(400)
    messages = []
    for message in database:
        if message['time'] > after:
            messages.append((message))
    return {'messages': messages[:50]}


app.run()
