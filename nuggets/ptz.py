#!/usr/bin/env python

import requests
import os
import math
from time import sleep
clear = lambda: os.system('cls')

CAMERA_URL = "http://192.168.0.108/axis-cgi/com/ptz.cgi"
CAM_AUTH = requests.auth.HTTPDigestAuth('root', 'mhwirth')

s = requests.Session()
s.auth = CAM_AUTH


def relative_pan(offset):
    payload = { 'rpan' : str(offset)}
    print payload
    code = s.post(CAMERA_URL, data=payload, auth=CAM_AUTH).status_code
    if code == 204:
        return True
    else:
        print 'pan failed'
        return False

def tilt(offset):
    payload = { 'rtilt' : str(offset)}
    code = s.post(CAMERA_URL, data=payload, auth=CAM_AUTH).status_code
    if code == 204:
        return True
    else:
        print 'pan failed'
        return False