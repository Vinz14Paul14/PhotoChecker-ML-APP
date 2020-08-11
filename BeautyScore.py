from tensorflow import keras
from tensorflow.keras.models import load_model
import tensorflow as tf
import numpy as np
from pathlib import Path

img_height = 350
img_width = 350
class_names = ["1", "2", "3", "4", "5"]

# load the saved model
beautyScore_model = load_model("beautyScore.h5")

def get_beauty_score(filename):
    imgPath = Path('static/uploads') / filename
    print(imgPath)
    img = keras.preprocessing.image.load_img(imgPath, target_size=(img_height, img_width))
    img_array = keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0) # Create a batch

    predictions = beautyScore_model.predict(img_array)
    score = tf.nn.softmax(predictions[0])

    beauty_score = class_names[np.argmax(score)]
    percent_confidence = round(100 * np.max(score),2)

    print(f"This image has a beauty score of {beauty_score} with a {percent_confidence:.2f} percent confidence.")

    data = {}
    data['beautyscore'] = beauty_score
    data['confidence'] = percent_confidence
    return data