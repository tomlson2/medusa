import cv2 as cv
import numpy as np
import pyautogui
import random
import time
import win32gui
from bank import Bank
from windowcapture import WindowCapture
from vision import Vision
from hsvfilter import HsvFilter

bankchest = Bank('Needle\\booth.png')
bankchest.withdraw('Needle\\sapphire.png',0)



# while True:
#     vision = Vision('Needle\\bluestacks2.png')
#     screenshot = inventory.get_screenshot()
#     rectangles = vision.find(screenshot,0.4)
#     points = inventory.get_screen_position(rectangles)
#     img = vision.draw_rectangles(screenshot,rectangles)
#     cv.imshow('s',img)
#     print(len(rectangles))

#initialize the WindowCapture class

# wincap = WindowCapture('BlueStacks')

# def click_rect(needle,threshold,hsv_filter=None,x_off=0,y_off=0):
#     vision = Vision(needle)
#     if hsv_filter == None:
#         vision = Vision(needle)
#         screenshot = wincap.get_screenshot()
#     else:
#         needle = cv.imread(needle)
#         needle = vision.apply_hsv_filter(needle,hsv_filter=hsv_filter)
#         vision = Vision(needle,edited=True)
#         screenshot = wincap.get_screenshot()
#         screenshot = vision.apply_hsv_filter(screenshot,hsv_filter=hsv_filter)
#     rectangles = vision.find(screenshot, threshold)
#     targets = vision.get_click_points(rectangles)
#     target = wincap.get_screen_position(targets[0])
#     pyautogui.moveTo(x=target[0] + 9 + x_off, y=target[1] + 45 + y_off)
#     pyautogui.click()
#     time.sleep(random.uniform(1,2.5))
#    return screenshot

# def hold_click(needle1,needle2,threshold1,threshold2):
#     screenshot = wincap.get_screenshot()
#     vision = Vision(needle1)
#     rectangles = vision.find(screenshot,threshold1)
#     targets = vision.get_click_points(rectangles)
#     target = wincap.get_screen_position(targets[0])
#     pyautogui.moveTo(x=target[0]+9, y=target[1] + 45)
#     pyautogui.mouseDown()
#     time.sleep(random.uniform(0.75,1.5))
#     screenshot = wincap.get_screenshot()
#     vision = Vision(needle2)
#     rectangles = vision.find(screenshot,threshold2)
#     targets = vision.get_click_points(rectangles)
#     target = wincap.get_screen_position(targets[0])
#     pyautogui.moveTo(x=target[0]+9, y=target[1] + 45)
#     pyautogui.mouseUp()
#     time.sleep(random.uniform(2,2.5))


# def wait_finish(needle,threshold):
#     while(True):
#         screenshot = wincap.get_screenshot()
#         vision = Vision(needle)
#         rectangles = vision.find(screenshot, threshold)
#         if len(rectangles) == 0:
#             print('Finished!')
#             break
#         else:
#             print("Crafting... " + str(len(rectangles)) + " left!")

# #loop_time = time()

# while(True):
#     #click_rect('Needle\\bankchest.png', 0.65)
#     click_rect('Needle\\coal_bank.png', 0.7,hsv_filter=HsvFilter())
#     click_rect('Needle\\x_bank.png', 0.7)
#     click_rect('Needle\\pipes.png', 0.7,x_off=-140, y_off=-45)
#     time.sleep(5)
#     click_rect('Needle\\bars.png',0.62,x_off=235,y_off=35,hsv_filter=HsvFilter())
#     time.sleep(3)
#     click_rect('Needle\\bar_collector.png',0.7,x_off=-65)
#     time.sleep(3)
#     click_rect('Needle\\stairs.png',0.6,x_off=55,y_off=-30)
#     time.sleep(3)
#     click_rect('Needle\\boxes.png',0.58,x_off=50,hsv_filter=HsvFilter(sAdd=100))
#     time.sleep(3)
#     click_rect('Needle\\bankchest.png',0.65)
#     time.sleep(2)
#     click_rect('Needle\\iron_bank.png',0.7,hsv_filter=HsvFilter())
#     click_rect('Needle\\x_bank.png', 0.7)
#     click_rect('Needle\\pipes.png', 0.7,x_off=-150, y_off=-45)
#     time.sleep(5)
#     click_rect('Needle\\bars.png',0.62,x_off=235,y_off=35,hsv_filter=HsvFilter())
#     time.sleep(3)
#     click_rect('Needle\\bar_collector.png',0.7,x_off=-65)
#     time.sleep(8)
#     click_rect('Needle\\collrdy.png',0.65,hsv_filter=HsvFilter(sAdd=120))
#     time.sleep(2)
#     click_rect('Needle\\sbar.png',0.8)
#     click_rect('Needle\\stairs.png',0.6,x_off=55,y_off=-30)
#     time.sleep(3)
#     click_rect('Needle\\boxes.png',0.58,x_off=50,hsv_filter=HsvFilter(sAdd=100))
#     time.sleep(3)
#     click_rect('Needle\\bankchest.png',0.65)
#     time.sleep(2)
#     click_rect('Needle\\steelbar.png',0.75)


#     # while(True):
#     #     cv.imshow('win',screenshot)
#     #     # press 'q' with the output window focused to exit.
#     #     # waits 1 ms every loop to process key presses
#     #     if cv.waitKey(1) == ord('q'):
#     #         cv.destroyAllWindows()
#     #         break

# print('Done.')