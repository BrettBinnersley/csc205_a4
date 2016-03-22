# edge_sharpen.py
# CSC 205 - Spring 2016
#
# B. Bird - 03/10/2016
#
# Edited by:
# Brett Binnersley
# V00776751
# for the purposes of our CSC205 class and assignment (4).

import copy
import math
import sys
import png
import itertools
import numpy

def write_png_grayscale(output_filename, pixels):
	with open(output_filename, 'wb') as f:
		w = png.Writer(pixels.shape[1], pixels.shape[0], greyscale=True)
		w.write(f, pixels)

def read_image_greyscale(filename):
	r = png.Reader(filename)
	image_data = r.asDirect()
	width,height = image_data[0], image_data[1]
	image_raw = numpy.vstack(itertools.imap(numpy.uint8, image_data[2]))
	if image_data[3]['greyscale']:
		image_bw = image_raw
	else:
		image_pixels = image_raw.reshape((height, width, 3))
		image_bw = numpy.array( image_pixels.mean(axis=2), dtype=numpy.uint8)
	return image_bw

# Simple Guassian blur matrix
def GenGaussianBlur5x5(deviation):
    matrix = []
    stddev = float(deviation)
    for y in range(-2, 3):
        row = []
        if deviation != 0:
            for x in range(-2, 3):
                xysqr = float(x) * float(x) + float(y) * float(y)
                yf = float(y)
                val = math.exp(-(xysqr/(2*stddev*stddev)))
                row.append(val)
        else:
            row.append(0)
            row.append(0)
            if y is 0:
                row.append(1)
            else:
                row.append(0)
            row.append(0)
            row.append(0)
        row = numpy.asarray(row)
        matrix.append(row)
    matrix = numpy.asarray(matrix)

    # Normalize so that the sum of every cell equals 1.
    msum = 0.0
    for y in range(0, 5):
        for x in range(0, 5):
            msum += matrix[x][y]
    for y in range(0, 5):
        for x in range(0, 5):
            matrix[x][y] /= msum
    return matrix

# Apply a gaussian blur to the image
def ApplyBlur(img, gmatrix):
    out = copy.deepcopy(img)  # Clone the image
    width = len(img)
    height = len(img[0])
    for x in range(width):
        for y in range(height):
            color = 0.0
            for mx in range(-2, 3):
                for my in range(-2, 3):
                    # Blur, use smearing
                    ix = min(max(x + mx, 0), width - 1)
                    iy = min(max(y + my, 0), height -1)
                    color += img[ix][iy] * gmatrix[mx + 2][my + 2]  # Proper bounding for matrix
            out[x][y] = min(max(int(color),0),255)  # Bound the pixel
    return out

# Main
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print >>sys.stderr, "Usage: %s <input image> <std deviation>"
        sys.exit(0)

    # Filenames
    input_filename = sys.argv[1]
    oname = input_filename.rsplit('.',1)[0]
    output_filename = oname + '_blurred.png'

    # Read input and generate guassian blur matrix
    image_intensities = read_image_greyscale(input_filename)
    if len(sys.argv) > 2:
        stddev = float(sys.argv[2])
    else:
        stddev = 1.0
    print "Bluring using 5x5 Guassian Matrix, stddev: ", stddev
    blur_matrix = GenGaussianBlur5x5(stddev)

    # Apply the matrix blur
    blurred_image = ApplyBlur(image_intensities, blur_matrix)

    # Plot output
    write_png_grayscale(output_filename, blurred_image)  # F(x) histogram
