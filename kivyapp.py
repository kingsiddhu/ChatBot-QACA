from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.card import MDCard
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
#import os
#import pyttsx3
import random
from chatbot import *
#from playsound import playsound

#engine = pyttsx3.init()
""" RATE"""
#rate = engine.getProperty('rate')   # getting details of current speaking rate
#print (rate)                        #printing current voice rate
#engine.setProperty('rate', 125)     # setting up new voice rate


"""VOLUME"""
#volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
#print (volume)                          #printing current volume level
#engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1

"""VOICE"""
#voices = engine.getProperty('voices')       #getting details of current voice
#engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
#engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female

beg = True
mute = False
def Text_to_speech(Message):
    global mute#, engine
    """if not mute:
        engine.say(Message)
        engine.runAndWait()
        engine.stop()"""



def getResponse(ints, intents_json):
    print(ints)
    try:
        tag = ints[0]['intent']
    except:
        return ("Sorry can I cannot understand.",0)
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag'] == tag):
            try:
                result = (random.choice(i['responses']), i["context"][0], "prev")
            except:
                result = (random.choice(i['responses']),1)
            break
    return result


def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    print(res)
    return res



output = ""


class User(MDCard):
    text = StringProperty()
    font_size = NumericProperty()

class Response(MDCard):
    text = StringProperty()
    font_size = NumericProperty()

class ChatScreen(Screen):
    chat_area = ObjectProperty()
    message = ObjectProperty()
    

    def send_message(self):
        self.user_input = self.ids.message.text
        self.ids.message.text = ""
        length = len(self.user_input)
        if length >= 40:
            self.ids.chat_area.add_widget(
                User(text=self.user_input, font_size=17, height = length)
            )
        else:
            self.ids.chat_area.add_widget(
                User(text=self.user_input,font_size= 17)
            )
    def responses(self):
        global beg, mute
        msg = self.user_input
        print(msg)
        global output, context
        if beg==True:
            if msg=='1':
                response=("Breast cancer is a type of cancer that forms in the cells of the breast. It primarily affects breast tissue and can develop in different parts of the breast, most commonly in the ducts that carry milk to the nipple (ductal carcinoma) or the glands that produce milk (lobular carcinoma).<br>",0,)
                
                beg = False
            elif msg=='2':
                response=("Colorectal cancer, also known as bowel cancer or colon cancer, refers to cancer that develops in the colon or rectum. The colon is the large intestine, while the rectum is the final part of the large intestine before the anus. Colorectal cancer typically starts as small, benign growths called polyps, which can gradually develop into cancer over time.",0,)

                beg = False
            elif msg == '3':
                response = ("Image Recognition:  Image recognition is a field of artificial intelligence where computers are trained to interpret and understand visual information, such as images or videos.  In cancer diagnosis, image recognition techniques are used to analyze medical images like X-rays, CT scresponse, and MRIs. Convolutional Neural Networks (CNNs) are a popular type of AI model for image recognition in cancer detection. <br> Genomic Analysis: Genomic analysis involves studying an individual's genetic material (genome) to identify genetic variations and mutations. Genomic analysis can be used to find specific genetic mutations associated with cancer. It's essential for understanding the genetic basis of cancer and can inform personalized treatment strategies. Identifying specific mutations in the BRCA1 and BRCA2 genes, which are linked to an increased risk of breast and ovarian cancer. <br> Screening Tests:<br> Perform specific screening tests that are appropriate for the type of cancer being considered. These tests may include: <br> Mammography for breast cancer <br> Colonoscopy for colorectal cancer",0,)

                beg = False
            elif msg=='4':
                response=("Treatment for breast cancer depends on various factors like the cancer's stage, type, whether it's hormone-sensitive, and an individual's overall health. Here are the primary treatment methods commonly used: Surgery, Radiation Therapy, Chemotherapy, Hormone Therapy, Targeted Therapy, Immunotherapy, Reconstructive Surgery",0,)

                beg = False
            elif msg=='5':
                response=("Treatment for colorectal cancer depends on the stage, location, and individual factors. Here are the primary treatment methods commonly used: Surgery, Radiation Therapy, Chemotherapy, Hormone Therapy, Immunotherapy, Stoma Surgery, Clinical Trials",0,)

                beg = False
            else:
                response = "sorry can you choose from 1 to 5 only for now?"
        else:
            response = chatbot_response(msg)
        

        length = len(str(response[0]))
        if length >= 40:
            self.ids.chat_area.add_widget(
            Response(text="{}".format(response[0]),font_size= 17, height = (length/40)*25+20)
        )
        else:
            self.ids.chat_area.add_widget(
            Response(text="{}".format(response[0]),font_size= 17)
        )
        if response[1]=="Mute":
            mute = True
        elif response[1]=="Talk":
            mute = False
        Text_to_speech(str(response[0]))
        print(response[0])
        print("Context:",response[1])

class ChatApp(MDApp):
    def build(self):
        self.title = "ChatBot"
        self.theme_cls.theme_style = "Dark"
        sm = ScreenManager()
        CH = ChatScreen(name="chat")
        text="""Hi there Before we start please choose one of the five choices.
1.What is breast cancer.
2.What is colorectal cancer.
3.Methods to identify cancer in asymptomatic people.
4.treatment methods for breast cancer.
5.treatments methods for colorectal cancer."""
        CH.ids.chat_area.add_widget( Response(text=text, font_size=17, height = str(len(text))))
        Text_to_speech(text)
        sm.add_widget(CH)
        return sm

ChatApp().run()