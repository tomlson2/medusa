import cv2 as cv
import numpy as np
import os
import pyautogui
import random
import time
from windowcapture import WindowCapture
from vision import Vision
from hsvfilter import HsvFilter


# initialize the WindowCapture class
wincap = WindowCapture('BlueStacks')
# initialize the Vision class
vision = Vision('Needle\\rubyruby.png')

#w,h,x,y = bounds.window_bounds(window="inventory")

def click_rect(needle,threshold):
    screenshot = wincap.get_screenshot(area=None)
    vision = Vision(needle)
    rectangles = vision.find(screenshot, threshold)
    targets = vision.get_click_points(rectangles)
    target = wincap.get_screen_position(targets[0])
    pyautogui.moveTo(x=target[0]+9, y=target[1] + 45)
    pyautogui.click()
    time.sleep(random.uniform(1,2.5))

def hold_click(needle1,needle2,threshold1,threshold2):
    screenshot = wincap.get_screenshot(area=None)
    vision = Vision(needle1)
    rectangles = vision.find(screenshot,threshold1)
    targets = vision.get_click_points(rectangles)
    target = wincap.get_screen_position(targets[0])
    pyautogui.moveTo(x=target[0]+9, y=target[1] + 45)
    pyautogui.mouseDown()
    time.sleep(random.uniform(0.75,1.5))
    screenshot = wincap.get_screenshot(area=None)
    vision = Vision(needle2)
    rectangles = vision.find(screenshot,threshold1)
    targets = vision.get_click_points(rectangles)
    target = wincap.get_screen_position(targets[0])
    pyautogui.moveTo(x=target[0]+9, y=target[1] + 45)
    pyautogui.mouseUp()
    time.sleep(random.uniform(2,2.5))


def wait_finish(needle,threshold):
    while(True):
        screenshot = wincap.get_screenshot(area=None)
        vision = Vision(needle)
        rectangles = vision.find(screenshot, threshold)
        if len(rectangles) == 0:
            print('Finished!')
            break
        else:
            if len(rectangles) == i:
                print("Crafting..." + str(len(rectangles)) + " left!")
            i = len(rectangles)

#loop_time = time()

while(True):

    click_rect('Needle\\maple_log.png',0.7)
    click_rect('Needle\\knife.png',0.65)
    click_rect('Needle\\interact_mapleshort.png',0.8)
    wait_finish('Needle\\maple_log.png',0.7)
    hold_click('Needle\\banker.png','Needle\\bank.png',0.45,0.8)
    click_rect('Needle\\unstrung_maple_short.png',0.8)
    click_rect('Needle\\maple_log.png',0.5)
    click_rect('Needle\\x_bank.png',0.8)

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break 

print('Done.')