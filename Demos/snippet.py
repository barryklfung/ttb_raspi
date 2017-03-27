from lib.label_image import *
import tensorflow as tf
import time
import requests

sess = tf.Session()

sess, sm_tensor = initialize_session(sess, 'apple.jpg')

image_data = tf.gfile.FastGFile('banana.jpg', 'rb').read()

label = classify_image(sess, sm_tensor, image_data)
mass = 300
r = requests.post('https://turnipthebeets.herokuapp.com/inventory/', json={'item':label, 'mass':mass})
print (r.json())
