from sqlalchemy import null
from windowcapture import CustomRegion, ScreenRegion
import cv2 as cv
from vision import Vision
from hsvfilter import HsvFilter
from scripting import Script
import time


region = ScreenRegion()

# Vision().init_control_gui()

window_name = 'window'

def init_trackbars():
    cv.namedWindow(window_name, cv.WINDOW_NORMAL)
    cv.createTrackbar('Match Threshold', window_name, 85, 100, null)
    cv.createTrackbar('Blur', window_name, 10, 100, null)
    cv.createTrackbar('Edge Detection', window_name, 1, 1, null)
    cv.createTrackbar('Edge Thresh1', window_name, 0, 200, null)
    cv.createTrackbar('Edge Thresh2', window_name, 0, 200, null)

def testing():
    while True:
        im = region.get_screenshot()
        hsv_img = Vision().apply_hsv_filter(im, HsvFilter(vMax=50))
        gray_im = cv.cvtColor(hsv_img, cv.COLOR_BGR2GRAY)
        canny_im = cv.Canny(gray_im, 1, 1)
        blurred_im = cv.GaussianBlur(canny_im, (9, 9), cv.BORDER_DEFAULT)
        contours, _ = cv.findContours(blurred_im, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            area = cv.contourArea(cnt)
            if area > 50:
                x, y, w, h = cv.boundingRect(cnt)
                cv.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # 
        cv.imshow('canny', im)

            
        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            break 


script = Script()

while True:
    time.sleep(5)
    script.print_time()