#Standard
import picamera
import RPi.GPIO as GPIO
import time
import sys
import tensorflow as tf
import requests

#Personal stuff
from lib.MotionDetection import WaitForStill
import lib.HX711 as HX711
from lib.lcd import *
from lib.label_image import *

#Tell the world how we doin it
startup_lcd()
#we use the BCM numbering for ease of use.
GPIO.setmode(GPIO.BCM)

#Parameters
WEIGHT_STD = 6 #our tolerance for what is a steady object.
REF_UNITS = 75
DOUT_PIN = 20
SCK_PIN = 21

MOT_MAX = 60
MOT_ANALYSIS_INT = 0.1 #seconds

filename = 'temp.jpg'

#initializing tensorflow net:
sess = tf.Session()
sess, sm_tensor = initialize_session(sess, 'apple.jpg')

#initializing the weight sensor
hx = HX711.HX711(20,21,32)
hx.set_reference_unit(REF_UNITS)
time.sleep(1)
hx.reset()
hx.tare(3)
hx.reset()


#the money loop
        
waiting_lcd()
try:
    while True:
        weight = hx.wait_for_delta(WEIGHT_STD,MOT_ANALYSIS_INT);
        detected_lcd()
        if abs(weight) > WEIGHT_STD:
            WaitForStill(0, MOT_ANALYSIS_INT, MOT_MAX)
            analyzing_lcd()
            with picamera.PiCamera() as camera:
                camera.resolution = (128, 96)
                camera.zoom = (0.1,0.1,0.8,0.8)
                camera.capture(filename)
            now = time.time()
            label = classify_image(sess, sm_tensor, tf.gfile.FastGFile(filename, 'rb').read(), 0.3)
            print('Classification took: ', time.time() - now)
            if label != "Error":
                 classified_lcd(label, weight)
                 print("Label", label, "Weight", weight)
                 requests.post("https://turnipthebeets.herokuapp.com/inventory/r = requests.post('https://turnipthebeets.herokuapp.com/inventory/", json={'item':label, 'mass':weight})
            else:
                errorclass_lcd()
        else:
            waiting_lcd()
except:
    clear_lcd()
