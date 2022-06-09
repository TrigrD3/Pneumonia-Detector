import tensorflow as tf
import base64
import io
import numpy as np
from PIL import Image
from keras.preprocessing import image

from google.cloud import storage

# Enable Cloud Storage
client = storage.Client()

# Reference an existing bucket.
bucket = client.get_bucket('pristine-sphere-343506.appspot.com')

# Download a file from your bucket.
model_ml = bucket.get_blob('ML_Model/model.h5')
model_ml.download_to_filename('model.h5')


model = tf.keras.models.load_model(model_ml)
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

def preprocess_image(img, target_size):
    if img.mode != "RGB":
        img = img.convert("RGB")
    
    img = img.resize(target_size)
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = img/255
    return img

def predict(data):
    img = Image.open(data)
    processed_image = preprocess_image(img, target_size=(224, 224))

    images = np.vstack([processed_image])
    classes = model.predict(processed_image, batch_size=10)
    label = np.where(classes[0] > 0.5, 1,0)
    print(label)   
    if label[0]==1:
        return ("normal") 
    elif label[1]==1:
        return ("covid") 
    elif label[2]==1:
        return ("bacterial") 
    else:
        return ("viral")