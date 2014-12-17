#!/usr/bin/env python
import cv2
import sys
import numpy as np
import urllib
import random

import jsg
import ptz

# Glyph tracking, combining CCTV and Webcam into one solution.
# Vision algorithm is implemented in the imported jsg module.
# Feedback to camera is implemented in the imported ptz module.
#
# Written by Joakim Skjefstad (skjefstad.joakim@gmail.com) Autumn 2014

print "Glyph-tracking proof of concept. Use ESC to exit program."
print "Written by Joakim Skjefstad (skjefstad.joakim@gmail.com) Autumn 2014"
print "Preproject for master thesis. M.Sc in Technical Cybernetics at NTNU, Norway."
print "Preproject for master thesis. M.Sc in Technical Cybernetics at NTNU, Norway."

# Target specification, allows multiple glyphs to be tracked at once, however this increases processing time per frame
machine1 = np.matrix('1 1 1 1 1; 1 0 1 0 1; 1 0 1 1 1; 1 0 0 0 1; 1 1 1 1 1')
#machine2 = np.matrix('1 1 1 1 1; 1 0 0 0 1; 1 1 0 1 1; 1 1 0 1 1; 1 1 1 1 1')

target_list = []
target_list.append(machine1)
#target_list.append(machine2)

collage = np.zeros((50,300, 3), np.uint8)

# Hard-coded CCTV Camera for PTZ-module. Change this when needed.
Camera = ptz.AxisCamera('129.241.154.82', '/axis-cgi/com/', 'root', 'JegLikerKanelSnurrer')

def init_capture_device(is_cctv):
    if (is_cctv == True):
        print "Using CCTV MJPEG stream"
        # Hard-coded CCTV Camera MJPEG stream. Change this when needed.
        stream=urllib.urlopen('http://ptz:ptz@129.241.154.82/mjpg/video.mjpg')
        return stream
    else:
        print "Using webcam stream"
        cap = cv2.VideoCapture(0)
        return cap

def grab_frame(capture_device, is_cctv):
    if is_cctv == False:
        ret, img = capture_device.read()
        return img
    else:
        bytes=''
        while True:
            bytes+=capture_device.read(1024)
            a = bytes.find('\xff\xd8')
            if a !=-1:
                b = bytes.find('\xff\xd9', a)
                if a!=-1 and b!=-1:
                    jpg = bytes[a:b+2]
                    bytes= bytes[b+2:]
                    i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.CV_LOAD_IMAGE_COLOR)
                    return i

capture_device = init_capture_device(False) # SET TO TRUE FOR CCTV STREAM
while True:
    for frame in range(0,5):
        source = grab_frame(capture_device, False) # SET TO TRUE FOR CCTV STREAM
    
    temp_img = jsg.preprocess(source)

    potential_glyphs = jsg.find_potential_glyphs(temp_img, 100.0)
    for glyph in potential_glyphs:
        glyph.compute_glyph(source)
        if jsg.compare_glyphs(glyph.glyph_matrix,target_list):
            print "Hit ", glyph.nr
            #print glyph.glyph_matrix
            cv2.drawContours(source,[glyph.approx_poly],0,(0,255,0),4)
            cv2.circle(source,(glyph.cx,glyph.cy),5,(255,0,255),-1)
            cv2.putText(source,str(glyph.nr), (glyph.cx,glyph.cy), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,0), 2)
            delta_array = jsg.delta_to_center(source, glyph)
            for item in delta_array:
                print "delta",item
                print "PANNING",-0.01*delta_array[0]
                
                # UNCOMMENT TO CONTROL PTZ
                #Camera.relative_pan(-0.005*delta_array[0])
                #Camera.tilt(-0.005*delta_array[1])

            print glyph.nr
            #break
            small = cv2.resize(glyph.img_roi, (50,50), interpolation =cv2.INTER_AREA)
            cv2.imshow('Roi',glyph.img_roi)
            cv2.imshow('Otsu',glyph.img_roi_otsu)
            collage[0:50,(0+(50*glyph.nr)):(50+(50*glyph.nr))] = small
        #else:
            #print "no hit"
            #cv2.drawContours(source,[glyph.contour],0,(0,0,255),4)
    cv2.imshow('Collage',collage)
    cv2.imshow('Source',source)
    
    if cv2.waitKey(1) == 27:
        exit(0)
