#!/usr/bin/env python
import cv2
import sys
import numpy as np
import requests
import random

CV_LOAD_IMAGE_COLOR = 1
CAMERA_URL = "http://192.168.0.108/mjpg/video.mjpg"

def grab_frame(capture_device, is_cctv):
    if is_cctv == False:
        ret, img = capture_device.read()
        return img
    else:
        bytes=''
        while True:
            bytes+=capture_device.raw.read(1024)
            a = bytes.find('\xff\xd8')
            if a !=-1:
                b = bytes.find('\xff\xd9', a)
                if a!=-1 and b!=-1:
                    jpg = bytes[a:b+2]
                    bytes= bytes[b+2:]
                    i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), CV_LOAD_IMAGE_COLOR)
                    return i

print "Using CCTV MJPEG stream"
session = requests.Session()
auth = requests.auth.HTTPDigestAuth('ptz', 'ptz')
request = requests.Request("GET", CAMERA_URL).prepare()
request.prepare_auth(auth)
capture_device = session.send(request, stream=True)

while True:
    source = grab_frame(capture_device, True) # SET TO TRUE FOR CCTV STREAM
    h_source, w_source, c_source = source.shape
    cv2.namedWindow('Source')
    cv2.imshow('Source',source)
    key = cv2.waitKey(1)
    if key == 27:
        exit(0)