import numpy as np
import cv2
import math
from matplotlib import pyplot as plt

def lloydMaxQuantizer(inp_image, level, is_uniform = False):
	# flatten the image
	flat_image = inp_image.flatten()
	t = np.zeros(level+1, dtype=float)
	t[0] = 0
	t[level] = 255
	q = 256/level
	# probibility count or pdf
	pdf = np.zeros(256, dtype=int)
	r = np.zeros(level, dtype=float)

	# Calcuate values for the histogram
	for i in flat_image:
		pdf[i]=pdf[i]+1
	# Mean Square Error
	mserr = 0.0
	lastmserr = -0.1
	# Initialize with uniform quantizer
	for k in range(1,level+1):
		# Apply thresholds
		t[k] = t[k-1]+q
		r[k-1] = (t[k]+t[k-1])/2
	# Iterate
	iter = 0
	if (not is_uniform):
		while (mserr>lastmserr and iter<11):
			lastmserr = mserr
			serr = 0.0
			num = np.zeros(level, dtype=int)
			den = np.zeros(level, dtype=int)
			# Thresholding
			for k in range(1,level):
				t[k] = (r[k-1] + r[k])/2

			for k in range(0,level):
				for i in range(int(math.ceil(t[k])), int(math.ceil(t[k+1]))):
					# print iter, i, int(math.ceil(t[k])), int(math.ceil(t[k+1]))
					num[k] = num[k] + i*pdf[i]
					den[k] = den[k] + pdf[i]

				r[k] = num[k]/den[k]
				r[k]=round(r[k])
				for i in range(int(math.ceil(t[k])), int(math.floor(t[k+1]))):
					serr = serr + (i-r[k])*(i-r[k])*pdf[i]

			mserr = math.sqrt(serr)
			iter = iter + 1

	# Apply quantization
	for i, j in enumerate(flat_image):
		for k in range(1,level+1):
			if j >= t[k-1] and j <= t[k]:
				flat_image[i] = r[k-1]
	mserr = math.sqrt(sum((flat_image-inp_image.ravel())*(flat_image-inp_image.ravel())))
	temp = np.reshape(flat_image, inp_image.shape)
	cv2.imshow('Quantized image (' +('Uniform' if is_uniform else 'Lloyd-Max')+ ')', temp)
	print "Press any key to continue..."
	# cv2.imwrite(('Uniform' if is_uniform else 'Lloyd-Max') + '.png', temp)
	cv2.waitKey(0)
	histogram = cv2.calcHist([flat_image], [0], None, [256], [0, 256])
	plt.plot(histogram)
	plt.xlim([0, 255])

if __name__ == "__main__":
	im = cv2.imread('flower.jpg', 0)
	cv2.imshow('flower', im)
	print "Press any key to continue..."
	cv2.waitKey(0)
	plt.figure()
	plt.title("Image Histogram")
	plt.xlabel("Pixel Bins")
	plt.ylabel("Number of Pixels")
	lloydMaxQuantizer(im, 8)
	lloydMaxQuantizer(im, 8, True)
	plt.show()
