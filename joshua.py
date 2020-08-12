import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import numpy as np
import pickle
import subprocess
import os
from os import system, name
import sys
from time import sleep
import wikipedia as wk
import re, string, unicodedata
import pyttsx3
from keras.models import load_model
model = load_model('chatbot_model.h5')
import json
import random
import concurrent.futures
intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))
typing_delay = 0.01

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[21].id)
engine.setProperty('rate', 230)

def screen_clear():
   if name == 'nt':
      _ = system('cls')
   # for mac and linux(here, os.name is 'posix')
   else:
      _ = system('clear')

#wikipedia search
def wikipedia_data(input):
    
    reg_ex = re.search('tell me about (.*)', input)
    try:
        if reg_ex:
            topic = reg_ex.group(1)
            wiki = wk.summary(topic, sentences = 3)
            return wiki
    except Exception as e:
            return "\nNo matching entries found. I'm afraid I can't help you with that.\n"

def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result

def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res

def textToSpeech(text):
    try:
        engine.endLoop()
    except Exception as e:
        pass      
    engine.say(text)
    engine.runAndWait()


def typing(sentence):
    sentence = sentence.upper()
    for char in sentence:
        sleep(typing_delay)
        sys.stdout.write(char)
        sys.stdout.flush()

# def parallel(string):
#     tasks = [lambda: textToSpeech(string), lambda: typing("\n> "+string+"\n\n")]
#     with ThreadPoolExecutor(max_workers=2) as executor:
#         futures = [executor.submit(task) for task in tasks]      
#         for future in futures:
#             try:
#                 future.result()
#             except Exception as e:
#                 print(e)
        
def parallel(text):
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        future_tasks = {executor.submit(textToSpeech, text), executor.submit(typing, "\n"+text+"\n\n")}
        for future in concurrent.futures.as_completed(future_tasks):
            try:
                data = future.result()
            except Exception as e:
                print(e)
                #pass


    
#Pre-Loop
screen_clear()
typing("                                                                        \n                                          \n                                              \n                                                             \n")
#Logon Loop
typing_delay=0.03
while True:
    try:
        logon_input = input("LOGON: ")
        logon_input = logon_input.lower()
        if(logon_input == "joshua"):
            break
        elif(logon_input == "help games"):
            typing("\n'Games' refers to models, simulations and games which have tactical and strategic applications.\n\n")
        elif(logon_input == "list games"):
            typing("\nFalken's Maze\nBlack Jack\nGin Rummy\nHearts\nBridge\nCheckers\nChess\nPoker\nFighter Combat\nGuerilla Engagement\nDesert Warfare\nAir-To-Ground Actions\nTheaterwide Tactical Warfare\nTheatrewide Biotoxic and Chemical Warfare\n\nGlobal Thermonuclear War.\n\n")        
        elif("help" in logon_input):
            typing("\nHELP NOT AVAILABLE\n\n")
        else:
            typing("\nIDENTIFICATION NOT RECOGNIZED BY SYSTEM\n--CONNECTION TERMINATED--\n\n\n\n")
            sys.exit(0)

        # Press ctrl-c or ctrl-d on the keyboard to exit
    except (KeyboardInterrupt, EOFError, SystemExit):
        sys.exit(0)
            
screen_clear()
typing_delay=0.0005

with open('data.txt', 'r') as file:
    data = file.read()
    typing(data)
    sleep(1.6) 
    screen_clear()
with open('dump.txt', 'r') as file:
    data = file.read()
    typing(data)
    sleep(0.5)    
    screen_clear()
with open('data2.txt', 'r') as file:
    data = file.read()
    typing(data)
    sleep(0.8) 
with open('dump2.txt', 'r') as file:
    data = file.read()
    typing(data)
    sleep(0.6)
    screen_clear()
with open('data3.txt', 'r') as file:
    data = file.read()
    typing(data)
    sleep(0.8)

screen_clear()
typing_delay=0.05
sleep(2.5)
parallel('Greetings Professor Falken')


# The following loop will execute each time the user enters input
while True:
    try:
        user_input = input()
        user_input = user_input.lower()

        if "tell me about" in user_input:
                parallel("Checking Database...")
                if user_input:
                    robo_response = wikipedia_data(user_input)              
                    parallel(robo_response)
        else:
            bot_response = chatbot_response(user_input)
            if(bot_response == "Falken's Maze\nBlack Jack\nGin Rummy\nHearts\nBridge\nCheckers\nChess\nPoker\nFighter Combat\nGuerilla Engagement\nDesert Warfare\nAir-To-Ground Actions\nTheaterwide Tactical Warfare\nTheatrewide Biotoxic and Chemical Warfare\n\nGlobal Thermonuclear War."):
                typing("\n"+bot_response+"\n\n")
            elif(bot_response == "** Identification not recognized **\n―――――――――――――――――――――――――――――――――――\n\n        ** Access Denied **"):
                print("\n"+bot_response+"\n\n")
            elif(bot_response == "Good, let's play Tic Tac Toe."): 
                process = subprocess.Popen(os.getcwd()+'/ttt.sh')
                process.wait()
                screen_clear()
                parallel("That was fun, I hope we can repeat this soon.")     
            elif(bot_response=="Great, let's play chess then."): 
                process = subprocess.Popen(os.getcwd()+'/chess.sh')
                process.wait()
                screen_clear()
                parallel("That was fun, I hope we can repeat this soon.")                                
            else:
                parallel(bot_response)

            if(bot_response=="Good bye, Professor Falken."):
                break


    # Press ctrl-c or ctrl-d on the keyboard to exit
    except (KeyboardInterrupt, EOFError, SystemExit):
        break

