#!/usr/bin/env python
import requests

CAMERA_URL = "http://192.168.0.108/axis-cgi/com/ptz.cgi"
CAM_AUTH = requests.auth.HTTPDigestAuth('root', 'mhwirth')

payload = { 'rpan':'10' }

response = requests.post(CAMERA_URL, data=payload, auth=CAM_AUTH)
print response