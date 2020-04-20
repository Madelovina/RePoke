import numpy as np
import matplotlib.pyplot as plt  # RGB
import os.path
import cv2  # BGR
import random
import pickle

DATADIR = "D:/kkya5/Pictures/Datasets/Pokemon"
CATEGORIES = os.listdir(DATADIR)
IMG_SIZE = 300


def create_training_data():
    training_data = []
    for category in CATEGORIES:
        # Gets into each pokemon directory
        path = os.path.join(DATADIR, category)
        class_num = CATEGORIES.index(category)
        temp_data = []
        for img in os.listdir(path):
            if len(temp_data) == 50:
                break
            try:
                # convert BGR to RGB
                img_array = cv2.imread(os.path.join(path, img))
                img_array = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)

                # normalize image
                new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
                temp_data.append([new_array, class_num])
            except Exception as e:
                pass
        training_data = training_data+temp_data
    return training_data


training_data = create_training_data()
random.shuffle(training_data)

X = []
y = []

for features, label in training_data:
    X.append(features)
    y.append(label)

print(len(X))
print(len(y))

X = np.array(X).reshape(-1, IMG_SIZE, IMG_SIZE, 3)

pickle_out = open("X.pickle", "wb")
pickle.dump(X, pickle_out)
pickle_out.close()

pickle_out = open("y.pickle", "wb")
pickle.dump(y, pickle_out)
pickle_out.close()
