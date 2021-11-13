import cv2 as cv
from hsvfilter import HsvFilter
from windowcapture import WindowCapture
import numpy as np
from vision import Vision
import uuid
import glob

screen = WindowCapture(area='run_orb')
vision = Vision('Needle\\banana.png')

object_detector = cv.createBackgroundSubtractorMOG2(history=100, varThreshold=40)
#colors = [[148, 154, 55],[137,187,104]]

while True:
    im = screen.get_screenshot()
    im = vision.apply_hsv_filter(im,HsvFilter(vMin=136,sSub=255))
    mask = object_detector.apply(im)
    contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    stencil = np.zeros(im.shape).astype(im.dtype)
    cv.fillPoly(stencil, contours, [255, 255, 255])
    stenciled_im = cv.bitwise_and(im, stencil)

    for cnt in contours:
        area = cv.contourArea(cnt)
        if area > 50:
            #cv.drawContours(im,[cnt],-1,(0,255,0))
            x, y, w, h = cv.boundingRect(cnt)
            #cv.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)
            im2 = im[y:y+h,x:x+w]
            cv.imwrite("digits//"+str(uuid.uuid4())+".png",im2)
            #         break
            #     elif cv.waitKey(1) == ord('2'):
            #         #cv.imwrite("failed//"+str(uuid.uuid4())+".png",im2)
            #         break
            
        
    cv.imshow('match',im)

    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break