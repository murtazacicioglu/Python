import nltk
from nltk.stem.snowball import SnowballStemmer
from snowballstemmer import TurkishStemmer
import warnings
import logging
import os
import numpy as np
import tflearn
import tensorflow as tf
import random
import pickle
import json

stemmer = TurkishStemmer()
warnings.filterwarnings("ignore")
logging.getLogger('tensorflow').disabled = True

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

veri = pickle.load( open( "C:/Users/svimu/Desktop/asistant/model/training_data", "rb" ) )

words = veri['words']
classes = veri['classes']
train_x = veri['train_x']
train_y = veri['train_y']

with open('C:/Users/svimu/Desktop/asistant/input/intents.json') as json_veri:
    intents = json.load(json_veri)

tf.compat.v1.reset_default_graph()

# Build neural network 
net = tflearn.input_data(shape=[None, len(train_x[0])]) 
net = tflearn.fully_connected(net, 8) 
net = tflearn.fully_connected(net, 8) 
net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax') 
#Ağı eğitmek için geriye yayılım (backpropagation) ve gradyan inişi (gradient descent) algoritmalarını tanımlıyoruz.
net = tflearn.regression(net) 

#Modeli tanımlıyoruz ve net yapılandırmasını kullanarak derin öğrenme modelini oluşturuyoruz.
model = tflearn.DNN(net)

#Önceden eğitilmiş modeli yükleyerek modeli eğitilmiş modele ayarlıyoruz. "model/model.tflearn" dosyasından ağırlık ve parametreleri yüklüyoruz.
#Dolayısıyla, model.load('model/model.tflearn') ifadesi, 'model.tflearn.index' ve 'model.tflearn.data-00000-of-00001' dosyalarının her ikisini de içeren modeli yükler.
model.load('C:/Users/svimu/Desktop/asistant/model/model.tflearn')

#clean_up_sentence() fonksiyonu, bir cümleyi temizlemek için kullanılır.
def clean_up_sentence(sentence):
    # Cümleyi parçalara ayırma (tokenization)
    sentence_words = nltk.word_tokenize(sentence)
    # Her kelimeyi köküne indirgeme (stemming)
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    return sentence_words

# bow() fonksiyonu -> bir cümle ve kelime listesi alarak veri_kumesi-of-words (BOW) dizisini oluşturur.
def bow(sentence, words, show_details=False):
    sentence_words = clean_up_sentence(sentence)
    veri_kumesi = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                veri_kumesi[i] = 1.
                if show_details: 
                    print ("found in veri_kumesi: %s" % w)

    return(np.array(veri_kumesi))

# ERROR_THRESHOLD değişkeni, sınıflandırma sonuçlarını filtrelemek için kullanılan bir eşik değeridir. Bu değerden düşük olasılıklara sahip classes filtrelenir.
ERROR_THRESHOLD = 0.25

#classify() fonksiyonu, verilen cümleyi sınıflandırmak için kullanılır.
def classify(sentence):
    #model.predict() fonksiyonu, cümle için tahmin olasılıklarını döndürür,cümle üzerinde modelin tahmin yapmasını sağlar.
    results = model.predict([bow(sentence, words)])[0]
    results = [[i,r] for i,r in enumerate(results) if r>ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append((classes[r[0]], r[1]))
    return return_list


#response() fonksiyonu, kullanıcının bir cümle girdisi verdiğinde, bu cümleyi sınıflandırır ve uygun bir yanıt üretir.
def response(sentence, userID='123', show_details=False):
        results = classify(sentence)
        if results:
            while results:
                for i in intents['intents']:
                    if i['tag'] == results[0][0]:
                        if results[0][1] < 0.6:
                            return "0"
                        res = random.choice(i['responses'])
                        return res
                results.pop(0)