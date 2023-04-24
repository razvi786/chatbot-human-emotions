import random
import json

import torch
import requests

from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
from transformers import pipeline

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents.json', 'r') as json_data:
    intents = json.load(json_data)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Chatbot"

def get_response(msg):
    sentence = tokenize(msg)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                return random.choice(intent['responses'])
    
    return "I do not understand"

def get_mood(msg):
    classifier = pipeline('sentiment-analysis')
    result = classifier(msg)[0]
    label = result['label']
    if label == 'POSITIVE':
        return 'happy'
    elif label == 'NEGATIVE':
        return 'sad'
    else:
        return 'neutral'
    
def get_mood_percentage(msg):
    classifier = pipeline('sentiment-analysis')
    result = classifier(msg)[0]
    score = result['score']
    print("score: ",score)
    return int(score * 100)
    

def get_emotion(msg):
    url = "https://twinword-emotion-analysis-v1.p.rapidapi.com/analyze/"
    payload = "text=" + msg
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "X-RapidAPI-Key": "64d87dd436mshefe48ec0629431cp10fb43jsneb521a7817b3",
        "X-RapidAPI-Host": "twinword-emotion-analysis-v1.p.rapidapi.com"
    }
    # response = requests.request("POST", url, data=payload, headers=headers)
    # response = response.json()
    response = {
        'emotions_detected': ['joy', 'surprise'],
        'emotion_scores': {'joy': 0.19989328226926473, 'surprise': 0.07104711614022974, 'disgust': 0, 'sadness': 0, 'anger': 0, 'fear': 0},
        'thresholds': {'disgust': 0.04, 'sadness': 0.04, 'anger': 0.04, 'joy': 0.04, 'surprise': 0.04, 'fear': 0.04},
        'version': '7.5.3',
        'author': 'twinword inc.',
        'email': 'help@twinword.com',
        'result_code': '200',
        'result_msg': 'Success'
    }
    print("response: ",response)
    result = [];
    if response is not None:
        if len(response['emotions_detected']) != 0:
            result = response['emotions_detected']
    
    print("result: ",result)
    return result






"""
i am going to create some functions here to work on how chat begin when chat start with chatbot
how chatbot give response to user using nltk and torch libraries
how  model and neuralnet will use here 

"""