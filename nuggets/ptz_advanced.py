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
        
def brightness(offset):
    payload = { 'brightness' : str(offset)}
    code = s.post(CAMERA_URL, data=payload, auth=CAM_AUTH).status_code
    if code == 204:
        return True
    else:
        print 'brightness failed'
        return False
        
def focus(offset):
    payload = { 'focus' : str(offset)}
    code = s.post(CAMERA_URL, data=payload, auth=CAM_AUTH).status_code
    if code == 204:
        return True
    else:
        print 'focus failed'
        return False
        
def iris(offset):
    payload = { 'iris' : str(offset)}
    code = s.post(CAMERA_URL, data=payload, auth=CAM_AUTH).status_code
    if code == 204:
        return True
    else:
        print 'iris failed'
        return False