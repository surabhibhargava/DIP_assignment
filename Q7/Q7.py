import numpy as np
import cv2
import itertools
import math

def detectHarrisCorners(image, window_size, block_size, alpha = 0.04):
	# preprocess the input image
	image = cv2.GaussianBlur(image,(5,5),0)

	gradient_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=block_size)
	gradient_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=block_size)
	# print gradient_x[gradient_x.nonzero()]
	# print gradient_y[gradient_y.nonzero()]
	cv2.imshow('Gradient along X', gradient_x)
	# cv2.imwrite('gradien_along_x.png', gradient_x)
	cv2.imshow('Gradient along Y', gradient_y)
	# cv2.imwrite('gradien_along_y.png', gradient_y)
	eigs = cv2.cornerEigenValsAndVecs(image, window_size, block_size)
	eigs = eigs[:,:,0:2]

	lambda_1 = eigs[:,:,0]
	lambda_2 = eigs[:,:,1]

	return lambda_1*lambda_2 - alpha*(lambda_1+lambda_2)**2

def nonMaximalSupression(src, win_len, G):
	dst = np.zeros(src.shape, dtype=bool)
	size = 2*win_len
	src_padded = cv2.copyMakeBorder(src, win_len, win_len, win_len, win_len, cv2.BORDER_REPLICATE)
	for i,j in itertools.product(xrange(src.shape[0]), xrange(src.shape[1])):
		if 	G[i,j]:
			if src[i,j] == np.max(src_padded[i:i+size, j:j+size]):
				dst[i,j] = True
			else:
				dst[i,j] = False
	return dst



if __name__ == "__main__":
	image = cv2.imread('IITG.jpg', 1)
	image_bw = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	candidates = detectHarrisCorners(image_bw, 2, 3)
	R = cv2.dilate(candidates, None)

	G = R > 0.01*R.max()
	temp = np.full(image_bw.shape, R.min())
	temp[G] = R[G]

	dst = nonMaximalSupression(temp, 3, G)
	image[dst]=[0,0,255]

	cv2.imshow('Corners superimposed on image', image)
	# cv2.imwrite('corners_superimposed.png', image)
	print 'Press any key to continue...'
	cv2.waitKey(0)
