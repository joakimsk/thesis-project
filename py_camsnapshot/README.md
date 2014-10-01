py_camsnapshot.py
===========
initial revision

py_camsnapshot.py will iterate through cams.csv and grab a snapshot of each camera.
Requires MJPEG access to CCTV-camera and correct connection string.

cams.csv:  # Description; Target folder name; Connection string
"House camera";cam1;http://ptz:ptz@129.241.154.82/mjpg/video.mjpg
"Dog camera";cam2;http://ptz:ptz@129.241.154.81/mjpg/video.mjpg

log.txt: # Date and time of capture;Target folder name; Was picture captured?
2014-10-01 20:04:12.285000;cam1;True
2014-10-01 20:04:12.285000;cam2;False
2014-10-01 20:04:56.731000;cam1;True
2014-10-01 20:04:56.731000;cam2;True

Dependencies
------------
- Python 2.7
- OpenCV
- Numpy


Tested on Windows 7
By Joakim Skjefstad for Project Thesis NTNU 2014
skjefstad.joakim@gmail.com