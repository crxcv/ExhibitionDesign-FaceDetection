
# convert color depth:
# https://stackoverflow.com/questions/33299374/opencv-convert-cv-8u-to-cv-64f
#
# 8-bit unsigned integer        (uchar)     uint8       CV_8U   0 to 255
# 8-bit signed integer          (schar)     int16       CV_8S   -32768 to 32767
# 16-bit unsigned integer       (ushort)    uint16      CV_16U  -32768 to 32767
# 16-bit signed integer         (short)     int16       CV_16S  0 to 65535
# 32-bit signed integer         (int)       int32       CV_32S  0 to 232 - 1
# 32-bit floating-point number  (float)     float       CV_32F  -1 to 1 or 0 to 1
# 64-bit floating-point number  (double)    double      CV_64F
# a tuple of several elements where all elements have the same type (one of the above). An array whose elements are such tuples, are called multi-channel arrays, as opposite to the single-channel arrays, whose elements are scalar values. The maximum possible number of channels is defined by the CV_CN_MAX constant, which is currently set to 512.
# For these basic types, the following enumeration is applied:
#
# enum { CV_8U=0, CV_8S=1, CV_16U=2, CV_16S=3, CV_32S=4, CV_32F=5, CV_64F=6 };
# imread: uint8

# sobel:
# src.depth() = CV_8U, ddepth = -1/CV_16S/CV_32F/CV_64F
# src.depth() = CV_16U/CV_16S, ddepth = -1/CV_32F/CV_64F
# src.depth() = CV_32F, ddepth = -1/CV_32F/CV_64F
# src.depth() = CV_64F, ddepth = -1/CV_64F


# supported by kivy:
# bufferfmt can be:
#
# ‘ubyte’, ‘byte’, ‘ushort’, uint’,  ‘int’, ‘short’, or ‘float’.
# The default value and the most commonly used is ‘ubyte’


min = np.min(img)
img = img-min #to have only positive values
max=np.max(img)
div = max / float(255) #calculate the normalize divisor
sobelx_8u = np.uint8(np.round(sobelx_64f / div))


# skimage conversions:
# img_as_float	Convert to 64-bit floating point.
# img_as_ubyte	Convert to 8-bit uint.
# img_as_uint	Convert to 16-bit uint.
# img_as_int	Convert to 16-bit int.


from skimage import img_as_float
image = np.arange(0, 50, 10, dtype=np.uint8)
print(image.astype(np.float)) # These float values are out of range.
# [  0.  10.  20.  30.  40.]
print(img_as_float(image))
# [ 0.          0.03921569  0.07843137  0.11764706  0.15686275]

from skimage import img_as_float
image = np.arange(0, 50, 10, dtype=np.uint8)
print(image.astype(np.float)) # These float values are out of range.
# [  0.  10.  20.  30.  40.]
print(img_as_float(image))
# [ 0.          0.03921569  0.07843137  0.11764706  0.15686275]


# Warnings can be locally ignored with a context manager:

import warnings
image = np.array([0, 0.5, 1], dtype=float)
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    img_as_ubyte(image)
# array([  0, 128, 255], dtype=uint8)
