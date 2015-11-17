import numpy as np
import cv2
from matplotlib import pyplot as plt
import math

# Function to apply median filter
# image: noisy input image
# size: size of the filter
def medianFilter(image, size):
	print "Applying MEDIAN FILTER of size = " + str(size)
	image_padded = cv2.copyMakeBorder(image,size/2,size/2,size/2,size/2,cv2.BORDER_REPLICATE)
	for i in range(image.shape[0]):
		for j in range(image.shape[1]):
				image[i][j] = np.median(image_padded[i : i+size, j : j+size])

# Function to apply bilateral Filter
# image : noisy image (pass by refference)
# sigma_d_sq : domain sigma square
# sigma_r_sq : range sigma square
# size : size of filter
def bilateralFilter(image, sigma_d_sq, sigma_r_sq, size = 5):
	print "Applying BILATERAL FILTER of size = " + str(size) + ", domain variance = " \
		+ str(sigma_d_sq) + ", range variance = " + str(sigma_r_sq)
	# w_d are domain weights
	# w_r are range weights
	w_d = np.array([[	m*m + n*n		\
		for m in range(-int(size/2), int(size/2) + 1)] \
		for n in range(-int(size/2), int(size/2) + 1)], dtype=float)
	w_d = np.square(w_d)
	w_d = w_d/(sigma_d_sq)
	w_d = np.exp(-w_d)
	image_padded = cv2.copyMakeBorder(image,size/2,size/2,size/2,size/2,cv2.BORDER_REPLICATE)
	for i in xrange(image.shape[0]):
		for j in xrange(image.shape[1]):
			# Compute range weights
			w_r = np.array(image_padded[i:i+size, j:j+size], dtype=float)
			w_r = np.square(w_r-image_padded[i,j])
			w_r = w_r/(sigma_r_sq)
			w_r = np.exp(-w_r)
			try:
				image[i][j] = np.sum(w_d*w_r*image_padded[i:i+size, j:j+size])/np.sum(w_d*w_r)
			except:
				pass



if __name__ == "__main__":
	# Reading noisy images
	spnoisy = cv2.imread('spnoisy.jpg',0)
	unifnoisy = cv2.imread('unifnoisy.jpg',0)
	spunifnoisy = cv2.imread('spunifnoisy.jpg',0)

	cv2.imshow('Uniform Noise', unifnoisy)
	print "Bilateral Filter to remove uniform noise."
	im_copy_1 = np.array(unifnoisy, copy=True)
	bilateralFilter(im_copy_1, 64, 4*64)
	cv2.imshow('Bilateral Filter', im_copy_1)
	# cv2.imwrite('bilateral_fltr_unif.png', im_copy_1)
	print "Median Filter to remove uniform noise."
	im_copy_2 = np.array(unifnoisy, copy=True)
	medianFilter(im_copy_2, 5)
	cv2.imshow('Median Filter', im_copy_2)
	# cv2.imwrite('median_fltr_unif.png', im_copy_2)
	print "Press any key to continue"
	cv2.waitKey(0)
	cv2.destroyAllWindows()

	print "......."
	print "......."

	cv2.imshow('Salt and Pepper Noise', spnoisy)
	print "Bilateral Filter to remove salt and pepper noise."
	im_copy_1 = np.array(spnoisy, copy=True)
	bilateralFilter(im_copy_1, 1024, 1024, 50)
	cv2.imshow('Bilateral Filter', im_copy_1)
	# cv2.imwrite('bilateral_fltr_sp.png', im_copy_1)
	print "Median Filter to remove salt and peper noise."
	im_copy_2 = np.array(spnoisy, copy=True)
	medianFilter(im_copy_2, 5)
	cv2.imshow('Median Filter', im_copy_2)
	# cv2.imwrite('median_fltr_sp.png', im_copy_2)
	print "Press any key to continue"
	cv2.waitKey(0)
	cv2.destroyAllWindows()

	print "......."
	print "......."

	cv2.imshow('Salt and Pepper and Uniform Noise', spunifnoisy)
	print "Median Filter to remove salt and pepper and uniform noise."
	im_copy_1 = np.array(spnoisy, copy=True)
	medianFilter(im_copy_1, 5)
	print "Bilateral Filter to uniform noise."
	bilateralFilter(im_copy_1, 16, 16)
	cv2.imshow('Median then Bilateral Filter', im_copy_1)
	# cv2.imwrite('med_bilateral_fltr_unifsp.png', im_copy_1)
	im_copy_2 = np.array(spnoisy, copy=True)
	print "Bilateral Filter to uniform and salt and pepper noise."
	bilateralFilter(im_copy_2, 16, 16)
	print "Median Filter to remove salt and pepper noise."
	medianFilter(im_copy_2, 5)
	cv2.imshow('Bilateral then Median Filter', im_copy_2)
	# cv2.imwrite('bilateral_med_fltr_unifsp.png', im_copy_2)
	print "Press any key to continue"
	cv2.waitKey(0)
	cv2.destroyAllWindows()
