#!/usr/bin/env python
import requests
import cv2
import ptz
import numpy as np

CAMERA_URL = "http://192.168.0.108/axis-cgi/com/ptz.cgi"
CAM_AUTH = requests.auth.HTTPDigestAuth('root', 'mhwirth')

GAIN = 10

#payload = { 'rpan':'10' }
#response = requests.post(CAMERA_URL, data=payload, auth=CAM_AUTH)

window = np.zeros((1,1,3), np.uint8)

while True:
    cv2.namedWindow('Joystick')
    cv2.imshow('Joystick',window)

    key = cv2.waitKey(1)
    if key == 27:
        exit(0)
    elif key == 2490368:
        print "Up"
        ptz.tilt(-GAIN)
    elif key == 2621440:
        print "Down"
        ptz.tilt(GAIN)
    elif key == 2555904:
        print "Right"
        ptz.relative_pan(-GAIN)
    elif key == 2424832:
        print "Left"
        ptz.relative_pan(GAIN)