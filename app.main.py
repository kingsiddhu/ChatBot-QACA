import random
import os
from gtts import gTTS
import eel
from playsound import playsound
from chatbot import *



try:
	# Opening JSON file
    with open('settings.json', 'r') as openfile:
        settings = json.load(openfile)
except:
	print("settings file not found")
	settings ={
    "mute" : False,
    "FirstTime" : True,
}
	with open("settings.json", "w") as outfile:
		json.dump(settings, outfile)

if settings["FirstTime"]== True:
    import nltk
    print("This may take a while")
    nltk.download("punkt")
    nltk.download("wordnet")
    nltk.download("stopwords")
    settings["FirstTime"]= False
    with open("settings.json", "w") as outfile:
        json.dump(settings, outfile)



context = "Beg"
beg = True
mute = settings["mute"]

def Text_to_speech(Message):
    global mute
    if not mute:
        if os.path.exists("DataFlair.mp3"):
            os.remove("DataFlair.mp3")
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
    ints = predict_class(msg, model)
    res = getResponse(ints, intents,context)
    return res


# Creating GUI with tkinter

eel.init('assets')
option = {
    'mode': 'custom',
    'args': ['node_modules/electron/dist/electron.exe', '.']
}
output = ""
f= open('./assets/log.html', 'w')
f.write("""<link type="text/css" rel="stylesheet" href="./styleHealth.css">
<div class='msgln' ><b class='bot' >SAiS </b>Hi, I am SAiS Chatbot your virtual healthcare guide who will help you give information regarding cancer.<br>
Before we start please choose one of the five choices<br>
1.What is breast cancer <br>
2.What is colorectal cancer <br>
3.Methods to identify cancer in asymptomatic people<br>
4.treatment methods for breast cancer <br>
5.treatments methods for colorectal cancer<br> </div >
(1,2,3,4,5)""")
Text_to_speech("""Hi, I am SAiS Chatbot your virtual healthcare guide who will help you give information regarding cancer.
Before we start please choose one of the five choices.
1.What is breast cancer.
2.What is colorectal cancer.
3.Methods to identify cancer in asymptomatic people.
4.treatment methods for breast cancer.
5.treatments methods for colorectal cancer.""")
f.close()

@eel.expose
def convert(msg):
    global beg, mute, context
    print(msg)
    with open("./assets/log.html", "a") as message:
        message.write("\n")
        message.write(f"<div class='msglnuser' >%s<b class='user' > You</b><br> </div >" % (msg))
    global output
    ##Beginning Only
    if beg==True:
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
    #Beginning End
    

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
    except:
        pass
    
    with open("./assets/log.html", "a") as bot:
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


eel.start('index - Chat.html', size=(800, 600))
settings["mute"] = mute

with open("settings.json", "w") as outfile:
    json.dump(settings, outfile)