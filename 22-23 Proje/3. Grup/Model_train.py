import json
import random
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from transformers import BertTokenizer
import nltk
import transformers
import torch
import warnings
from typing import Tuple, Union
from transformers import AutoModel, AutoTokenizer
from snowballstemmer import TurkishStemmer


warnings.filterwarnings("ignore")

# Türkçe BERT modeli yükleniyor
tokenizer = transformers.BertTokenizer.from_pretrained('bert-base-uncased')
bert_model = AutoModel.from_pretrained("C:/Users/svimu/Desktop/asistant/bert-base-turkish-cased")

# Veri seti yükleniyor
with open('C:/Users/svimu/Desktop/asistant/input/intents.json') as json_veri:
    intents = json.load(json_veri)

# Lancaster Stemmer kullanarak kelimeleri köklerine ayırıyoruz
stemmer = TurkishStemmer()

# Veri setindeki kelimelerin tamamı alınarak bir kelime listesi oluşturuluyor
words = []
classes = []
documents = []
ignore_words = ['?']

for intent in intents['intents']:
    for pattern in intent['patterns']:
        # Cümleler wordse ayrılıyor
        w = nltk.word_tokenize(pattern)
        words.extend(w)
        documents.append((w, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

words = [stemmer.stemWord(w.lower()) for w in words if w not in ignore_words]
words = sorted(list(set(words)))

classes = sorted(list(set(classes)))

# Eğitim veri seti oluşturuluyor
training = []
output = []

output_empty = [0] * len(classes)

for doc in documents:
    veri_kumesi = []
    pattern_words = doc[0]
    pattern_words = [stemmer.stemWord(word.lower()) for word in pattern_words]
    for w in words:
        if w in pattern_words:
            veri_kumesi.append(1)
        else:
            veri_kumesi.append(0)
    output_row = [0] * len(classes)
    output_row[classes.index(doc[1])] = 1

    training.append([veri_kumesi, output_row])

random.shuffle(training)
training = np.array(training)

# Eğitim ve test setleri oluşturuluyor
train_x = list(training[:, 0])
train_y = list(training[:, 1])

# BERT modeline uygun girdi oluşturuluyor
def get_bert_input(text):
    input_dict = tokenizer(text, return_tensors='pt', padding='max_length', truncation=True, max_length=128)
    return {key: val[0] for key, val in input_dict.items()}
train_x = ["Bu pozitif bir cümle.", "Bu negati bir cümle."]
train_x = [get_bert_input(text) for text in train_x]
train_y = torch.tensor([1, 0])



# Yapay sinir ağı modeli oluşturuluyor
input_word_ids = tf.keras.layers.Input(shape=(train_x[0]['input_word_ids'].shape[1],), dtype=tf.int32,
                                       name="einput_word_ids")
input_mask = tf.keras.layers.Input(shape=(train_x[0]['input_mask'].shape[1],), dtype=tf.int32,
                                   name="input_mask")
input_type_ids = tf.keras.layers.Input(shape=(train_x[0]['input_type_ids'].shape[1],), dtype=tf.int32,
                                        name="input_type_ids")
bert_inputs = [input_word_ids, input_mask, input_type_ids]
bert_model = AutoModel.from_pretrained("C:/Users/svimu/Desktop/asistant/bert-base-turkish-cased")
bert_sequence_output = bert_model({'input_word_ids': input_word_ids, 'input_mask': input_mask, 'input_type_ids': input_type_ids})[0]
net = tf.keras.layers.Dense(128, activation='relu')(bert_sequence_output)
net = tf.keras.layers.Dropout(0.5)(net)
net = tf.keras.layers.Dense(64, activation='relu')(net)
net = tf.keras.layers.Dropout(0.5)(net)
output = tf.keras.layers.Dense(len(classes), activation='softmax')(net)
model = tf.keras.models.Model(inputs=bert_inputs, outputs=output)

# Model derleniyor
optimizer = tf.keras.optimizers.Adam(learning_rate=0.0001)
model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])

# Model eğitiliyor
model.fit(train_x, train_y, epochs=200, batch_size=8)

# Model kaydediliyor
tf.keras.models.save_model(model, 'model.tflearn')