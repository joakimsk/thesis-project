#!/usr/bin/env python
'''
py_camsnapshot.py
===========
initial revision

py_camsnapshot.py will iterate through cams.csv and grab a snapshot of each camera.
Requires MJPEG access to CCTV-camera and correct connection string.

cams.csv:  # Description; Target folder name; Connection string
"House camera";cam1;http://ptz:ptz@129.241.154.82/mjpg/video.mjpg
"Dog camera";cam2;http://ptz:ptz@129.241.154.81/mjpg/video.mjpg

log.txt: # Date and time of capture;Target folder name; Was picture captured?
2014-10-01 20:04:12.285000;cam1;True
2014-10-01 20:04:12.285000;cam2;False
2014-10-01 20:04:56.731000;cam1;True
2014-10-01 20:04:56.731000;cam2;True

Dependencies
------------
- Python 2.7
- OpenCV
- Numpy


Tested on Windows 7
By Joakim Skjefstad for Project Thesis NTNU 2014
skjefstad.joakim@gmail.com
'''
import cv2
import urllib 
import numpy as np
import time
import os
import csv
import calendar
import socket
from datetime import date
from datetime import datetime

timeout = 2 # Seconds before urllib requesting MJPEG stream times out
socket.setdefaulttimeout(timeout)

today = date.today()
utcdate = datetime.utcnow()

cameras = []

class Camera(object):
    description = ""
    target_folder = ""
    connection_string = ""
    def __init__(self, description, target_folder, connection_string):
        self.description = description
        self.target_folder = target_folder
        self.connection_string = connection_string
        
    def __str__(self):
        return "Camera %s %s %s" % (self.description, self.target_folder, self.connection_string)

    def captureSnapshot(self):
        try:
            stream=urllib.urlopen(self.connection_string)
        except:
            print "Failed urllib request"
            return False
        bytes=''
        for i in range(1,1024): # A finite loop, in case of errors, to avoid system overload
            bytes+=stream.read(1024)
            a = bytes.find('\xff\xd8')
            b = bytes.find('\xff\xd9')
            if a!=-1 and b!=-1: # If JPEG boundaries are found
                jpg = bytes[a:b+2]
                bytes= bytes[b+2:]
                img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.CV_LOAD_IMAGE_COLOR)
                
                d = datetime.utcnow()
                unix_timestamp = str(calendar.timegm(d.utctimetuple()))
                
                if not os.path.exists(self.target_folder):
                    os.mkdir(self.target_folder)
                target_file = self.target_folder + today.strftime("%d%m%y") + '_' + unix_timestamp + '.png'
                cv2.imwrite(os.path.join(self.target_folder, target_file), img)
                print 'Data transfer loops:',i
                return True
        return False
        
        
with open('cams.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=';', quotechar='"')
    for row in reader:
        cameras.append(Camera(row[0], row[1], row[2]))

log = open('log.txt', 'a')

        
for camera in cameras:
    log.write(str(utcdate) + ';' + str(camera.target_folder) + ';' + str(camera.captureSnapshot()) + '\n')
    print "Capturing", camera
    

print "Completed capturing, shutting down program."    
exit(0)

