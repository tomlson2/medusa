import cv2 as cv
import numpy as np

class Numbers():

    def __init__(self) -> None:
        samples = np.loadtxt('generalsamples.data',np.float32)
        responses = np.loadtxt('generalresponses.data',np.float32)
        responses = responses.reshape((responses.size,1))

        self.model = cv.ml.KNearest_create()
        self.model.train(samples,cv.ml.ROW_SAMPLE,responses)


    def number(self, im):
        out = np.zeros(im.shape,np.uint8)
        gray = cv.cvtColor(im,cv.COLOR_BGR2GRAY)
        blur = cv.GaussianBlur(gray,(5,5),0)
        mask = cv.adaptiveThreshold(blur,255,1,1,11,2)
        contours, _ = cv.findContours(mask, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            if 250 > cv.contourArea(cnt)>50:
                [x,y,w,h] = cv.boundingRect(cnt)
                if  h>15:
                    roi = mask[y:y+h,x:x+w]
                    roismall = cv.resize(roi,(10,10))
                    roismall = roismall.reshape((1,100))
                    roismall = np.float32(roismall)
                    retval, results, neigh_resp, dists = self.model.findNearest(roismall, k = 1)
                    num = str(int((results[0][0])))
                    print(num)
                