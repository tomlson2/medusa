import cv2 as cv
import numpy as np

class Ocr:

    '''
    TODO\n
    -finish and identify differences needed (parameters) for number()\n
    -eliminate contours withing each other
    '''

    def __init__(self, samples_file : str, responses_file : str) -> None:
        samples = np.loadtxt(samples_file,np.float32)
        responses = np.loadtxt(responses_file,np.float32)
        responses = responses.reshape((responses.size,1))

        self.model = cv.ml.KNearest_create()
        self.model.train(samples,cv.ml.ROW_SAMPLE,responses)
    


    def number(self, im):
        out = np.zeros(im.shape,np.uint8)
        gray = cv.cvtColor(im,cv.COLOR_BGR2GRAY)
        blur = cv.GaussianBlur(gray,(5,5),0)
        mask = cv.adaptiveThreshold(blur,255,1,1,11,2)
        contours, _ = cv.findContours(mask, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
        num = []
        xlis = []
        for cnt in contours:
            if 350 > cv.contourArea(cnt)>75:
                [x,y,w,h] = cv.boundingRect(cnt)
                if  h>10 or w>10:
                    coord = int(x + (w / 2))
                    xlis.append(coord)
                    roi = mask[y:y+h,x:x+w]
                    roismall = cv.resize(roi,(10,10))
                    roismall = roismall.reshape((1,100))
                    roismall = np.float32(roismall)
                    retval, results, neigh_resp, dists = self.model.findNearest(roismall, k = 1)
                    for digit in results[0]:
                        num.append(int(digit))
        #print(len(num))
        zipped_pairs = zip(num, xlis)
        z = sorted(zipped_pairs, key = lambda x: x[1])
        num = [x[0] for x in z]
        res = ''.join(map(str, num))
        return int(res)

    def text(self, im):
        out = np.zeros(im.shape,np.uint8)
        gray = cv.cvtColor(im,cv.COLOR_BGR2GRAY)
        blur = cv.GaussianBlur(gray,(5,5),0)
        mask = cv.adaptiveThreshold(blur,255,1,1,11,2)
        contours, _ = cv.findContours(mask, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
        print(len(contours))
        num = []
        xlis = []
        ylis = []
        for cnt in contours:
            if 375 > cv.contourArea(cnt)>75:
                [x,y,w,h] = cv.boundingRect(cnt)
                if  h>5 or w>5:
                    coord = int(x + (w / 2))
                    xlis.append(coord)
                    ylis.append(y)
                    roi = mask[y:y+h,x:x+w]
                    roismall = cv.resize(roi,(10,10))
                    roismall = roismall.reshape((1,100))
                    roismall = np.float32(roismall)
                    retval, results, neigh_resp, dists = self.model.findNearest(roismall, k = 1)
                    print(len(results[0]))
                    for digit in results[0]:
                        num.append(chr(digit))
        zipped_pairs = zip(num, xlis)
        z = sorted(zipped_pairs, key = lambda x: x[1])
        num = [x[0] for x in z]
        xlis = [x[1] for x in z]
        diff = np.diff(xlis)
        print(xlis)
        ind = [n for n,i in enumerate(diff) if i>20]
        d = 0
        for i in ind:
            d += 1
            num.insert(i+d," ")
        
        res = ''.join(map(str, num))
        return str(res)

        
        
                