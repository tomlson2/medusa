from numpy import float64, ndarray
import win32gui, win32con, win32api
import time
import random
from numpy import ndarray
from hsvfilter import HsvFilter
from vision import Vision
from windowcapture import WindowCapture
# from ocr import Ocr
# import cv2 as cv

class Interactions:
    """
    Screen region object used for checking and interacting with needles.
    """

    def __init__(self, area: str = None):
        self.area = area
        self.wincap = WindowCapture()
        self.vision = Vision('Needle\\banana.png')
        # self.ocr = Ocr('samples/bold12lowersamples.data', 'responses/bold12lowerresponses.data')
    

    def click(self, item: object, threshold : float = 0.7, right_click : bool = False):
        """
        Finds and clicks on needle based on region of defined Interaction object.
        """

        # looks for item to click with 10 second timeout.
        s = time.time()
        while time.time()-s < 7:
            # print(time.time()-s)
            rectangles = item.find(self.vision.apply_hsv_filter(WindowCapture(area = self.area).get_screenshot(),hsv_filter=item.get_hsv_filter()),threshold)
            if len(rectangles) > 0:
                break

        points = item.get_click_points(rectangles)
        point = WindowCapture(area = self.area).get_screen_position(points[0])

        hWnd = win32gui.FindWindow(None, "BlueStacks")
        lParam = win32api.MAKELONG(point[0]-1, point[1]-33)

        hWnd1 = win32gui.FindWindowEx(hWnd, None, None, None)
        win32gui.SendMessage(hWnd1, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
        
        if right_click == True:
            time.sleep(random.normalvariate(.72,.01))

        win32gui.SendMessage(hWnd1, win32con.WM_LBUTTONUP, None, lParam)

        time.sleep(random.normalvariate(0.25,0.02))

        # TODO
        # if point[0] < 964:
        #     self.wincap.x = point[0] + 65
        #     self.wincap.y = point[1] - 20
        #     self.wincap.w = 300
        #     self.wincap.h = 45
        # else:
        #     self.wincap.x = point[0] - 365
        #     self.wincap.y = point[1] - 20
        #     self.wincap.w = 300
        #     self.wincap.h = 45

        # im = self.wincap.get_screenshot()
        
        # print(self.ocr.text(im))

        
    def hold_shift(self):
        hWnd = win32gui.FindWindow(None, "BlueStacks")
        hWnd1 = win32gui.FindWindowEx(hWnd, None, None, None)
        win32gui.SendMessage(hWnd1, win32con.WM_KEYDOWN, win32con.VK_SHIFT, None)
        
    def release_shift(self):
        hWnd = win32gui.FindWindow(None, "BlueStacks")
        hWnd1 = win32gui.FindWindowEx(hWnd, None, None, None)
        win32gui.SendMessage(hWnd1, win32con.WM_KEYUP, win32con.VK_SHIFT, None)
        
                
    def shift_click(self, item : object, threshold : float = 0.7):
        """
        Finds and shift clicks a needle based on region of defined 'item' Interaction object.
        """
        s = time.time()
        
        while time.time()-s < 10:
            #print(time.time()-s)
            rectangles = item.find(self.vision.apply_hsv_filter(WindowCapture(area = self.area).get_screenshot(),hsv_filter=item.get_hsv_filter()),threshold)
            if len(rectangles) > 0:
                break

        points = item.get_click_points(rectangles)
        point = WindowCapture(area = self.area).get_screen_position(points[0])

        hWnd = win32gui.FindWindow(None, "BlueStacks")
        lParam = win32api.MAKELONG(point[0]-1, point[1]-33)

        hWnd1 = win32gui.FindWindowEx(hWnd, None, None, None)
        
        #vk_shift is shift key
        #press keys
        #for shift to work window has to be focused! IDK WHY OR HOW TO FIX
        win32gui.SendMessage(hWnd1, win32con.WM_KEYDOWN, win32con.VK_SHIFT, lParam)
        time.sleep(random.normalvariate(.15, 0.001))
        win32gui.SendMessage(hWnd1, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
        #release keys
        time.sleep(.05)
        win32gui.SendMessage(hWnd1, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, lParam)
        time.sleep(random.normalvariate(.15, 0.005))
        win32gui.SendMessage(hWnd1, win32con.WM_KEYUP, win32con.VK_SHIFT, lParam)


    
    def click_point(self, point : tuple):
        hWnd = win32gui.FindWindow(None, "BlueStacks")
        lParam = win32api.MAKELONG(point[0]-1, point[1]-33)

        hWnd1 = win32gui.FindWindowEx(hWnd, None, None, None)
        win32gui.SendMessage(hWnd1, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
        win32gui.SendMessage(hWnd1, win32con.WM_LBUTTONUP, None, lParam)

        time.sleep(random.normalvariate(0.2,0.02))

    def click_region(self, rectangle : ndarray, right_click : bool = False):
        
        points = self.vision.get_click_points(rectangle)
        point = WindowCapture(area = self.area).get_screen_position(points[0])

        hWnd = win32gui.FindWindow(None, "BlueStacks")
        lParam = win32api.MAKELONG(point[0]-2, point[1]-53)

        hWnd1 = win32gui.FindWindowEx(hWnd, None, None, None)
        win32gui.SendMessage(hWnd1, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
        
        if right_click == True:
            time.sleep(random.normalvariate(.72,.01))

        win32gui.SendMessage(hWnd1, win32con.WM_LBUTTONUP, None, lParam)

        time.sleep(random.normalvariate(0.25,0.03))
    
    def contains(self, item: object, threshold: float = 0.7) -> bool:
        """
        Checks if screen region contains certain needle and returns a boolean value
        """
        if len(item.find(self.vision.apply_hsv_filter(WindowCapture(area = self.area).get_screenshot(),hsv_filter=item.get_hsv_filter()),threshold)) > 0:
            return True
        else:
            return False
    
    def amount(self, item, threshold):
        return len(item.find(self.vision.apply_hsv_filter(WindowCapture(area = self.area).get_screenshot(),hsv_filter=item.get_hsv_filter()),threshold))


    def wait_for(self, item : object, threshold : float = 0.7):
        """
        Waits for something to appear on screen region with a 10 second timeout period.
        """
        start_time = time.time()
        while self.contains(item, threshold) == False:
            current_time = (time.time() - start_time)
            if current_time > 5:
                print("Failed to find Needle in 5 seconds")
                break
    