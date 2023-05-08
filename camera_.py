#Modified by smartbuilds.io
#Date: 27.09.20
#Desc: This scrtipt script..
import os
import argparse
import sys
from threading import Thread
import importlib.util


import cv2
from imutils.video.pivideostream import PiVideoStream
import imutils
import time
from datetime import datetime
import numpy as np
from tfl import model


class VideoCamera(object):
    def __init__(self, resolution=(640,480), framerate=30, flip = False, file_type  = ".jpg", photo_string= "stream_photo"):
        # self.vs = PiVideoStream(resolution=(1920, 1080), framerate=30).start()
        # Initialize the PiCamera and the camera image stream
        self.stream = cv2.VideoCapture(0)
        ret = self.stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        ret = self.stream.set(3,resolution[0])
        ret = self.stream.set(4,resolution[1])
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False
        
        self.flip = flip # Flip frame vertically
        self.file_type = file_type # image type i.e. .jpg
        self.photo_string = photo_string # Name to save the photo
        time.sleep(2.0)
    
    def start(self):
	# Start the thread that reads frames from the video stream
        Thread(target=self.update,args=()).start()
        return self
    
    def update(self):
        # Keep looping indefinitely until the thread is stopped
        while True:
            # If the camera is stopped, stop the thread
            if self.stopped:
                # Close camera resources
                self.stream.release()
                return

            # Otherwise, grab the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()

    def __del__(self):
        self.stopped = True

    def flip_if_needed(self, frame):
        if self.flip:
            return np.flip(frame, 0)
        return frame

    def get_frame(self):
        
        frame1 = self.flip_if_needed(self.frame)
        frame = model.detect(frame1)
        ret, jpeg = cv2.imencode(self.file_type, frame)
        #self.previous_frame = jpeg
        return jpeg.tobytes()
        #return self.frame

    # Take a photo, called by camera button
    def take_picture(self):
        frame = self.flip_if_needed(self.vs.read())
        ret, image = cv2.imencode(self.file_type, frame)
        today_date = datetime.now().strftime("%m%d%Y-%H%M%S")
        cv2.imwrite("Security_snapshots/" + str(self.photo_string + "_" + today_date + self.file_type), frame)
