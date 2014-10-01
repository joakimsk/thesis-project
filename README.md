the_project
===========

Implementation for the project thesis, preliminary work before the master thesis. Mashup of various technologies.

Final purpose is to have a suite which can track and follow glyphs using PTZ camera coupled with computer vision.

Mainly developed on Windows 7

- py_camsnapshot: Program to capture snapshots of cameras
- py_camstream: CCTV camera streaming implementation
- py_glyph: Glyph recognition implementation
- py_camglyph: Combination of CCTV Camera and Glyph Recognition, realtime
- cpp_gsoap: PTZ ONVIF-S Implementation C++


# Primary effort
- Implement proof-of-concept glyph tracking CCTV camera in Python

## Secondary effort
- Implement proof-of-concept in C++
- Increase robustness and noise removal through super-resolution

Screenshot
------------
py_camglyph.py running off an AXIS CCTV Camera video stream.
![ScreenShot](screenshot.jpg)
Dependencies
------------
- C++ Compiler (VS 2013 Express or gcc)
- Python 2.7
- gSOAP
- ONVIF-S WSDL
- OpenSSL
- OpenCV
- Numpy