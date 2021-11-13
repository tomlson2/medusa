import cv2 as cv
from hsvfilter import HsvFilter
from windowcapture import WindowCapture
import numpy as np
from vision import Vision
import uuid
import glob
import sys
import os
import time

screen = WindowCapture(area='run_orb')
vision = Vision('Needle\\banana.png')

samples = np.empty((0,100))
responses = []

for img in os.listdir('digits/raw2/'):
    im = cv.imread('digits/raw2/'+img)
    im = vision.apply_hsv_filter(im,HsvFilter(vMin=136,sSub=255))
    gray = cv.cvtColor(im,cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray,(5,5),0)
    mask = cv.adaptiveThreshold(blur,255,1,1,11,2)
    contours, _ = cv.findContours(mask, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    print(type(contours))
    keys = [i for i in range(48,58)]

    for cnt in contours:
        area = cv.contourArea(cnt)
        if 250 > area > 50:
            x, y, w, h = cv.boundingRect(cnt)
            if h>10:
                cv.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)
                im2 = mask[y:y+h,x:x+w]
                roismall = cv.resize(im2,(10,10))
                cv.imshow('norm',im)
                key = cv.waitKey(0)

                if key == 27:  # (escape to quit)
                    sys.exit()
                elif key in keys:
                    responses.append(int(chr(key)))
                    sample = roismall.reshape((1,100))
                    samples = np.append(samples,sample,0)

responses = np.array(responses,np.float32)
responses = responses.reshape((responses.size,1))

np.savetxt('generalsamples.data',samples)
np.savetxt('generalresponses.data',responses)