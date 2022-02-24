# test script to trace contours on envelope sample with OpenCV
import cv2
import numpy as np

# read in sample image & convert to grayscale
img = cv2.imread('envelope_sample_redcross.jpg')
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(img_gray, 127, 255, 0)

# find contours
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

# draw contours
cv2.drawContours(img, contours, -1, (0,255,0), 3)

# displaying image with contours drawn on
cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Image', 1080,1920)
cv2.imshow('Image', img)
#cv2.imshow('Image Grayscale', img_gray)

# exit
cv2.waitKey(0)
cv2.destroyAllWindows()