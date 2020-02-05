# Python Script to align multiple tools on Jubilee printer
# Using images from USB camera and finding circles in those images
# Circle find needs lots of tuning...
#
# Copyright (C) 2020 Danal Estes all rights reserved.
# Released under The MIT License. Full text available via https://opensource.org/licenses/MIT
#
# Requires OpenCV to be installed on Pi
# Requires running via the OpenCV installed python (that is why no shebang)
import datetime
import imutils
import time
import cv2
import numpy as np

# initialize the video stream and allow the cammera sensor to warmup
vs = cv2.VideoCapture(0)
time.sleep(2.0) 
avg=[0,0]
count=0
# loop over the frames from the video stream
while True:
	(grabbed, frame) = vs.read()

	# draw the timestamp on the frame
	timestamp = datetime.datetime.now()
	ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
	cv2.putText(frame, ts, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,0.90, (255, 255, 255), 1)
	#Find circles
	img = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	img = cv2.medianBlur(img,17)
	circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,50,param1=50,param2=39,minRadius=15,maxRadius=50)
	if (circles is None):
		continue
	circles = np.uint16(np.around(circles))
	for i in circles[0,:]:
		# Keep track of center of circle
		avg[0] += i[0]
		avg[1] += i[1]
		count += 1
		if (count > 15):
			avg[0] /= count
			avg[1] /= count
			avg = np.around(avg,2)
			print(avg[0],avg[1])
			avg = [0,0]
			count = 0
		# draw the circle
		i = np.around(i)
		cv2.circle(frame,(i[0],i[1]),i[2],(0,0,255),3)

	# show the frame
	cv2.imshow("Nozzle", frame)
	key = cv2.waitKey(1)
	#print(ts)
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
