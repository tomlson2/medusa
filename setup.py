import cv2 as cv
import numpy as np
import os
from time import time
from windowcapture import WindowCapture
from vision import Vision
from hsvfilter import HsvFilter

class Setup:

    def __init__(self):
        screenshot = WindowCapture("BlueStacks").get_screenshot(w=0,h=0,x=0,y=0,area=None)
        vision = Vision("Needle/inventorymarker.png")
        while(True):
            self.rectangles = vision.find(screenshot,0.8)
            output_image = vision.draw_rectangles(screenshot, self.rectangles)
            cv.imshow('Matches', output_image)
            if len(self.rectangles) >= 1:
                print(self.rectangles)
                break
            else:
                print('Unable to find inventory bounds')
    
    def window_bounds(self,window):
        if window == 'inventory':
            window_rect = self.rectangles
            w = 172
            h = 236
            x = window_rect[0][0]-170
            y = window_rect[0][1]+45
        
        else:
            w = 0
            h = 0
            x = 0
            y = 0
        return w,h,x,y
        