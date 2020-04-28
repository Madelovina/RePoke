import cv2
import tensorflow as tf
import os

DATADIR = "D:/kkya5/Pictures/Datasets/PokemonGame"
CATEGORIES = os.listdir(DATADIR)


def prepare(filepath):
    IMG_SIZE = 100
    img_array = cv2.imread(filepath)
    img_array = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)
    new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
    return new_array.reshape(-1, IMG_SIZE, IMG_SIZE, 3)/255


model = tf.keras.models.load_model("RePoke_Gen1.model")

prediction = model.predict_classes([prepare("whosthatpokemon.png")])
print(CATEGORIES[int(prediction)])
