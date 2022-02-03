import cv2 as cv
from hsvfilter import HsvFilter
from windowcapture import PlayerRegion, ScreenRegion, WindowCapture
import numpy as np
from vision import Vision
import uuid
import glob
import time

screen = PlayerRegion()
vision = Vision('Needle\\banana.png')

object_detector = cv.createBackgroundSubtractorMOG2(history=100, varThreshold=60)
#colors = [[148, 154, 55],[137,187,104]]

while True:
    im = screen.get_screenshot()
    mask = object_detector.apply(im)
    contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    stencil = np.zeros(im.shape).astype(im.dtype)
    cv.fillPoly(stencil, contours, [255, 255, 255])
    stenciled_im = cv.bitwise_and(im, stencil)

    for cnt in contours:
        area = cv.contourArea(cnt)
        if 1000 > area > 800:
            #cv.drawContours(im,[cnt],-1,(0,255,0))
            x, y, w, h = cv.boundingRect(cnt)
            cv.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)
            im2 = im[y:y+h,x:x+w]
        
    cv.imshow('match',im)


    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break