from windowcapture import ScreenRegion
import cv2 as cv
import uuid
import time

while True:
    screen = ScreenRegion()
    im = screen.get_screenshot()
    cv.imwrite("rock_fall_data//"+str(uuid.uuid4())+".png", im)
    time.sleep(1)

