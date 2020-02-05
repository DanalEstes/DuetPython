# DuetPython
Python utilities for Duet RepRap based 3D printers, including D3+Pi

## find_nozzle.py
Uses OpenCV machine vision to find circles in a camera view. 
Assumes USB camera.  Could be changed for PiCam. 
Requires: OpenCV.  Runs on: Whatever machine owns the camera

## getCoordsDemo.py
Returns a JSON object with coordinates of axis of a Duet printer
Auto-senses RRF2 vs RRF3 printers. 
Requires: Nothing.  Runs on: Any machine that can reach the printer via the network. 
Does not support Duet passwords at this time. 

## toolAlignImageDuet.py
Creates G10 commands for tool-to-tool alignment on a multi-tool printer. 
Uses the human being for image alignment. 
Interfaces to printer to fetch XY (using getCoord from above)
Requires: OpenCV.  Runs on: Whatever machine owns the camera and can reach the printer via the network. 

## toolAlignImage.py
Creates G10 commands for tool-to-tool alignment on a multi-tool printer. 
Uses the human being for image alignment. 
Uses the Human Bieng to enter XY coordinates. 
Requires: OpenCV.  Runs on: Whatever machine owns the camera 
Should work for ANY toolchanging printer. 

