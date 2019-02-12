from bottle import route, run, request, response, Bottle
import random
import json
import datetime
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.conversation import Statement
import logging
import sys
from telepot.loop import MessageLoop
from bottle import static_file
import json
import re

logging.basicConfig(level=logging.INFO)
escape = ''.join([chr(char) for char in range(1, 32)])
bot_ = ChatBot(
    'Anokha',
    storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
    logic_adapters=[
        "chatterbot.logic.BestMatch",
        "chatterbot.logic.MathematicalEvaluation",
    ],
    filters=[
        #         'chatterbot.filters.RepetitiveResponseFilter'
    ],
    database_uri='mongodb://mongo:27017/chatterbot-database',
    read_only=True
)

# bot_.set_trainer(ChatterBotCorpusTrainer)
# bot_.train("chatterbot.corpus.english")

trainer = ChatterBotCorpusTrainer(bot_)

trainer.train(
    'chatterbot.corpus.english'
)

prevText = {}
prevReply = {}
permAdmin = ['393347098']
people = ['393347098']
admin = ['393347098']


app = Bottle()


@app.route('/', method='GET')
def home():
    return static_file('chatbotv2.html', root='./')


@app.route('/js/<filename:re:.*\.js>')
def js(filename):
    return static_file(filename, root='./static/js/')


@app.route('/css/:filename#.*#')
def css(filename):
    return static_file(filename, root='./static/css/')


@app.route('/assets/:filename#.*#')
def css(filename):
    return static_file(filename, root='./static/assets/')


@app.hook('after_request')
def enable_cors():
    """
    You need to add some headers to each request.
    Don't use the wildcard '*' for Access-Control-Allow-Origin in production.
    """
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'


@app.route('/api', method="POST")
@app.route('/bot/api', method="POST")
def api():
    if request.cookies.get('id') == None:
        nw = str(datetime.datetime.now())[-15:]
        chat_id = str(str(int(random.random()*1000000)) + nw)[:18]
        response.set_cookie("id", chat_id, path='/')
    else:
        chat_id = request.cookies.get('id')

    print(chat_id)
    msg = request.forms.get('data')

    if len(msg) == 0:
        reply = 'You can\'t send me an empty text'
        resp = {"reply": reply}
        return dict(data=resp)
        
    msg = msg.strip()
    msg = re.sub(r'[\\[a-z]*','', msg)
    msg=re.sub(r'\+',' + ',msg)    
    msg=re.sub(r'\*',' * ',msg) 
    msg=re.sub(r'\-',' - ',msg) 
    msg=re.sub(r'\\',' \ ',msg) 
    print(msg)
    if len(msg) == 0:
        reply = 'Am I a joke to you -_-'

    elif msg == '/error':
        with open("errors.txt", "a") as file:
            writeData = "cid-" + str(chat_id) + "-txt-" + str(
                prevText[chat_id]) + "-rep-" + str(prevReply[chat_id]) + "\n"
            file.write(writeData)
        reply = 'Your response has been recorded'

    elif msg == '/mkadmin.ak2K19':
        response.set_cookie("id", '393347098', path='/')
        reply = "You are admin for prevText type /prevText and prevReply type /prevReply and for errortxt type /errortxt"

    elif msg == '/errortxt' and chat_id in admin:
        with open("errors.txt", "r") as myfile:
            reply = myfile.readlines()

    elif msg == '/prevText' and chat_id in admin:
        reply = json.dumps(prevText)

    elif msg == '/prevReply' and chat_id in admin:
        reply = json.dumps(prevReply)

    elif msg == '/rmadmin' and chat_id in admin:
        nw = str(datetime.datetime.now())[-15:]
        chat_id = str(str(int(random.random()*1000000)) + nw)[:18]
        response.set_cookie("id", chat_id, path='/')
        reply = "You are no longer admin"

    elif msg[0] == '/':
        reply = "You are not allowed to perform admin operations"

    else:
        try:
            reply = str(bot_.get_response(msg))
        except Exception as e:
            print(e)
            reply = "I'm sorry, I didn't understand you. Could you rephrase it please?"

    prevText[chat_id] = msg
    prevReply[chat_id] = reply

    print(prevReply, prevText)

    resp = {"reply": reply}
    return dict(data=resp)


run(app, host='0.0.0.0', port=6789, reloader=True, debug=True)
