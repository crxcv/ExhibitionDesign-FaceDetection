from __future__ import print_function
import cv2 as cv
import numpy as np
import argparse
morph_size = 0
max_operator = 4
max_elem = 2
max_kernel_size = 21
title_trackbar_operator_type = 'Operator:\n 0: Opening - 1: Closing  \n 2: Gradient - 3: Top Hat \n 4: Black Hat'
title_trackbar_element_type = 'Element:\n 0: Rect - 1: Cross - 2: Ellipse'
title_trackbar_kernel_size = 'Kernel size:\n 2n + 1'
title_window = 'Morphology Transformations Demo'
morph_op_dic = {0: cv.MORPH_OPEN, 1: cv.MORPH_CLOSE, 2: cv.MORPH_GRADIENT, 3: cv.MORPH_TOPHAT, 4: cv.MORPH_BLACKHAT}


def morphology_operations(val):
    morph_operator = cv.getTrackbarPos(title_trackbar_operator_type, title_window)
    morph_size = cv.getTrackbarPos(title_trackbar_kernel_size, title_window)
    morph_elem = 0
    val_type = cv.getTrackbarPos(title_trackbar_element_type, title_window)
    if val_type == 0:
        morph_elem = cv.MORPH_RECT
    elif val_type == 1:
        morph_elem = cv.MORPH_CROSS
    elif val_type == 2:
        morph_elem = cv.MORPH_ELLIPSE
    element = cv.getStructuringElement(morph_elem, (2*morph_size + 1, 2*morph_size+1), (morph_size, morph_size))
    operation = morph_op_dic[morph_operator]
    dst = cv.morphologyEx(img, operation, element)
    cv.imshow(title_window, dst)


img = cv.imread('images/orig.JPEG')
img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
img = cv.resize(img, (0,0), fx=0.7, fy=0.7)


kernel = np.ones((5, 5), np.uint8)
erosion = cv.erode(img, kernel, iterations=1)
dilation = cv.dilate(img,kernel,iterations = 1)

cv.namedWindow("erosion")
cv.namedWindow("dilation")
cv.imshow("erosion", erosion)
cv.imshow("dilation", dilation)

cv.namedWindow(title_window)
cv.createTrackbar(title_trackbar_operator_type, title_window , 0, max_operator, morphology_operations)
cv.createTrackbar(title_trackbar_element_type, title_window , 0, max_elem, morphology_operations)
cv.createTrackbar(title_trackbar_kernel_size, title_window , 0, max_kernel_size, morphology_operations)
morphology_operations(0)
cv.waitKey()
