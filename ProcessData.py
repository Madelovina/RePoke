import numpy as np
import os
import pickle
import time
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D
from tensorflow.keras.callbacks import TensorBoard, ModelCheckpoint

NAME = "RePoke_CNN_{}".format(int(time.time()))

tensorboard = TensorBoard(log_dir="tb_logs\{}".format(NAME))
filepath = "best_val_acc_model.hdf5"
modelcheckpoint = ModelCheckpoint(
    filepath,
    monitor="val_accuracy",
    verbose=0,
    save_best_only=True,
    mode="max",)

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

IMG_SIZE = 100

X = pickle.load(open("X.pickle", "rb"))
y = pickle.load(open("y.pickle", "rb"))

X = np.array(X)
y = np.array(y)

# normalize data
X = X.reshape(X.shape[0], IMG_SIZE, IMG_SIZE, -1)
X = X.astype("float64")
X /= 255
y = keras.utils.to_categorical(y, 151)


def createModel():
    try:
        model = load_model("best_val_acc_model.hdf5")
        print("Successfully loaded model")
        return model
    except Exception as e:
        print("Error importing model")
        print("Creating new model")

        model = Sequential()
        model.add(Conv2D(32, kernel_size=(3, 3),
                         activation='relu',
                         input_shape=(IMG_SIZE, IMG_SIZE, 3)))
        model.add(Conv2D(64, (3, 3), activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))
        model.add(Flatten())
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(151, activation='softmax'))

        model.compile(loss="categorical_crossentropy",
                      optimizer=keras.optimizers.Adadelta(), metrics=['accuracy'])
        return model


model = createModel()
model.fit(X, y, batch_size=16, epochs=1,
          validation_split=0.1, callbacks=[tensorboard, modelcheckpoint])

model.save("RePoke_Gen1.model")
