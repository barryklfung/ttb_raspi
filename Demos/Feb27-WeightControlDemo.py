#Standard
import picamera.array
import picamera
#import matplotlib.pyplot as plt
import cv2
import RPi.GPIO as GPIO
import time
import sys 

#Personal stuff
from lib.MotionDetection import WaitForStill
import lib.HX711 as HX711
from lib.lcd import *

startup_lcd()
#we use the BCM numbering for ease of use.
GPIO.setmode(GPIO.BCM)

#Parameters
WEIGHT_STD = 0.6 #our tolerance for what is a steady object.
REF_UNITS = 70
DOUT_PIN = 20
SCK_PIN = 21

MOT_MAX = 60
MOT_ANALYSIS_INT = 0.1 #seconds

#initializing the weight sensor
hx = HX711.HX711(20,21,32)
hx.set_reference_unit(700)
time.sleep(1)
hx.reset()
hx.tare(3)
hx.reset()
#the money loop
screen_res = 1280, 720
scale_width = screen_res[0] / 640
scale_height = screen_res[1] / 480
scale = min(scale_width, scale_height)
window_width = int(640 * scale)
window_height = int(480 * scale)

cv2.namedWindow('dst_rt', cv2.WINDOW_NORMAL)
cv2.resizeWindow('dst_rt', window_width, window_height)

        
while True:
    print "Waiting for change in weight"
    waiting_lcd()
    weight = hx.wait_for_delta(WEIGHT_STD,MOT_ANALYSIS_INT);
    print "Detected weight: ", weight
    detected_lcd()
    if abs(weight) > WEIGHT_STD:
        print "Waiting for motion to finish"
        WaitForStill(0, MOT_ANALYSIS_INT, MOT_MAX)
        with picamera.PiCamera() as camera:
            camera.resolution = (640, 480)
            cap = picamera.array.PiRGBArray(camera)
            camera.capture(cap,format="bgr")
            img = cap.array
            #- display with OpenCV        
            cv2.imshow('dst_rt', img)
            cv2.waitKey(0)
