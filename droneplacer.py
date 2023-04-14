import numpy as np
from tkinter import filedialog
import cv2 as cv
import os
import math

def distance(pt1, pt2):
    (x1, y1), (x2, y2) = pt1, pt2
    dist = math.sqrt( (x2 - x1)**2 + (y2 - y1)**2 )
    return dist

def analyse(filename,dronecount,coordinateplane):
    img = cv.imread(filename)
    gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    bi = cv.bilateralFilter(gray, 5, 75, 75)
    # cv.imshow('bi',bi)
    dst = cv.cornerHarris(bi, 2, 3, 0.04)
    mask = np.zeros_like(gray)
    mask[dst>0.01*dst.max()] = 255
    # cv.imshow('mask', mask)
    # cv.waitKey()
    img[dst > 0.01 * dst.max()] = [0, 0, 255]   #--- [0, 0, 255] --> Red ---
    # cv.imshow('dst', img)
    # cv.waitKey()
    coor = np.argwhere(mask)
    coor_list = [l.tolist() for l in list(coor)]
    coor_tuples = [tuple(l) for l in coor_list]
    original=coor_tuples.copy()
    thresh = 100
    prev=0

    while True:
        coor_tuples_copy = coor_tuples
        i = 1    
        for pt1 in coor_tuples:
            for pt2 in coor_tuples[i::1]:
                if(distance(pt1, pt2) < thresh):
                    coor_tuples_copy.remove(pt2)      
            i+=1
        if len(coor_tuples) > dronecount:
            prev=thresh
            thresh*=2
        
        elif len(coor_tuples) < dronecount:
            coor_tuples=original.copy()
            thresh=(prev+thresh)/2
        
        else:
            break
    index=2
    if coordinateplane=="yz":
        index=0
    elif coordinateplane=="xz":
        index=1    
    
    final=[]

    for i in coor_tuples:
        intermediate=list(i)
        intermediate.insert(index,0)
        final.append(intermediate)

    os.remove(filename)
    file_text =filedialog.asksaveasfilename(defaultextension='txt')
    with open(file_text,"w") as f:
        for i in final:
            f.write(str(i[0])+','+str(i[1])+','+str(i[2])+'\n')

analyse("./test10.jpg", 15, "xy")