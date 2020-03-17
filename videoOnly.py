# Python Script to align multiple tools on Jubilee printer
# Using images from USB camera and user input
#
# Copyright (C) 2020 Danal Estes all rights reserved.
# Released under The MIT License. Full text available via https://opensource.org/licenses/MIT
# 
# Requires OpenCV to be installed on Pi
# Requires running via the OpenCV installed python (that is why no shebang)
import datetime
import time
import cv2
import numpy as np
import threading

# initialize the video stream and allow the cammera sensor to warmup
vs = cv2.VideoCapture(0)
time.sleep(2.0)
avg=[0,0]
count=0
x = []
y = []

def imageStream():
    # loop over the frames from the video stream
    while True:
        (grabbed, frame) = vs.read()

        # draw the timestamp on the frame
        timestamp = datetime.datetime.now()
        ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
        cv2.putText(frame, ts, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,0.90, (255, 255, 255), 1)
        cv2.circle(frame,(320,240),25,(0,255,),3)
        # show the frame
        cv2.imshow("Nozzle", frame)
        key = cv2.waitKey(10)



def userInterface():
    print("")
    tc=input("Press enter to close the window when done. \n")

#######################
# Main Code Starts Here
#######################
th = threading.Thread(target=imageStream)
th.daemon = True # Thread will be killed when main exits.
th.start()

userInterface()
