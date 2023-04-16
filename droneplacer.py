import numpy as np
from tkinter import filedialog
import cv2 as cv
import math
import matplotlib.pyplot as plt

def distance(pt1, pt2):
    (x1, y1), (x2, y2) = pt1, pt2
    dist = math.sqrt( (x2 - x1)**2 + (y2 - y1)**2 )
    return dist

def analyse(filename,dronecount,coordinateplane):
    img = cv.imread(filename)
    gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    bi = cv.bilateralFilter(gray, 5, 75, 75)
    dst = cv.cornerHarris(bi, 2, 3, 0.04)
    mask = np.zeros_like(gray)
    mask[dst>0.01*dst.max()] = 255
    img[dst > 0.01 * dst.max()] = [0, 0, 255]
    coor = np.argwhere(mask)
    coor_list = [l.tolist() for l in list(coor)]
    coor_tuples = [tuple(l) for l in coor_list]
    thresh = 100
    prev=0

    coor_temp=[]
    print(type(coor_tuples))
    for i in coor_tuples:
        if i[1]==799:
            continue
        else:
            coor_temp.append(i)
    
    original=coor_temp.copy()
    while True:
        coor_tuples_copy = coor_temp
        i = 1    
        for pt1 in coor_temp:
            for pt2 in coor_temp[i::1]:
                if(distance(pt1, pt2) < thresh):
                    coor_tuples_copy.remove(pt2)      
            i+=1
        if len(coor_temp) > dronecount:
            prev=thresh
            thresh*=2
        
        elif len(coor_temp) < dronecount:
            coor_temp=original.copy()
            thresh=(prev+thresh)/2
        
        else:
            break
    index=2
    if coordinateplane in ("yz","yz"):
        index=0
    elif coordinateplane in ("xz","zx"):
        index=1    

    final=[]
    finalx=[]
    for i in coor_temp:
        intr=(i[1],i[0])
        finalx.append(intr)

    zip(*finalx)
    plt.scatter(*zip(*finalx))
    plt.show()
    for i in coor_temp:
        intermediate=list(i)
        intermediate[0],intermediate[1]=intermediate[1],intermediate[0]
        intermediate.insert(index,0)
        final.append(intermediate)

    file_text =filedialog.asksaveasfilename(defaultextension='txt')
    with open(file_text,"w") as f:
        for i in final:
            f.write(str(i[0])+','+str(i[1])+','+str(i[2])+'\n')