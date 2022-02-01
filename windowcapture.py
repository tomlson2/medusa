import numpy as np
from numpy import ndarray
import win32gui, win32api, win32ui, win32con
import time, random
from vision import Vision
import cv2 as cv
import sys

window_name = input('client name: ')
class WindowCapture:

    # constructor
    def __init__(self, window_name=window_name):

        self.window_name = window_name
        if self.window_name is None:
            self.hwnd = win32gui.GetDesktopWindow()
        else:
            self.hwnd = win32gui.FindWindow(None, self.window_name)
            if not self.hwnd:
                raise Exception('Window not found: {}'.format(self.window_name))

        # set the window size
        win32gui.MoveWindow(self.hwnd, 0, 0, 1920, 1112, True)

        window_rect = win32gui.GetWindowRect(self.hwnd)

        w = window_rect[2] - window_rect[0]
        h = window_rect[3] - window_rect[1]

        # account for the window border and titlebar and cut them off
        self.border_pixels = 1
        self.titlebar_pixels = 33
        self.w_diff = (self.border_pixels * 2)
        self.h_diff = self.titlebar_pixels - self.border_pixels
        x = self.border_pixels
        y = self.titlebar_pixels

        self.x = x
        self.y = y
        self.w = w
        self.h = h        


        self.offset_x = window_rect[0]
        self.offset_y = window_rect[1]

    def get_region(self):
        return self.x, self.y, self.w, self.h
    
    def get_window(self):
        hwnd = win32gui.FindWindowEx(self.hwnd, None, None, None)
        return hwnd

    def get_screenshot(self):
            
        # get the window image data
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (self.w, self.h), dcObj, (self.x, self.y), win32con.SRCCOPY)

        # convert the raw data into a format opencv can read
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.frombuffer(signedIntsArray, dtype='uint8')
        img.shape = (self.h, self.w, 4)

        # free resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        img = img[...,:3]

        img = np.ascontiguousarray(img)

        return img

    @staticmethod
    def list_window_names():
        def winEnumHandler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                print(hex(hwnd), win32gui.GetWindowText(hwnd))
        win32gui.EnumWindows(winEnumHandler, None)


