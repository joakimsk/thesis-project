#!/usr/bin/env python
from __future__ import division
import cv2
import sys
import logging
import numpy as np
"""Module: jsg
Implements glyph finding using OpenCV.
Written by Joakim Skjefstad
"""
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

class PotentialGlyph:
	def __init__(self, nr, contour, approx_poly, area, moment):
		logging.debug('instance of PotentialGlyph created')
		self.nr = nr
		self.contour = contour
		self.approx_poly = approx_poly
		self.area = area
		self.moment = moment
		self.cx = int(self.moment['m10']/self.moment['m00']) # cx = M10/M00
		self.cy = int(self.moment['m01']/self.moment['m00']) # cy = M01/M00
		self.img_roi = np.array([ [0,0],[249,0],[249,249],[0,249] ],np.float32)
		self.img_roi_otsu = np.array([ [0,0],[249,0],[249,249],[0,249] ],np.float32)
		self.glyph_matrix = np.matrix('-1 -1 -1 -1 -1;-1 -1 -1 -1 -1;-1 -1 -1 -1 -1;-1 -1 -1 -1 -1;-1 -1 -1 -1 -1')

	def __str__(self):
		return "JoakimGlyph %s, area=%s" % (self.nr, self.area) 

	def compute_glyph(self, original_img):
		self.img_roi = self._crop_transform_roi(original_img, self.approx_poly)
		self.img_roi_otsu = self._otsu_roi(self.img_roi)
		self.glyph_matrix = self._identify_glyph_matrix(self.img_roi_otsu)

	def _crop_transform_roi(self, original_img, approx_poly):
		rectified_approx_poly = rectify(approx_poly)
		transform = cv2.getPerspectiveTransform(rectified_approx_poly,self.img_roi)
		transformed_roi = cv2.warpPerspective(original_img, transform, (250,250))
		return transformed_roi

	def _otsu_roi(self, img_roi):
		# OTSU details http://docs.opencv.org/trunk/doc/py_tutorials/py_imgproc/py_thresholding/py_thresholding.html
		roi_gray = cv2.cvtColor(img_roi, cv2.COLOR_BGR2GRAY)
		#roi_blur = cv2.GaussianBlur(roi_gray,(5,5),0)
		ret, img_roi_otsu = cv2.threshold(roi_gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
		return img_roi_otsu

	def _identify_glyph_matrix(self, img_roi_otsu):
		height, width = img_roi_otsu.shape
		glyph_matrix = np.matrix('-1 -1 -1 -1 -1;-1 -1 -1 -1 -1;-1 -1 -1 -1 -1;-1 -1 -1 -1 -1;-1 -1 -1 -1 -1')
		x_roll = int(width/50)
		y_roll = int(height/50)
		for numx in range(0,x_roll):
			for numy in range(0, y_roll):
				if check_region_fill(img_roi_otsu[numx*50:numx*50+50,numy*50:numy*50+50]) > 0.5:
					glyph_matrix[numx, numy] = 1
				else:
					glyph_matrix[numx, numy] = 0
		return glyph_matrix


def check_region_fill(otsu_roi_part):
	height, width = otsu_roi_part.shape
	size = width * height
	fill = size - cv2.countNonZero(otsu_roi_part)
	#print width, height, size, fill
	# NB: Floating return value REQUIRES from __future__ import division
	return (fill/size)

if __name__ == "__main__":
	print "This is a module, please load as such."

def __init__():
	print "loaded jsg module."

def rectify(h):
	# http://opencvpython.blogspot.no/2012/06/sudoku-solver-part-3.html
    h = h.reshape((4,2))
    hnew = np.zeros((4,2),dtype = np.float32)

    add = h.sum(1)
    hnew[0] = h[np.argmin(add)]
    hnew[2] = h[np.argmax(add)]

    diff = np.diff(h,axis = 1)
    hnew[1] = h[np.argmin(diff)]
    hnew[3] = h[np.argmax(diff)]
    return hnew

def find_potential_glyphs(img, minimum_area):
	contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	potential_glyphs = []
	nr = 0
	for contour in contours:
		approx_poly = cv2.approxPolyDP(contour, 0.01*cv2.arcLength(contour, True), True)
		if len(approx_poly)==4:
			area = cv2.contourArea(contour)
			if area >= minimum_area:
				moment = cv2.moments(contour)
				logging.debug('recognize_glyphs - Contour - IsQuad')
				potential_glyphs.append(PotentialGlyph(nr, contour, approx_poly, area, moment))
				nr += 1
	return potential_glyphs

def preprocess(img):
	height, width, depth = img.shape
	img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	#img_blur = cv2.GaussianBlur(img_gray,(3,3),0)
	img_edge = cv2.Canny(img_gray, 100, 200)
	return img_edge

def compare_glyphs(glyph_matrix, target_glyph_matrix):
	for i in range(4):
		if (target_glyph_matrix==glyph_matrix).all():
			return True
		glyph_matrix = np.rot90(glyph_matrix)
	return False

def delta_to_center(source_img, glyph):
	height, width, depth = source_img.shape
	center_x = width/2
	center_y = height/2
	delta_x = center_x - glyph.cx
	delta_y = glyph.cy - center_y  
	print delta_x,delta_y