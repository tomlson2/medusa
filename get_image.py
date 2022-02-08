from windowcapture import ScreenRegion
import cv2 as cv
import uuid
import time
screen = ScreenRegion()
count = 251

while True:
    

    im = screen.get_screenshot()
    cv.imwrite("mf_data//"+str(count)+".png", im)
    time.sleep(2)
    count += 1
    if count > 280:
        break