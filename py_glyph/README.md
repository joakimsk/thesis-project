py_glyph.py
===========
initial revision

py_glyph.py will load a single image and try to identify the glyphs found.
It is then compared to the fixed glyph from checkIfValidGlyph().

Not rotation invariant at this current stage.

validGlyph = np.matrix('
1 1 1 1 1;
1 0 0 1 1;
1 1 0 0 1;
1 1 0 1 1;
1 1 1 1 1
')

General process implemented
------------
1: Grayscale
2: Blur gaussian 5x5
3: Canny edge detection
4: Contour finding, minimum areal to eliminate tiny shit
5: Find aproximations with exactly 4 points from contour, coloured red
6: Perspective transform into 250x250 pixler ROI
7: Binary Otsu tresholding on each ROI from #6.
8: Segmenting 5x5 matrix, using "fill" where fill = size - black_pixels and fill > 0.5 = 1 (True)
9: Comparing 5x5 matrix to valid glyph 5x5 matrix, one-to-one (NOT rotation independent for now)

Dependencies
------------
- Python 2.7
- OpenCV
- Numpy

Tested on Windows 7
By Joakim Skjefstad for Project Thesis NTNU 2014
skjefstad.joakim@gmail.com
