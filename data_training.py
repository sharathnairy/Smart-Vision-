import os
import numpy as np
from tensorflow.keras.utils import to_categorical
from keras.layers import Input, Dense
from keras.models import Model

X = np.load("pose_data.npy")
y = np.array([0]*len(X))  # 0 means no fighting; 1 means fighting (you will have labels for fighting events)

# Simple binary classification: fighting or not
y = to_categorical(y)

X_new = X.copy()
y_new = y.copy()
counter = 0

cnt = np.arange(X.shape[0])
np.random.shuffle(cnt)

for i in cnt: 
    X_new[counter] = X[i]
    y_new[counter] = y[i]
    counter += 1

# Define simple neural network
ip = Input(shape=(X.shape[1]))
m = Dense(128, activation="tanh")(ip)
m = Dense(64, activation="tanh")(m)
op = Dense(y.shape[1], activation="softmax")(m)

model = Model(inputs=ip, outputs=op)
model.compile(optimizer='rmsprop', loss="categorical_crossentropy", metrics=['acc'])

model.fit(X_new, y_new, epochs=80)

model.save("fight_detection_model.h5")
