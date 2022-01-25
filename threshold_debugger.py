import cv2 as cv
from hsvfilter import HsvFilter
from windowcapture import WindowCapture, CustomRegion
from vision import Vision

wincap = CustomRegion(867,345,148,180)

needle = 'Needle\\motherlode\\right_vein.png'

vision = Vision(needle)

vision.init_control_gui()

cv.namedWindow("Threshold", cv.WINDOW_NORMAL)

def nothing(position):
    pass

cv.createTrackbar('Match Threshold', 'Threshold', 85, 100, nothing)


while True:
    threshold = (cv.getTrackbarPos('Match Threshold', "Threshold") * .01)
    hsv_filter1 = vision.get_hsv_filter_from_controls()
    edited_needle = Vision(needle, hsv_filter=hsv_filter1)
    screenshot = vision.apply_hsv_filter(wincap.get_screenshot(),hsv_filter=hsv_filter1)
    rectangles = edited_needle.find(screenshot, threshold=threshold)
    edited_image = vision.draw_rectangles(screenshot,rectangles=rectangles)
    edited_image = cv.putText(edited_image,"Threshold = " + str(round(threshold,4)),(50,40),cv.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
    edited_image = cv.putText(edited_image,"Matches = " + str(len(rectangles)),(50,85),cv.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)                
    cv.imshow('matches', edited_image)
    cv.imshow('needle', edited_needle.get_image())
        
    if cv.waitKey(1) == ord('q'):
        cv.imwrite("needle2.png", edited_needle.get_image())
        cv.destroyAllWindows()
        break 

print('Done.')