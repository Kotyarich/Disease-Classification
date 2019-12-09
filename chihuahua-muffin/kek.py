import tensorflow as tf
from tensorflow import keras

from keras import utils as np_utils
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.optimizers import SGD

import numpy as np
import matplotlib.pyplot as plt
import glob, os
import re

import PIL
from PIL import Image

 # Use Pillow library to convert an input jpeg to a 8 bit grey scale image array for processing.
def jpeg_to_8_bit_greyscale(path, maxsize):
        img = Image.open(path).convert('L')   # convert image to 8-bit grayscale
        # Make aspect ratio as 1:1, by applying image crop.
    # Please note, croping works for this data set, but in general one
    # needs to locate the subject and then crop or scale accordingly.
        WIDTH, HEIGHT = img.size
        if WIDTH != HEIGHT:
                m_min_d = min(WIDTH, HEIGHT)
                img = img.crop((0, 0, m_min_d, m_min_d))
        # Scale the image to the requested maxsize by Anti-alias sampling.
        img.thumbnail(maxsize, PIL.Image.ANTIALIAS)
        return np.asarray(img)

def load_image_dataset(path_dir, maxsize):
        images = []
        labels = []
        os.chdir(path_dir)
        for file in glob.glob("*.jpg"):
                img = jpeg_to_8_bit_greyscale(file, maxsize)
                if re.match('chihuahua.*', file):
                        images.append(img)
                        labels.append(0)
                elif re.match('muffin.*', file):
                        images.append(img)
                        labels.append(1)
        return (np.asarray(images), np.asarray(labels))


maxsize_w = 100
maxsize_h = 100

maxsize = maxsize_w, maxsize_h
(train_images, train_labels) = load_image_dataset('C:\\Users\\mrado\\OneDrive\\Desktop\\Hackathon\\chihuahua-muffin\\train_set', maxsize)
(test_images, test_labels) = load_image_dataset('C:\\Users\\mrado\\OneDrive\\Desktop\\Hackathon\\chihuahua-muffin\\test_set', maxsize)

train_images.shape
print(test_labels)

class_names = ['chihuahua', 'muffin']
def display_images(images, labels):
        plt.figure(figsize=(10,10))
        grid_size = min(25, len(images))
        for i in range(grid_size):
                plt.subplot(5, 5, i+1)
                plt.xticks([])
                plt.yticks([])
                plt.grid(False)
                plt.imshow(images[i], cmap=plt.cm.binary)
                plt.xlabel(class_names[labels[i]])


train_images = train_images / 255.0
test_images = test_images / 255.0

 # Setting up the layers.

first_model = keras.Sequential([
    keras.layers.Flatten(input_shape=(100, 100)),
        keras.layers.Dense(128, activation=tf.nn.sigmoid),
        keras.layers.Dense(16, activation=tf.nn.sigmoid),
    keras.layers.Dense(2, activation=tf.nn.softmax)
])
sgd = keras.optimizers.SGD(lr=0.01, decay=1e-5, momentum=0.7, nesterov=True)

first_model.compile(optimizer=sgd,
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

first_model_history=first_model.fit(train_images, train_labels, epochs=100)

test_loss, test_acc = first_model.evaluate(test_images, test_labels)
print('Test accuracy:', test_acc)

predictions = first_model.predict(test_images)
display_images(test_images, np.argmax(predictions, axis = 1))
plt.show()
second_model_history=second_model.fit(train_images, train_labels, epochs=100)

def plot_history(histories, key='accuracy'):
  plt.figure(figsize=(16,10))

  for name, history in histories:
    val = plt.plot(history.epoch, history.history[key],
                   '--', label=name.title()+' Val')
    plt.plot(history.epoch, history.history[key], color=val[0].get_color(),
             label=name.title()+' Train')

  plt.xlabel('Epochs')
  plt.ylabel(key.replace('_',' ').title())
  plt.legend()

  plt.xlim([0,max(history.epoch)])

plot_history([('Первая модель', first_model_history),
              ('Вторая модель', second_model_history)])


