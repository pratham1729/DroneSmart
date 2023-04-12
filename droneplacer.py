import numpy as np
import cv2 as cv
img = cv.imread('./test.jpg')
img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
assert img is not None, "file could not be read, check with os.path.exists()"
print(img_gray)
ret,thresh = cv.threshold(img_gray,127,255,0)
contours,hierarchy = cv.findContours(thresh, 1, 2)
cnt = contours[0]
# M = cv.moments(cnt)
# print(M)
length=cv.arcLength(cnt,True)
epsilon = 0.05*length
approx = cv.approxPolyDP(cnt,epsilon,True)
print(length)
print(approx)