#!/usr/bin/env python
import cv2
import sys
import numpy as np
import urllib
import random

import jsg

target_glyph_matrix = np.matrix('1 1 1 1 1; 1 0 0 1 1; 1 1 0 0 1; 1 1 0 1 1; 1 1 1 1 1')

collage = np.zeros((50,300, 3), np.uint8)

def init_capture_device(is_cctv):
	if (is_cctv == True):
		print "Using CCTV MJPEG stream"
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
			b = bytes.find('\xff\xd9')
			if a!=-1 and b!=-1:
				jpg = bytes[a:b+2]
				bytes= bytes[b+2:]
				img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.CV_LOAD_IMAGE_COLOR)
				return img

capture_device = init_capture_device(False)
while True:	
	source = grab_frame(capture_device, False)
	temp_img = jsg.preprocess(source)

	potential_glyphs = jsg.find_potential_glyphs(temp_img, 100.0)

	for glyph in potential_glyphs:
		glyph.compute_glyph(source)
		#cv2.imshow(str(glyph.nr),glyph.img_roi_otsu)
		if jsg.compare_glyphs(glyph.glyph_matrix,target_glyph_matrix):
			print glyph.glyph_matrix
			cv2.drawContours(source,[glyph.approx_poly],0,(0,255,0),4)
			cv2.circle(source,(glyph.cx,glyph.cy),5,(255,0,255),-1)
			cv2.putText(source,str(glyph.nr), (glyph.cx,glyph.cy), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,0), 2)
			jsg.delta_to_center(source, glyph)
			print glyph.nr
			small = cv2.resize(glyph.img_roi, (50,50), interpolation =cv2.INTER_AREA)
			collage[0:50,(0+(50*glyph.nr)):(50+(50*glyph.nr))] = small
			#collage[(glyph.nr*50)+50:(glyph.nr*50)+50,(glyph.nr*50)+50:(glyph.nr*50)+50] = 
		else:
			cv2.drawContours(source,[glyph.contour],0,(0,0,255),4)
	cv2.imshow('Collage',collage)
	
	cv2.imshow('Source',source)
	if cv2.waitKey(1) ==27:
		exit(0)