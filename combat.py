import cv2 as cv
import win32gui
import pyautogui
import time
import random
from hsvfilter import HsvFilter
from bank import Bank
from vision import Vision
from windowcapture import WindowCapture


# # aids hsv filtering
# splat_filter = HsvFilter(sMax=126)
# splat_image = 'Needle\\cow\\8_splat.png'

splat_hit = Vision('Needle\\cow\\2_splat.png')
splat_miss = Vision('Needle\\cow\\0_splat.png')

ten_hp = Vision('Needle\\health_points\\10hp.png')
nine_hp = Vision('Needle\\health_points\\9hp.png')
eight_hp = Vision('Needle\\health_points\\8hp.png')
seven_hp = Vision('Needle\\health_points\\7hp.png')
six_hp = Vision('Needle\\health_points\\6hp.png')
five_hp = Vision('Needle\\health_points\\5hp.png')
four_hp = Vision('Needle\\health_points\\4hp.png')
three_hp = Vision('Needle\\health_points\\3hp.png')
two_hp = Vision('Needle\\health_points\\2hp.png')
one_hp = Vision('Needle\\health_points\\1hp.png')
# edited_needle = cv.imread(splat_image)
# splat_edited = splat.apply_hsv_filter(edited_needle, splat_filter)
# final_splat = Vision(splat_edited, edited=True)
# adjusted_screenshot = final_splat.apply_hsv_filter(screenshot, splat_filter)



class Combat:

    def __init__(self):
        self.counter = 0

    def in_combat(self): 
        self.wincap = WindowCapture('Bluestacks', area='character')
        while self.counter <= 15:
            screenshot = self.wincap.get_screenshot()

            # multiple needles extended to an empty list that clears every loop 
            rectangles1 = splat_hit.find(screenshot, threshold=0.4)
            rectangles2 = splat_miss.find(screenshot, threshold=0.4)
            rect_list = []
            rect_list.extend(rectangles1)
            rect_list.extend(rectangles2)


            # long sleep if hitsplat detected, short sleep if not
            if len(rect_list) == 0:
                print('No hitsplats detected...')
                self.counter += 1
                time.sleep(0.15)
                print(self.counter)
            else:
                self.counter = 0
                print('In combat... ')
                time.sleep(0.6)
        


    # TODO FINISH THIS MIGHT NEED OCR (easyocr) OR TRAIN OWN MODEL CR
    def eat(self, min_hp : int, food : str):
        '''
        eat a given food if below minimum hp, \n
        food is file path to food needle
        '''
        if self.get_current_hp <= min_hp:
            food_vis = Vision(food)
            self.wincap = WindowCapture('BlueStacks', area='inventory')
            screenshot = self.wincap.get_screenshot()
            rectangles = food_vis.find(screenshot, threshold=0.6)
            points = food_vis.get_click_points(rectangles)
            point = self.wincap.get_screen_position(points[0])
            pyautogui.click(point[0],point[1])
            # recursion ?????? why not just while loop hp less than min hp? good question
            return self.eat(min_hp, food)


    # if check for each hp needle, returning the current hp as int
    # garbage function only works for 10hp account
    def get_current_hp(self):
        '''
        gets current hp between 10 and 1
        '''
        self.wincap = WindowCapture('BlueStacks', area='health_orb')
        screenshot = self.wincap.get_screenshot()
        if ten_hp.match(screenshot, threshold=0.7)[0] == True:
            print("10 hp")
            return(10)
        elif nine_hp.match(screenshot, threshold=0.7)[0] == True:
            print("9 hp")
            return(9)
        elif eight_hp.match(screenshot, threshold=0.8)[0] == True:
            print("8 hp")
            return(8)
        elif seven_hp.match(screenshot, threshold=0.7)[0] == True:
            print("7 hp")
            return(7)
        elif six_hp.match(screenshot, threshold=0.8)[0] == True:
            print("6 hp")
            return(6)
        elif five_hp.match(screenshot, threshold=0.8)[0] == True:
            print("5 hp")
            return(5)
        elif four_hp.match(screenshot, threshold=0.8)[0] == True:
            print("4 hp")
            return(4)
        elif three_hp.match(screenshot, threshold=0.8)[0] == True:
            print("3 hp")
            return(3)
        elif two_hp.match(screenshot, threshold=0.7)[0] == True:
            print("2 hp")
            return(2)
        elif one_hp.match(screenshot, threshold=0.7)[0] == True:
            print("1 hp")
            return(1)
        else:
            print('No hp detected')
            return False

        # return current_hp

    def bugcheck(self):
        print('WOW')
