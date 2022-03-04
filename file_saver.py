from regions import ScreenRegion
import cv2 as cv
import uuid
import time
i = 0
while True:
    screen = ScreenRegion()
    im = screen.get_screenshot()
    cv.imwrite("tourist_trap_data//"+str(i)+".png", im)
    i += 1
    time.sleep(1)

