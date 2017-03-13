from __future__ import print_function
import numpy as np
import picamera
import picamera.array
import datetime
import logging
import picamera

#parameters
MotionMax = 60
AnalysisInterval = 0.1 #seconds
InitialDelay = 1 #second

class DetectMotion(picamera.array.PiMotionAnalysis):
      motion_max = 60
      interval = 1 #seconds
      SufficientlyStill = False
      last_capt_time = datetime.datetime.now()
      def setParams(self,mm, intvl):
          self.motion_max = mm
          self.interval = intvl
          self.last_capt_time = datetime.datetime.now()
      def WasStill(self):
        return self.SufficientlyStill
      def resetStill(self):
        self.SufficientlyStill = False
      def analyse(self, a):
        #Some parameters and stillness parameters used.
        if datetime.datetime.now() > self.last_capt_time + \
            datetime.timedelta(seconds=self.interval):
            #take the euclidean distance of the motion vector
            a = np.sqrt( np.square(a['x'].astype(np.float)) + np.square(a['y'].astype(np.float))).clip(0, 255).astype(np.uint8)
            if (a > self.motion_max).sum() < 10:
                self.SufficientlyStill = True
            self.last_capt_time = datetime.datetime.now()

def WaitForStill(InitialDelay,AnalysisInterval,MotionMax):
    # The 'analyse' method gets called on every frame processed while picamera
    # is recording h264 video.
    # It gets an array (see: "a") of motion vectors from the GPU.
    
    camera = picamera.PiCamera()
    with DetectMotion(camera) as output:
        camera.resolution = (640, 480)
        camera.framerate= 10
        output.setParams(MotionMax,AnalysisInterval)
        # record video to nowhere, as we are just trying to capture images:
        camera.start_recording('/dev/null', format='h264', motion_output=output)
        while not output.WasStill():
            camera.wait_recording(AnalysisInterval)
        camera.stop_recording()
        output.resetStill()
    camera.close()
if __name__ == "__main__":
    filename = open('testimage.jpg','wb')
    print("Testing waiting module. Time is", datetime.datetime.now())
    WaitForStill(InitialDelay, AnalysisInterval, MotionMax)
    camera = picamera.PiCamera()
    camera.capture(filename)
    print("It's still. Time is", datetime.datetime.now())
    filename.close()
