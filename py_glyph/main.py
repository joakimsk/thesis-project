#!/usr/bin/env python
import cv2
import urllib 
import numpy as np

stream=urllib.urlopen('http://root:Wtfr0lfe@129.241.154.82/mjpg/video.mjpg')
bytes=''
while True:
    bytes+=stream.read(1024)
    a = bytes.find('\xff\xd8')
    b = bytes.find('\xff\xd9')
    if a!=-1 and b!=-1:
        jpg = bytes[a:b+2]
        bytes= bytes[b+2:]
        i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.CV_LOAD_IMAGE_COLOR)
        blur = cv2.GaussianBlur(i,(5,5),0)
        edges = cv2.Canny(blur, 100, 200)
        cv2.imshow('i',edges)
        if cv2.waitKey(1) ==27:
            exit(0)