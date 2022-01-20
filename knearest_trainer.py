import cv2 as cv
from hsvfilter import HsvFilter
from windowcapture import WindowCapture
import numpy as np
from vision import Vision
import sys
import os


vision = Vision('Needle\\banana.png')

samples = np.empty((0,100))
responses = []

# samples = np.loadtxt('bold12lowersamples.data')
# responses = np.loadtxt('bold12lowerresponses.data')
# responses = np.ndarray.tolist(responses)

for img in os.listdir('fonts/'):
    im = cv.imread('fonts/'+img)
    im = vision.apply_hsv_filter(im,HsvFilter(vMin=136,sSub=255))
    gray = cv.cvtColor(im,cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray,(5,5),0)
    mask = cv.adaptiveThreshold(blur,255,1,1,11,2)
    contours, _ = cv.findContours(mask, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    print(len(contours))
    keys = [i for i in range(28,122)]

    for cnt in contours:
        area = cv.contourArea(cnt)
        if 375 > area > 75:
            x, y, w, h = cv.boundingRect(cnt)
            if h>5 or w>5:
                im = vision.apply_hsv_filter(im,HsvFilter(vMin=136,sSub=255))
                cv.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)
                im2 = mask[y:y+h,x:x+w]
                roismall = cv.resize(im2,(10,10))
                cv.imshow('norm',im)
                key = cv.waitKey(0)

                if key == 27:  # (escape to quit)
                    sys.exit()
                elif key in keys:
                    responses.append(key)
                    print(key)
                    sample = roismall.reshape((1,100))
                    samples = np.append(samples,sample,0)
                cv.rectangle(im, (x, y), (x + w, y + h), (255, 0, 0), 2)

responses = np.array(responses,str)
responses = responses.reshape((responses.size,1))

np.savetxt('samples/test.data',samples)
np.savetxt('responses/test.data',responses, fmt='%s')