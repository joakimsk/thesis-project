#!/usr/bin/env python
import requests
import ptz_advanced
import time

CAMERA_URL = "http://192.168.0.108/axis-cgi/com/ptz.cgi"
CAM_AUTH = requests.auth.HTTPDigestAuth('root', 'mhwirth')

for level in range(0, 10001, 1000):
    ptz_advanced.brightness(level)
    time.sleep(0.2)
    print "Setting brightness level ",level

for level in range(0, 10001, 1000):
    ptz_advanced.focus(level)
    time.sleep(0.2)
    print "Setting focus level ",level
    
for level in range(0, 10001, 1000):
    ptz_advanced.iris(level)
    time.sleep(0.2)
    print "Setting iris level ",level