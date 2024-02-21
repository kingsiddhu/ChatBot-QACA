from flask import Flask, request, jsonify
import random
from chatbot import *
app = Flask(__name__)

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
                    result = (random.choice(i['responses']), i["context"][0])
                except:
                    result = (random.choice(i['responses']),None)
                break
    return result


def chatbot_response(msg,context):
    ints = predict_class(msg, model)
    res = getResponse(ints, intents,context)
    return res


@app.route("/")
def home():
    return "Hello"
@app.route("/Hello/<user>")
def hello(user):
    return f"hello {user}"

@app.route("/get-msg/")
def getuser():
    msg = request.args.get("msg")
    context = request.args.get("context")
    msgCalc = chatbot_response(msg,context)
    if msg and context:
        return jsonify({"msg":msgCalc[0],"context":msgCalc[1]}), 200
    else:
        return "Error 204", 204
if __name__ == "__main__":
    app.run(debug=True, port=80)