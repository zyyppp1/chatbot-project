import nltk
import random
import numpy as np
import json
import pickle
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model

# 下载所需的 NLTK 资源
nltk.download('punkt')
nltk.download('wordnet')

# 初始化词形还原器
lemmatizer = WordNetLemmatizer()

# 加载意图文件和预训练模型
with open('intents.json', 'r') as json_file:
    intents = json.load(json_file)

words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbot_model.keras')

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence.lower())
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    word_dict = {word: index for index, word in enumerate(words)}
    for w in sentence_words:
        if w in word_dict:
            bag[word_dict[w]] = 1
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list

def get_response(intents_list):
    tag = intents_list[0]['intent']
    list_of_intents = intents['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result

def process_input(user_input):
    ints = predict_class(user_input)
    res = get_response(ints)
    return res