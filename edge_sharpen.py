# guassian_blur.py
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
def GenHL():
    matrix = []
    row = numpy.asarray([0, 1, 0])
    matrix.append(row)
    row = numpy.asarray([1, -4, 1])
    matrix.append(row)
    row = numpy.asarray([0, 1, 0])
    matrix.append(row)
    matrix = numpy.asarray(matrix)

    # Normalize so that the sum of every cell equals 1.
    # msum = 0.0
    # for y in range(0, 3):
    #     for x in range(0, 3):
    #         msum += matrix[x][y]
    # for y in range(0, 3):
    #     for x in range(0, 3):
    #         matrix[x][y] /= msum
    return matrix

# Apply a gaussian blur to the image
def ApplyHL(img, gmatrix, weight):
    hlcon_I = copy.deepcopy(img)  # Clone the image
    width = len(img)
    height = len(img[0])
    for x in range(width):
        for y in range(height):
            color = 0.0
            for mx in range(-1, 2):
                for my in range(-1, 2):
                    # Blur, use smearing
                    ix = min(max(x + mx, 0), width - 1)
                    iy = min(max(y + my, 0), height -1)
                    color += img[ix][iy] * gmatrix[mx + 1][my + 1]  # Proper bounding for matrix
            hlcon_I[x][y] = min(max(int(color),0),255)  # Bound the pixel

    # We have HL * I (hlcon_I). Multiply everything by weight
    w = float(weight)
    for x in range(width):
        for y in range(height):
            if float(hlcon_I[x][y]) * w > 255.0:
                hlcon_I[x][y] = 255
            elif float(hlcon_I[x][y]) * w < 0.0:
                hlcon_I[x][y] = 0
            else:
                hlcon_I[x][y] *= w

    out = copy.deepcopy(img)  # Clone the image (again)
    for x in range(width):
        for y in range(height):
            out[x][y] = int(out[x][y])
            if out[x][y] > hlcon_I[x][y]:
                out[x][y] = max(min(out[x][y] - hlcon_I[x][y], 255), 0)
            else:
                out[x][y] = 0
    return out

# Main
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print >>sys.stderr, "Usage: %s <input image> <weight>"
        sys.exit(0)

    # Filenames
    input_filename = sys.argv[1]
    oname = input_filename.rsplit('.',1)[0]
    output_filename = oname + '_sharpen.png'

    # Read input and generate guassian blur matrix
    image_intensities = read_image_greyscale(input_filename)
    if len(sys.argv) > 2:
        weight = float(sys.argv[2])
    else:
        weight = 10.0
    print "Sharpening Edges with weight: ", weight
    hl = GenHL()

    # Apply the matrix blur
    blurred_image = ApplyHL(image_intensities, hl, weight)

    # Plot output
    write_png_grayscale(output_filename, blurred_image)  # F(x) histogram
