

# CODE STARTS HERE


# In[1]:

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.conversation import Statement
import logging
import sys
from telepot.loop import MessageLoop

# Uncomment the following lines to enable verbose logging
# import logging
# logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.INFO)

# Create a new ChatBot instance
bot_ = ChatBot(
    'Anokha',
    storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
    logic_adapters=[
        "chatterbot.logic.BestMatch",
        "chatterbot.logic.MathematicalEvaluation",
    ],
    filters=[
        # 'chatterbot.filters.RepetitiveResponseFilter'
    ],
    database_uri='mongodb://mongo:27017/chatterbot-database'
)

# bot_.set_trainer(ChatterBotCorpusTrainer)
# bot_.train("chatterbot.corpus.english")

trainer = ChatterBotCorpusTrainer(bot_)

trainer.train(
    'chatterbot.corpus.english'
)

# 'chatterbot.corpus.english'


# In[2]:


import telepot
import time


# In[3]:


bot = telepot.Bot('258599010:AAEi9pqVhiP3h-wVw1tzCiq_elG5RuBefVc')
prevText = {}
prevReply = {}
permAdmin = [393347098]
people = [393347098]
admin = [393347098]
params = {
    'train_': False,
    'in_': None,
    'res_': None
}


bot.sendMessage(393347098, "Bot Restatred")


# In[ ]:


def get_feedback(msg):
    if 'yes' in msg.lower():
        return 1
    elif 'no' in msg.lower():
        return 0
    else:
        return -1


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)
    print(params['train_'])

    if content_type == 'text':
        if chat_id not in people:
            bot.sendMessage(chat_id, "Hello!  You seem to be a new face, allow me to introduce myself. I am anokhaBot I'm an                                       artificial agent that can tell you anything about Anokha. I'm still learning a lot about                                       anokha so it would be very helpful if you type /wrong whenever I go wrong somewhere and I promise to get better next time.")
            if chat_id in admin:
                bot.sendMessage(chat_id, "Greetings admin. What do you wanna do?\ninsertNewContext(inc-contextname)\n/train\naddPattern(ap-contextname-question)\n/errortxt\naddResponse(ar-contextname-response)\naddAdmin(adm-chatid)\nremoveAdmin(rmadm)")

            people.append(chat_id)

        if chat_id in admin:
            if msg['text'] == '/help':
                bot.sendMessage(chat_id, "Greetings admin. What do you wanna do?\ninsertNewContext(inc-contextname)\n/train\naddPattern(ap-contextname-question)\n/errortxt\naddResponse(ar-contextname-response)\naddAdmin(adm-chatid)\nremoveAdmin(rmadm)")
                return

            if msg['text'] == '/stop':
                bot.sendMessage(chat_id, "Stopping Bot")
                sys.exit(0)
                return

            if msg['text'] == '/train':
                if params['train_'] == False:
                    params['train_'] = True
                    bot.sendMessage(chat_id, "Now you can Train")
                    return
                if params['train_'] == True:
                    params['train_'] = False
                    params['in_'] = None
                    params['res_'] = None
                    bot.sendMessage(chat_id, "Trainning has been disabled")
                    return

            if msg['text'] == '/errortxt':
                with open('errors.txt') as s:
                    for line in s:
                        bot.sendMessage(chat_id, line)
                return

            if params['train_']:
                if params['in_'] == None and params['res_'] == None:
                    params['in_'] = Statement(str(msg["text"]))
                    reply = bot_.get_response(str(msg["text"])).text
                    bot.sendMessage(chat_id, reply)
                    bot.sendMessage(chat_id, "Is this a coherent response to " +
                                    str(params['in_']) + " \n Please type either 'Yes' or 'No'")
                    return

                if params['in_'] != None and params['res_'] == None:
                    in__ = str(msg["text"])
                    feed = get_feedback(in__)
                    if feed == 1:
                        params['in_'] = None
                    elif feed == 0:
                        params['res_'] = '10101*@#^'
                        bot.sendMessage(
                            chat_id, "Please enter correct response")
                    else:
                        bot.sendMessage(
                            chat_id, "Please type either 'Yes' or 'No'")
                    return

                if params['res_'] == '10101*@#^':
                    params['res_'] = Statement(str(msg["text"]))
                    bot_.learn_response(params['res_'], params['in_'])
                    params['in_'] = None
                    params['res_'] = None
                    bot.sendMessage(chat_id, "Responses added to bot!")
                    return

                return

            if not params['train_']:
                try:
                    reply = bot_.get_response(str(msg["text"])).text
                    prevText[chat_id] = msg["text"]
                    prevReply[chat_id] = reply
                    if not reply == None:
                        bot.sendMessage(chat_id, reply)
                    else:
                        bot.sendMessage(
                            chat_id, "I'm sorry, I didn't understand you. Could you rephrase it please?")
                except Exception as e:
                    print(e)
                    bot.sendMessage(
                        chat_id, "I'm sorry, I didn't understand you. Could you rephrase it please?")

                print(prevReply, prevText)
                return

            if 'adm' in msg['text'][:4].lower():
                chatID = int(msg['text'][4:])
                if chatID not in permAdmin:
                    permAdmin.append(chatID)
                if chatID not in admin:
                    admin.append(chatID)
                bot.sendMessage(chat_id, "Chat ID " +
                                str(chatID) + " is now an admin")
                bot.sendMessage(chatID, "You have been made an admin")
                return

            if 'rmadm' in msg['text'][:6].lower():
                admin.remove(chat_id)
                people.remove(chat_id)
                bot.sendMessage(
                    chat_id, "You are not an admin anymore. You can become an admin once again by typing /makemeadmin")
                return

        if msg["text"] == "/wrong" or msg['text'] == '\wrong':
            with open("errors.txt", "a") as file:
                writeData = "cid-" + str(chat_id) + "-txt-" + str(
                    prevText[chat_id]) + "-rep-" + str(prevReply[chat_id]) + "\n"
                file.write(writeData)
                return

        if chat_id not in admin:
            if msg['text'] == '/makemeadmin' and chat_id in permAdmin:
                admin.append(chat_id)
                bot.sendMessage(chat_id, "You are now an admin")
                return

            if msg['text'] == '/start':
                return

            print(msg['text'])

            try:
                reply = bot_.get_response(str(msg["text"])).text
                prevText[chat_id] = msg["text"]
                prevReply[chat_id] = reply
                if not reply == None:
                    bot.sendMessage(chat_id, reply)
                else:
                    bot.sendMessage(
                        chat_id, "I'm sorry, I didn't understand you. Could you rephrase it please?")
            except Exception as e:
                print(e)
                bot.sendMessage(
                    chat_id, "I'm sorry, I didn't understand you. Could you rephrase it please?")

            print(prevReply, prevText)


MessageLoop(bot, handle).run_as_thread()


print('Listening ...')


while 1:
    time.sleep(1)


# In[ ]:


# In[ ]:


# In[ ]:
