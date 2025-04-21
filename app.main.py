# -*- coding: utf-8 -*-
import json
try:
	# Opening JSON file
    with open('settings.json', 'r') as openfile:
        settings = json.load(openfile)
except:
	print("settings file not found")
	settings ={
    "mute" : False,
    "FirstTime" : True,
    "Language" : "en"
}
	with open("settings.json", "w") as outfile:
		json.dump(settings, outfile)

if settings["FirstTime"]== True:
    import sys, os
    print("This may take a while since it is the first time running the program")
    path= sys.path[0][:-7]
    os.system(f'"{path}python\\python.exe" -m pip install gtts')
    os.system(f'"{path}python\\python.exe" -m pip install nltk')
    os.system(f'"{path}python\\python.exe" -m pip install pickle')
    os.system(f'"{path}python\\python.exe" -m pip install keras')
    os.system(f'"{path}python\\python.exe" -m pip install tensorflow')
    os.system(f'"{path}python\\python.exe" -m pip install playsound==1.2.2')
    import nltk
    print("This may take a while")
    nltk.download("punkt")
    nltk.download("wordnet")
    nltk.download("stopwords")
    settings["FirstTime"]= False
    with open("settings.json", "w") as outfile:
        json.dump(settings, outfile)

import random
import os
from gtts import gTTS
import eel
from playsound import playsound
import json
from keras.models import load_model
import numpy as np
import pickle
import nltk
from nltk.stem import WordNetLemmatizer


lemmatizer = WordNetLemmatizer()
""""""
#MAIN THINKING
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(
        word.lower()) for word in sentence_words]
    return sentence_words
# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print("found in bag: %s" % w)
    return(np.array(bag))
def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list
#PREDICTION END

"""

from chatbot import *"""

if settings["Language"] == "ar":
    model = load_model('model\\chatbot_model.ar.h5')
    intents = json.loads(open('model\\intents.main.ar.json', encoding='utf8').read())
    words = pickle.load(open('model\\words.ar.pkl', 'rb'))
    classes = pickle.load(open('model\\classes.ar.pkl', 'rb'))
else:
    model = load_model('model\\chatbot_model.en.h5')
    intents = json.loads(open('model\\intents.main.en.json', encoding='utf8').read())
    words = pickle.load(open('model\\words.en.pkl', 'rb'))
    classes = pickle.load(open('model\\classes.en.pkl', 'rb'))

context = "Beg"
"""
beg = False"""
mute = settings["mute"]

def Text_to_speech(Message):
    global mute, settings
    if not mute:
        if os.path.exists("DataFlair.mp3"):
            os.remove("DataFlair.mp3")
        if settings["Language"] == "ar":
            speech = gTTS(text = str(Message).replace("<br>"," "), lang="ar")
        else:
            speech = gTTS(text = str(Message).replace("<br>"," "))
        speech.save('DataFlair.mp3')
        playsound('DataFlair.mp3', block=False)

def getResponse(ints, intents_json,contextToUse):
    try:
        tag = ints[0]['intent']
        print(tag)
        print(contextToUse)
    except:
        return ("Sorry can I cannot understand.",0)
    
    list_of_intents = intents_json['intents']
    if tag == "elaborate":
        for i in list_of_intents:
            print(i["tag"])
            if contextToUse == i["tag"]:
                result = (random.choice(
                    ["Sure! Let me provide more information: ",
                "Certainly! Here's some additional information: ",
                "I'd be happy to elaborate. Here you go: "]
                ) + random.choice(i['responses']), i["context"][0])
                break
        else:
            result = ("I'm not sure how to elaborate on that topic. Please specify a valid topic.",None)
    else:
        for i in list_of_intents:
            """for index in contextToUse:
                if index == tag:
                    result = (random.choice(i['responses']), i["context"][0])
                    break"""
            if(i['tag'] == tag):
                try:
                    result = (random.choice(i['responses']), i["context"], tag)
                except:
                    result = (random.choice(i['responses']),None, None)
                break
    return result


def chatbot_response(msg,context):
    global intents
    try:
        
        ints = predict_class(msg, model)
        # If no intent is recognized, inform the user
        

        res = getResponse(ints, intents,context)
        return res
    except ValueError:
        if settings["Language"] == "en":
            return "Sorry, I can't understand. Please provide more information or try a different question.", None, None
        else:
            return "آسف، لا أستطيع أن أفهم. يرجى تقديم المزيد من المعلومات أو تجربة سؤال آخر.", None, None


# Creating GUI with eel

eel.init('assets')



option = {
    'mode': 'custom',
    'args': ['node_modules/electron/dist/electron.exe', '.']
}
output = ""
f= open('./assets/log.html', 'w', encoding="utf8")
if settings["Language"] == "en":
    f.write("""<link type="text/css" rel="stylesheet" href="./styleHealth.css">
<div class='msgln' ><b class='bot' >SAiS </b>Hi, I am QACA Chatbot your virtual healthcare guide who will help you give information regarding cancer.<br>
Here are some sample questions you can try<br>
1.What is breast cancer <br>
2.What is colorectal cancer <br>
3.Methods to identify cancer in asymptomatic people<br>
4.treatment methods for breast cancer <br>
5.treatments methods for colorectal cancer<br>""")
    Text_to_speech("""Hi, I am QACA Chatbot your virtual healthcare guide who will help you give information regarding cancer.
Here are some sample questions you can try
1.What is breast cancer.
2.What is colorectal cancer.
3.Methods to identify cancer in asymptomatic people.
4.treatment methods for breast cancer.
5.treatments methods for colorectal cancer.""")
    

else:
    f.write("""<link type="text/css" rel="stylesheet" href="./styleHealth.css">
<div class='msgln' ><b class='bot' >SAiS </b>مرحباً، أنا QACA Chatbot مرشدك الافتراضي للرعاية الصحية الذي سيساعدك في تقديم المعلومات المتعلقة بالسرطان.
إليك بعض نماذج الأسئلة التي يمكنك تجربتها<br>
ما هو سرطان الثدي.1<br>
ما هو سرطان القولون والمستقيم.2<br>
طرق التعرف على السرطان لدى الأشخاص الذين لا تظهر عليهم أعراضه.3<br>
طرق علاج سرطان الثدي.4<br>
طرق علاج سرطان القولون والمستقيم.5</div>""")
    Text_to_speech("""مرحباً، أنا QACA Chatbot مرشدك الافتراضي للرعاية الصحية الذي سيساعدك في تقديم المعلومات المتعلقة بالسرطان.
إليك بعض نماذج الأسئلة التي يمكنك تجربتها
ما هو سرطان الثدي.1
ما هو سرطان القولون والمستقيم.2
طرق التعرف على السرطان لدى الأشخاص الذين لا تظهر عليهم أعراضه.3
طرق علاج سرطان الثدي.4
طرق علاج سرطان القولون والمستقيم.5""")
    pass
f.close()
eel.SwitchJS(settings["Language"],True)

