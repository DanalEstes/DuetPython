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
    tc=input("How many tools to align?\n")
    tc = int(tc)
    if (tc < 2): tc = 2
    print("IMPORTANT: Before proceeding, enter the commands below in Duet Web console.")
    for tool in range(0,tc):
        print("G10 P{} X0 Y0".format(tool))
    print("It is OK to copy/paste, one line at a time.")
    print("")
    for tool in range(0,tc):
        print("Use Duet Web to align Tool {} with green circle.".format(tool))
        string = input("After alignment, Input X coordinate from Duet Web:\n")
        x.append(float(string))
        string = input("Input Y coordinate from Duet Web:\n")
        y.append(float(string))

def report():
    print("")
    for tool in range(0,len(x)):
        xd = np.around(x[0] - x[tool],2)
        yd = np.around(y[0] - y[tool],2)
        print("G10 P{} X{} Y{}".format(tool,xd,yd))
    print("")
    print("NOTE: Each G10 above will also have a Z component, not shown here.")    


#######################
# Main Code Starts Here
#######################
th = threading.Thread(target=imageStream)
th.daemon = True # Thread will be killed when main exits.
th.start()

userInterface()

report()
