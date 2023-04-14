import numpy as np
import cv2 as cv

def analyse(filename,dronecount,coordinateplane):
    img = cv.imread(filename,cv.IMREAD_GRAYSCALE)
    assert img is not None, "file could not be read, check with os.path.exists()"
    ret,thresh = cv.threshold(img,127,255,0)
    contours,hierarchy = cv.findContours(thresh, 1, 2)
    cnt = contours[0]
    length=cv.arcLength(cnt,True)
    epsilon = 0.05*length
    approx = cv.approxPolyDP(cnt,epsilon,True)
    print(length)
    print(approx)