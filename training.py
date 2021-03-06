
import nltk

#nltk.download('punkt')
#nltk.download('wordnet')

from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import random
import json
import pickle

import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation , Dropout
from keras.optimizers import SGD #Stochastic Gradient Descent

from snowballstemmer import stemmer

words=[]
classes = []
documents = []
ignore_words = ['?', '!']
datafile = open('simple.json').read()
intents = json.loads(datafile)

for intent in intents['intents']:
    for pattern in intent['patterns']:
        w = nltk.word_tokenize(pattern)
        words.extend(w)
        
        documents.append((w,intent['tag']))
        
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]
words = sorted(list(set(words)))

print (len(documents), "documents")

print (len(classes), "classes", classes) 

print (len(words), "unique lemmatized words", words) 
pickle.dump(words,open('words.pkl','wb'))
pickle.dump(classes,open('classes.pkl','wb'))




training = []
output_empty = [0] * len(classes)

for doc in documents:
    word_bag = []
    
    pattern_words = doc[0]
    pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]
    
    
    for w in words:
        word_bag.append( 1)  if w in pattern_words else word_bag.append(0)
        
        output_row = list(output_empty)
        output_row[classes.index(doc[1])] = 1

        training.append([word_bag, output_row])
        


random.shuffle(training)
training = np.array(training)
    



x_train = list(training[:,0])
y_train = list(training[:,1])



model = Sequential()

model.add(Dense(128, input_shape = (37,),activation = 'relu'))

model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(y_train[0]), activation='softmax'))

sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])


hist = model.fit(np.array(x_train), np.array(y_train), epochs=15, batch_size=5, verbose=1)

model.save('chatbotmodel.h5', hist)





