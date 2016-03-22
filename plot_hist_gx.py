# plot_histograms.py
# CSC 205 - Spring 2016
#
# B. Bird - 03/10/2016
#
# Edited by:
# Brett Binnersley
# V00776751
# for the purposes of our CSC205 class and assignment (4).

import math
import sys
import png
import itertools
import numpy

# Provided code below
def GetHistogram(image_intensities):
	all_intensities = image_intensities.flatten() #Convert the 2d array into a single long array of pixel values
	hist = numpy.zeros(256)
	for i in all_intensities:
		hist[i] += 1
	return hist

def plot_histogram_array(output_filename, hist):
	hist_field = numpy.ndarray((256,100))
	hist_field[:,:] = 255
	for i in range(256):
		hist_field[i,0:hist[i]*100] = 0
	hist_field = hist_field[:,::-1]
	hist_image = numpy.ndarray((276,120))
	hist_image[:,:] = 255
	hist_image[10:266,9] = 0
	hist_image[10:266,110] = 0
	hist_image[9,10:110] = 0
	hist_image[266,10:110] = 0
	hist_image[10:266,10:110] = hist_field
	write_png_grayscale(output_filename, hist_image.T)

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

# Generate the F(X) histogram for 256 values. [0-255]
def gen_fx_cumulative_histogram(om, u):
    arr = []
    for i in range(256):
        arr.append(0.0)
    arr = numpy.asarray(arr)
    for x in range(256):
        ft = 1.0 / (om * math.sqrt(2.0 * math.pi))
        st = math.exp(-((x-u) * (x-u))/(2.0*om*om))
        val = ft * st
        arr[x] = val
    arr /= arr.max()
    for x in range(256):
        arr[x] = 1 - arr[x]

	cumulative_hist = numpy.zeros(256)
	cumulative_hist[0] = arr[0]
	for i in xrange(1,256):
		cumulative_hist[i] = cumulative_hist[i-1] + arr[i]
    cumulative_hist /= cumulative_hist.max()
    return cumulative_hist

# Function for matching histograms
# Nref will always be 1 in our case
def MatchHistograms(imgHist, width, height, href, nref):
    n = width * height
    r = n / nref
    h = imgHist
    F = []
    for i in range(256):
        F.append(0.0)
    F = numpy.asarray(F)
    i, j, c = 0, 0, 0
    while i < 256:
        if c <= r * href[j]:
            c = c + h[i]
            F[i] = j
            i = i + 1
        else:
            j = j + 1
    for i in range(256):
        F[i] = float(F[i])
    F /= F.max()  # Normalize & return
    return F

# Main
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print >>sys.stderr, "Usage: %s <input image>"
        sys.exit(0)

    # Filenames
    input_filename = sys.argv[1]
    oname = input_filename.rsplit('.',1)[0]
    output_filename = oname + '_gx_matched.png'

    # Read input and generate histograms
    image_intensities = read_image_greyscale(input_filename)
    histogram = GetHistogram(image_intensities)
    hist_fx_cumulative = gen_fx_cumulative_histogram(50.0, 128.0)

    # Find the width & height of the image
    width = len(image_intensities[0])
    height = len(image_intensities)
    m_hist = MatchHistograms(histogram, width, height, hist_fx_cumulative, 1.0)

    # Plot output
    plot_histogram_array(output_filename, m_hist)  # F(x) histogram