@eel.expose
def convert(msg):
    global intents, mute, context, settings, classes, words, model
    if not msg.isalpha:
        msg = msg[::-1]
    print(msg)
    #print(intents)
    with open("./assets/log.html", "a", encoding="utf8") as message:
        message.write("\n")
        message.write(f"<div class='msglnuser' >%s<b class='user' > You</b><br> </div >" % (msg))
    global output
    ##Beginning Only
    """if beg==True:
        if msg=='1':
            ans="Breast cancer is a type of cancer that forms in the cells of the breast. It primarily affects breast tissue and can develop in different parts of the breast, most commonly in the ducts that carry milk to the nipple (ductal carcinoma) or the glands that produce milk (lobular carcinoma).<br>"
            Text_to_speech(ans)
            with open("./assets/log.html", "a") as bot:
                bot.write("\n")
                bot.write(f"<div class='msgln' ><b class='bot' >SAiS </b>%s<br> </div >" % (ans))
                beg=False
            return ans
        elif msg=='2':
            ans="Colorectal cancer, also known as bowel cancer or colon cancer, refers to cancer that develops in the colon or rectum. The colon is the large intestine, while the rectum is the final part of the large intestine before the anus. Colorectal cancer typically starts as small, benign growths called polyps, which can gradually develop into cancer over time."
            Text_to_speech(ans)
            with open("./assets/log.html", "a") as bot:
                bot.write("\n")
                bot.write(f"<div class='msgln' ><b class='bot' >SAiS </b>%s<br> </div >" % (ans))
                beg=False
            return ans
        elif msg == '3':
            ans = "Image Recognition:  Image recognition is a field of artificial intelligence where computers are trained to interpret and understand visual information, such as images or videos.  In cancer diagnosis, image recognition techniques are used to analyze medical images like X-rays, CT scans, and MRIs. Convolutional Neural Networks (CNNs) are a popular type of AI model for image recognition in cancer detection. <br> Genomic Analysis: Genomic analysis involves studying an individual's genetic material (genome) to identify genetic variations and mutations. Genomic analysis can be used to find specific genetic mutations associated with cancer. It's essential for understanding the genetic basis of cancer and can inform personalized treatment strategies. Identifying specific mutations in the BRCA1 and BRCA2 genes, which are linked to an increased risk of breast and ovarian cancer. <br> Screening Tests:<br> Perform specific screening tests that are appropriate for the type of cancer being considered. These tests may include: <br> Mammography for breast cancer <br> Colonoscopy for colorectal cancer"
            Text_to_speech(ans)
            with open("./assets/log.html", "a") as bot:
                bot.write("\n")
                bot.write(f"<div class='msgln' ><b class='bot' >SAiS </b>%s<br> </div >" % (ans))
                beg=False
            return ans
        elif msg=='4':
            ans="Treatment for breast cancer depends on various factors like the cancer's stage, type, whether it's hormone-sensitive, and an individual's overall health. Here are the primary treatment methods commonly used: Surgery, Radiation Therapy, Chemotherapy, Hormone Therapy, Targeted Therapy, Immunotherapy, Reconstructive Surgery"
            Text_to_speech(ans)
            with open("./assets/log.html", "a") as bot:
                bot.write("\n")
                bot.write(f"<div class='msgln' ><b class='bot' >SAiS </b>%s<br> </div >" % (ans))
                beg=False
            return ans
        elif msg=='5':
            ans="Treatment for colorectal cancer depends on the stage, location, and individual factors. Here are the primary treatment methods commonly used: Surgery, Radiation Therapy, Chemotherapy, Hormone Therapy, Immunotherapy, Stoma Surgery, Clinical Trials"
            Text_to_speech(ans)
            with open("./assets/log.html", "a") as bot:
                bot.write("\n")
                bot.write(f"<div class='msgln' ><b class='bot' >SAiS </b>%s<br> </div >" % (ans))
                beg=False
            return ans
        else:
            Text_to_speech("sorry can you choose from 1 to 5 only for now?")
            with open("./assets/log.html", "a") as bot:
                bot.write("\n")
                bot.write(f"<div class='msgln' ><b class='bot' >SAiS </b>sorry can you choose from 1 to 5 only for now?<br> </div >")
            return 0
    #Beginning End"""
    

    output = chatbot_response(str(msg), context)
    try:
        context = output[1][0]
    except:
        context = ""
    try:
        if context=="Mute":
            mute = True
        elif context=="Talk":
            mute = False
        elif context=="Switch":
            if settings["Language"] == "ar":
                eel.SwitchJS("en", False)

            else:
                eel.SwitchJS("ar", False)

    except:
        pass
    
    with open("./assets/log.html", "a" , encoding="utf8") as bot:
        bot.write("\n")
        bot.write(f"<div class='msgln' ><b class='bot' >SAiS </b>%s<br> </div >" % (str(output[0])))
    Text_to_speech(str(output[0]))
    print(output[0])
    try:
        if "picAvail" in output[1][1]:
            with open("./assets/log.html", "a") as bot:
                bot.write("\n")
                bot.write(f"<div class='msgln' ><b class='bot' >SAiS </b><img src='./Images/%s.png'> <br></div >" % (str(output[2])))
    except:
        pass
    print("Context:",output[1])
    # if str(output) in ["bye!","good bye","buh bye","bye bye","good night"]:
    #    eel.sleep(10)
    return str(output[0])



def switch(a):
    global classes, model, words, intents, settings
    settings["Language"] = a
    with open("settings.json", "w") as outfile:
        json.dump(settings, outfile)
    del model
    del intents
    del words
    del classes
    model = load_model(f'model\\chatbot_model.{a}.h5')
    intents = json.loads(open(f'model\\intents.main.{a}.json', encoding='utf8').read())
    words = pickle.load(open(f'model\\words.{a}.pkl', 'rb'))
    classes = pickle.load(open(f'model\\classes.{a}.pkl', 'rb'))

eel.expose(switch)

def say(a):
    with open("./assets/log.html", "a", encoding="utf8") as bot:
        bot.write(f"<div class='msgln' ><b class='bot' >SAiS </b>{a}<br> </div >" )
    Text_to_speech(a)

eel.expose(say)

eel.start('index - Chat.html', size=(800, 600))
settings["mute"] = mute

with open("settings.json", "w") as outfile:
    json.dump(settings, outfile)