class Interactions(WindowCapture, Vision):
    def __init__(self):
        super().__init__()
    
    def get_screen_position(self, pos):
        return (pos[0]+self.x-self.border_pixels, pos[1]+self.y-self.titlebar_pixels)
    
    def right_click(self, item: object, threshold: float = 0.7, timeout = 7):
        self.mouse_down()
        time.sleep(random.normalvariate(0.72,0.1))
        self.mouse_up()

    def mouse_down(self, lParam):
        hwnd = self.get_window()
        win32gui.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)

    def mouse_up(self, lParam):
        hwnd = self.get_window()
        win32gui.SendMessage(hwnd, win32con.WM_LBUTTONUP, None, lParam)

    def click(self, item: object, threshold: float = 0.7, timeout = 7, right_click: bool = False):
        # looks for item to click with _ second timeout.
        s = time.time()
        while time.time()-s < timeout:
            rectangles = item.find(self.apply_hsv_filter(self.get_screenshot(),hsv_filter=item.get_hsv_filter()),threshold)
            if len(rectangles) > 0:
                break

        points = item.get_click_points(rectangles)
        point = self.get_screen_position(points[0])
        #print(point)
        lParam = win32api.MAKELONG(point[0], point[1])

        self.mouse_down(lParam)
        if right_click == True:
            time.sleep(random.normalvariate(0.8,0.01))
        self.mouse_up(lParam)

        time.sleep(random.normalvariate(0.25,0.02))
    
    def click_list(self, items: list, threshold: float = 0.7, timeout = 7, right_click: bool = False):
        # looks for item to click with _ second timeout.
        s = time.time()
        while time.time()-s < timeout:
            for item in items:
                rectangles = item.find(self.apply_hsv_filter(self.get_screenshot(),hsv_filter=item.get_hsv_filter()),threshold)
                if len(rectangles) > 0:
                    break
            if len(rectangles) > 0:
                break

        points = item.get_click_points(rectangles)
        point = self.get_screen_position(points[0])
        #print(point)
        lParam = win32api.MAKELONG(point[0], point[1])

        self.mouse_down(lParam)
        if right_click == True:
            time.sleep(random.normalvariate(0.8,0.01))
        self.mouse_up(lParam)

        time.sleep(random.normalvariate(0.25,0.02))

        return item
    
    def drag(self):
        lParam1 = win32api.MAKELONG(100, 100)
        self.mouse_down(lParam1)
        lParam2 = win32api.MAKELONG(300, 300)
        self.mouse_up(lParam2)


    def fast_click(self, item: object, threshold: float = 0.7, timeout = 7, right_click: bool = False):
        # looks for item to click with _ second timeout.
        s = time.time()
        while time.time()-s < timeout:
            rectangles = item.find(self.apply_hsv_filter(self.get_screenshot(),hsv_filter=item.get_hsv_filter()),threshold)
            if len(rectangles) > 0:
                break

        points = item.get_click_points(rectangles)
        point = self.get_screen_position(points[0])
        print(point)
        lParam = win32api.MAKELONG(point[0], point[1])

        self.mouse_down(lParam)
        if right_click == True:
            time.sleep(random.normalvariate(0.8,0.01))
        self.mouse_up(lParam)

        time.sleep(random.normalvariate(0.15,0.02))
        
    def hold_shift(self):
        hwnd = self.get_window()
        win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_SHIFT, None)
        
    def release_shift(self):
        hwnd = self.get_window()
        win32gui.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_SHIFT, None)
                        
    def shift_click(self, item : object, threshold : float = 0.7):

        s = time.time()
        
        while time.time()-s < 10:
            rectangles = item.find(self.apply_hsv_filter(self.get_screenshot(),hsv_filter=item.get_hsv_filter()),threshold)
            if len(rectangles) > 0:
                break

        points = item.get_click_points(rectangles)
        point = self.get_screen_position(points[0])

        hWnd = win32gui.FindWindow(None, self.window_name)
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
        hWnd = win32gui.FindWindow(None, self.window_name)
        lParam = win32api.MAKELONG(point[0], point[1])

        hWnd1 = win32gui.FindWindowEx(hWnd, None, None, None)
        win32gui.SendMessage(hWnd1, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
        win32gui.SendMessage(hWnd1, win32con.WM_LBUTTONUP, None, lParam)

        time.sleep(random.normalvariate(0.2,0.02))

    def click_region(self, rectangle : ndarray, right_click : bool = False):
        
        points = self.get_click_points(rectangle)
        point = self.get_screen_position(points[0])

        hWnd = win32gui.FindWindow(None, self.window_name)
        lParam = win32api.MAKELONG(point[0], point[1])

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
        if len(item.find(self.apply_hsv_filter(self.get_screenshot(),hsv_filter=item.get_hsv_filter()),threshold)) > 0:
            return True
        else:
            return False
    
    def amount(self, item, threshold):
        return len(item.find(self.apply_hsv_filter(self.get_screenshot(),hsv_filter=item.get_hsv_filter()),threshold))

    def wait_for(self, item : object, threshold : float = 0.7, t: int = 5):
        """
        Waits for something to appear on screen region with a 10 second timeout period.
        """
        start_time = time.time()
        while self.contains(item, threshold) == False:
            current_time = (time.time() - start_time)
            if current_time > t:
                print(f"Failed to find Needle in {t} seconds")
                break
class CustomRegion(Interactions):

    def __init__(self, w1, h1, x1, y1):
        super().__init__()
        self.w = w1
        self.h = h1
        self.x = x1
        self.y = y1

          
class InventoryRegion(Interactions):

    def __init__(self):
        super().__init__()
        self.w = 408
        self.h = 559
        self.x = 1388
        self.y = 477
    
    def drink_potion(self):
        self.click()
    
    def num_items(self):
        im = self.get_screenshot()
        gray = cv.cvtColor(im,cv.COLOR_BGR2GRAY)
        blur = cv.GaussianBlur(gray,(5,5),0)
        mask = cv.adaptiveThreshold(blur,255,1,1,11,2)
        contours, _ = cv.findContours(mask, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
        rectangles = []
        for cnt in contours:
            if 7500 > cv.contourArea(cnt) > 350:
                x, y, w, h = cv.boundingRect(cnt)
                if w<500 and h<500:
                    rectangles.append([x, y, w, h])
                    rectangles.append([x, y, w, h])
        rects, weights = cv.groupRectangles(rectangles, groupThreshold=1, eps=1)
        return len(rects)

    def drop_click(self, item : object, quantity : int, threshold=0.7):
        '''
        must have drop mode on before call
        '''
        rectangles = item.find(self.apply_hsv_filter(self.get_screenshot(),hsv_filter=item.get_hsv_filter()),threshold)
        for i in range(quantity):
            points = item.get_click_points(rectangles)
            point = self.get_screen_position(points[i])
            lParam = win32api.MAKELONG(point[0], point[1])
            self.mouse_down(lParam)
            self.mouse_up(lParam)
            time.sleep(random.normalvariate(0.31, 0.02))
            
    def drop_list_vert(self, list : list, threshold=0.7):
        '''
        drops everything in inventory vertically of param list.
        must have drop mode on before call.
        gets the click points of all the items of the list to drop.
        then sorts the list and drops them.
        '''
        point_list = []
        # get all rectangles
        for i in range(len(list)):
            rectangles = (list[i].find(self.apply_hsv_filter(self.get_screenshot(),hsv_filter=list[i].get_hsv_filter()),threshold))
            points = list[i].get_click_points(rectangles)
            point_list.extend(points)
        
        # remove empty tuples
        point_list = [t for t in point_list if t]
        # sort rectangles
        point_list.sort(key = lambda x: x[0])
        point_list0 = []
        point_list1 = []
        point_list2 = []
        point_list3 = []

        for t in point_list:
            if t[0] < 100:
                point_list0.append(t)
            elif t[0] < 200:
                point_list1.append(t)
            elif t[0] < 300:
                point_list2.append(t)
            elif t[0] < 400:
                point_list3.append(t)
        
        list_list = [point_list0, point_list1, point_list2, point_list3]
        for l in list_list:
            l.sort(key = lambda x: x[1])
        
        final_list = []
        for l in list_list:
            final_list.extend(l)

        print(f'dropping {len(final_list)} items')
        #drop items in sorted order
        for i in range(len(point_list)):
            point = self.get_screen_position(final_list[i])
            lParam = win32api.MAKELONG(point[0], point[1])
            self.mouse_down(lParam)
            self.mouse_up(lParam)
            time.sleep(random.normalvariate(0.31, 0.02))
        
    
class ScreenRegion(Interactions):

    def __init__(self):
        super().__init__()
class ChatboxRegion(Interactions):

    def __init__(self):
        super().__init__()
        self.w = 1105
        self.h = 297
        self.x = 29
        self.y = 37

class BankRegion(Interactions):

    def __init__(self):
        super().__init__()
        self.w = 1025
        self.h = 688
        self.x = 295
        self.y = 376


class MinimapRegion(Interactions):
    def __init__(self):
        super().__init__()
        self.w = 217
        self.h = 208
        self.x = 1604
        self.y = 96