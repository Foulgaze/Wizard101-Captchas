
# coding: utf-8

# In[ ]:


import cv2
import numpy as np
from matplotlib import pyplot as plt
import os
files = os.listdir(filepath)
numcount = 0
for captcha in files:
    MIN_CONTOUR_AREA = 200
    img = testimg = cv2.imread(//filepath to captcha folder + captcha)
    threshimg = cv2.imread(//filepath to captcha folder + captcha, 0)
    ret,thresh = cv2.threshold(threshimg,100,255,cv2.THRESH_BINARY)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)    
    blured = cv2.blur(gray, (5,5), 0)    
    img_thresh = cv2.adaptiveThreshold(blured, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    #ret,img_thresh = cv2.threshold(img,100,250,cv2.THRESH_BINARY_INV)
    imgContours, Contours, Hierarchy = cv2.findContours(img_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    height, width = img.shape[:2]
    x_points = []
    y_points = []
    imnew = img_thresh
    for contour in Contours:
        if cv2.contourArea(contour) > MIN_CONTOUR_AREA:
            [X, Y, W, H] = cv2.boundingRect(contour)
            if(W > 40):
                #print(W/2)
                x_points.extend([X, (X + round(W/2))])
                y_points.extend([Y, Y+H])
                cv2.rectangle(img_thresh, (X, 247), (X + round(W/2), 0), (0,0,0), -1)
                x_points.extend([(X + round(W/2)), X+W ])
                y_points.extend([Y, Y+H])
                cv2.rectangle(img_thresh, (X + round(W/2), 247), (X + W, 0), (0,0,0), -1)
            else:
                x_points.extend([X, X+W ]) # Adds the x's to a list
                y_points.extend([Y, Y+H]) # Adds the y's to a list
                cv2.rectangle(img_thresh, (X, 247), (X + W, 0), (0,0,0), -1)
    kernel = np.ones((6,2), np.uint8)
    img_thresh = cv2.dilate(img_thresh, kernel)
    #print('allo')
    imgContours, Contours, Hierarchy = cv2.findContours(img_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for contour in Contours:
        if cv2.contourArea(contour) > MIN_CONTOUR_AREA:
            [X, Y, W, H] = cv2.boundingRect(contour)
            if(W > 45):
                x_points.extend([X, (X + round(W/2))])
                y_points.extend([Y, Y+H])
                x_points.extend([(X + round(W/2)), X+W ])
                y_points.extend([Y, Y+H])
            else:
                x_points.extend([X, X+W ]) # Adds the x's to a list
                y_points.extend([Y, Y+H]) # Adds the y's to a list
    sorted_x = sorted(x_points[::2]).copy()
    index_x = x_points.copy()
    for i in range(len(index_x)):
        if i % 2 != 0:
            index_x[i] = 0
    
    for i in range(0,len(x_points),2): # Makes all the rectangles, with the given points from x and y list
        cv2.rectangle(img, (x_points[i], y_points[i]), (x_points[i+1], y_points[i+1]), (0,0,255), 1)
    #print("Contour Length: " + str(counter))
    #print("\n--------------------------------------------------------\n")
    try:
        for i in range(len(sorted_x)):
            numcount += 1
            x_ref = index_x.index(sorted_x[i])
            cv2.rectangle(testimg, (x_points[x_ref], y_points[x_ref]), (x_points[x_ref+1], y_points[x_ref+1]), (0,255,0), 1)
            cv2.imshow("thresh", thresh)
            save_image = thresh[0:47, x_points[x_ref]: x_points[x_ref+1]]
            if captcha[i].isupper():
                file_exten = 'Capital Letters'
            else:
                file_exten = 'Lowercase Letters'
            cv2.imwrite(//path to captcha folder + file_exten + "\\" + captcha[i] + "\\" + "num" + str(numcount) + ".png", save_image)

    except(IndexError):
        print("Index Error")
        pass
print("Program Complete")

