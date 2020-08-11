from tensorflow import keras
from tensorflow.keras.models import load_model
import tensorflow as tf
import numpy as np
from pathlib import Path

img_height = 350
img_width = 350
class_names = ["1", "2", "3", "4", "5"]

# load the model
beautyScore_model = load_model("beautyScore.h5")

# rgear_url = "https://i.pinimg.com/236x/a2/4f/35/a24f351c4149f0fc2da71efa77599297.jpg"
# rgear_path = tf.keras.utils.get_file('a24f351c4149f0fc2da71efa77599297', origin=rgear_url)

# img = keras.preprocessing.image.load_img(
#     rgear_path, target_size=(img_height, img_width)
# )
# img_array = keras.preprocessing.image.img_to_array(img)
# img_array = tf.expand_dims(img_array, 0) # Create a batch

# predictions = beautyScore_model.predict(img_array)
# score = tf.nn.softmax(predictions[0])

# print(
#     "This image has a beauty score of {} with a {:.2f} percent confidence."
#     .format(class_names[np.argmax(score)], 100 * np.max(score))
# )

# imageFiles = Path('Images').glob("*/*")
imageFiles = Path('images-test1').glob("*")
for imgPath in imageFiles:
    print(imgPath)
    img = keras.preprocessing.image.load_img(imgPath, target_size=(img_height, img_width))
    img_array = keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0) # Create a batch

    predictions = beautyScore_model.predict(img_array)
    score = tf.nn.softmax(predictions[0])

    print(f"This image has a beauty score of {class_names[np.argmax(score)]} with a {100 * np.max(score):.2f} percent confidence.")