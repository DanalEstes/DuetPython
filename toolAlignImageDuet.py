# Python Script to align multiple tools on Jubilee printer
# Using images from USB camera and pulling positions from
# the printer via web interface.
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
import requests
import json
import sys

# initialize the video stream and allow the cammera sensor to warmup
vs = cv2.VideoCapture(0)
time.sleep(2.0)
avg=[0,0]
count=0
x = []
y = []

# Globals to make getCoords work
endpoint2='/rr_status?type=1'   # RRF2 request
endpoint3='/machine/status'     # RRF3 request
endpointA=endpoint2             # Active
def getCoords(base_url):
    global endpointA
    if (endpointA == endpoint2):
        try:
            r = requests.get(f'{base_url}{endpointA}')
            j=json.loads(r.text)
            jc=j['coords']['xyz']
            ret=json.loads('{}')
            for i in range(0,len(jc)):
                ret[ 'xyz'[i] ] = jc[i] 
            return(ret)
        except:
            endpointA = endpoint3
    if (endpointA == endpoint3):    
        try:
            r = requests.get(f'{base_url}{endpointA}')
            j=json.loads(r.text)
            ja=j['result']['move']['axes']
            jd=j['result']['move']['drives']
            ad=json.loads('{}')
            for i in range(0,len(ja)):
                ad[ ja[i]['letter'] ] = ja[i]['drives'][0]
            ret=json.loads('{}')
            for i in range(0,len(ja)):
                ret[ ja[i]['letter'] ] = jd[i]['position']
            return(ret)
        except:
            print(base_url," does not appear to be a RRF2 or RRF3 printer", file=sys.stderr)
            raise

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
    ip=input("Please enter IP or name of printer:\n")
    tc=input("How many tools to align?\n")
    tc = int(tc)
    if (tc < 2): tc = 2
    for tool in range(0,tc):
        print("G10 P{} X0 Y0".format(tool))
    print("It is OK to copy/paste, one line at a time.")
    print("")
    for tool in range(0,tc):
        print("Use Duet Web to align Tool {} with green circle.".format(tool))
        string = input("After alignment, press enter\n")
        j=getCoords('HTTP://'+ip)
        x.append(float(j['X']))
        y.append(float(j['Y']))
        print('')

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
