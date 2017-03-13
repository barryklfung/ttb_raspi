from lib.label_image import *
import tensorflow as tf
import time

sess = tf.Session()

sess, sm_tensor = initialize_session(sess, 'apple.jpg')

image_data = tf.gfile.FastGFile('banana.jpg', 'rb').read()

time.time
print(classify_image(sess, sm_tensor, image_data))
