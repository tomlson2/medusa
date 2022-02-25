from typing import Tuple
import numpy as np
from numpy import ndarray
from ocr import Ocr
import win32gui, win32api, win32ui, win32con
import time, random
from hsvfilter import HsvFilter
from model import Model
from vision import Vision
import cv2 as cv
from errors import OptionHandlerError
from image_tools import contour_boxes

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

    def click(self, item: object, threshold: float = 0.7, timeout = 7, right_click: bool = False, ind = 0):
        # looks for item to click with _ second timeout.
        s = time.time()
        while time.time()-s < timeout:
            rectangles = self.get_rectangles(item, threshold)
            if len(rectangles) > 0:
                break

        points = item.get_click_points(rectangles)
        point = self.get_screen_position(points[ind])
        #print(point)
        lParam = win32api.MAKELONG(point[0], point[1])

        self.mouse_down(lParam)
        if right_click == True:
            time.sleep(random.normalvariate(0.75,0.01))
        self.mouse_up(lParam)

        time.sleep(random.normalvariate(0.25,0.02))
    
    def get_rectangles(self, item, threshold):
        if type(item) == Vision:
            rectangles = item.find(self.apply_hsv_filter(self.get_screenshot(),hsv_filter=item.get_hsv_filter()),threshold)
        elif type(item) == Model:
            rectangles = item.find(self.get_screenshot(),threshold)
        
        return rectangles

    def click_list(self, items: list, threshold: float = 0.7, timeout = 7, right_click: bool = False):
        # looks for item to click with _ second timeout.
        s = time.time()
        matches = np.empty((0,4),int)
        inxlst = []
        while time.time()-s < timeout:
            for inx, item in enumerate(items):
                rectangles = self.get_rectangles(item, threshold)
                for _ in rectangles:
                    inxlst.append(inx)
                if len(rectangles) > 0:
                    matches = np.append(matches, rectangles, axis=0)
            if len(matches) > 0:
                break
        
        rectangles, idx = self.get_center_rectangles(matches)

        inxlst = [inxlst[i] for i in idx.tolist()]

        points = item.get_click_points(rectangles)
        point = self.get_screen_position(points[0])

        lParam = win32api.MAKELONG(point[0], point[1])

        self.mouse_down(lParam)
        if right_click == True:
            time.sleep(random.normalvariate(0.8,0.01))
        self.mouse_up(lParam)

        time.sleep(random.normalvariate(0.25,0.02))
        return items[inxlst[0]]

    def click_self(self):

        point = self.get_click_points(np.array([(self.x, self.y, self.w, self.h)]))

        hWnd = win32gui.FindWindow(None, self.window_name)
        lParam = win32api.MAKELONG(point[0][0], point[0][1])

        hWnd1 = win32gui.FindWindowEx(hWnd, None, None, None)
        win32gui.SendMessage(hWnd1, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
        win32gui.SendMessage(hWnd1, win32con.WM_LBUTTONUP, None, lParam)
        time.sleep(random.normalvariate(0.2,0.01))
    
    def drag(self):
        lParam1 = win32api.MAKELONG(100, 100)
        self.mouse_down(lParam1)
        lParam2 = win32api.MAKELONG(300, 300)
        self.mouse_up(lParam2)


    def fast_click(self, item: object, threshold: float = 0.7, timeout = 7, right_click: bool = False):
        # looks for item to click with _ second timeout.
        s = time.time()
        while time.time()-s < timeout:
            rectangles = rectangles = self.get_rectangles(item, threshold)
            if len(rectangles) > 0:
                break

        points = self.get_click_points(rectangles)
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
            rectangles = rectangles = self.get_rectangles(item, threshold)
            if len(rectangles) > 0:
                break

        points = self.get_click_points(rectangles)
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

    def click_point(self, point : tuple, relative = True):

        if relative == True:
            point = self.get_screen_position(point)

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
    
    def contains(self, item: object, threshold: float = 0.7, screenshots = 1) -> bool:
        """
        Checks if screen region contains certain needle and returns a boolean value
        """
        found = 0
        not_found = 0
        for _ in range(screenshots):
            if self.amount(item, threshold) > 0:
                found += 1
            else:
                not_found += 1
            time.sleep(0.01)
        if (found/screenshots) > .25:
            return True
        else:
            return False
    
    def amount(self, item, threshold = 0.7):
        return len(self.get_rectangles(item=item, threshold=threshold))

    def wait_for(self, item : object, threshold : float = 0.7, t: int = 5):
        """
        Waits for something to appear on screen region with a 10 second timeout period.
        """
        start_time = time.time()
        while self.contains(item, threshold) == False:
            current_time = (time.time() - start_time)
            if current_time > t:
                print(f"Failed to find Needle in {t} seconds")
                return False
            else:
                pass
                
            
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

        self.item_amt = None
        self.timer = None
    
    def drink_potion(self):
        self.click()

    def line_process(self):
        im = self.get_screenshot()
        im = self.apply_hsv_filter(im, hsv_filter=HsvFilter(vMax=28))
        gray = cv.cvtColor(im,cv.COLOR_BGR2GRAY)
        lines = cv.Canny(gray, 0, 0)
        blur = cv.GaussianBlur(lines,(3,3),0)
        edited_im = cv.adaptiveThreshold(blur,255,1,1,11,2)
        return edited_im

    def num_items(self, debugger = False):
        number = 0
        im = self.line_process()
        bgr_im = cv.cvtColor(im, cv.COLOR_GRAY2BGR)
        contours, _ = cv.findContours(im, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        cnt_rects = []
        for cnt in contours:
            area = cv.contourArea(cnt)
            x,y,w,h = cv.boundingRect(cnt)
            x += int((w * 0.5)/2)
            y += int((h * 0.5)/2)
            w = int(w * 0.5)
            h = int(h * 0.5)
            if area > 150:
                cnt_rects.append((x, y, w, h))        
                cv.rectangle(bgr_im, (x, y), (x + w, y + h), (0, 255, 0), 2)
        x = 15
        y = 10
        w = 90
        h = 75

        inventory_spot = 1
        while x < 350 and y < 590:
            while x < 350:
                for r in cnt_rects:
                    if x < r[0] and y < r[1]:
                        if x + w > r[0] + r[2] and y + h > r[1] + r[3]:
                            number += 1
                            break
                cv.rectangle(bgr_im, (x, y), (x+w, y+h), (255,0,0),2)
                inventory_spot += 1
                x += 95
            x = 15
            y += 78
        
        if debugger == True:
            cv.imshow('1', bgr_im)
            cv.waitKey(0)
            cv.destroyAllWindows()
        
        return number

    
    def is_full(self) -> bool:
        if self.num_items() == 28:
            return True
        else:
            return False
    
    def is_emptying(self, interval = 5.5) -> bool:
        '''
        checks if inventory is emptying out (at least 1 item every x amount of seconds)
        useful for things like wintertodt where you put in one thing at a time
        '''
        if self.timer is None:
            self.timer = time.time()
        num = self.num_items()
        if time.time() - self.timer > interval:
            self.timer = None
            if num == self.num_items():
                return False
            else:
                return True
    
    def item_increasing(self, item: object, interval = 5.5) -> bool:
        if self.item_amt is None:
            self.item_amt = self.amount(item)
        elif self.timer is None:
            self.timer = time.time()
        else:
            if time.time() - self.timer > interval:
                self.timer = None
                if self.amount(item) > self.item_amt:
                    self.item_amt = self.amount(item)
                    return True
                else:
                    self.item_amt = self.amount(item)
                    return False
            

    def drop_click(self, item: object, quantity: int, threshold=0.7):
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
            
    def drop_click_vert(self, item : object, quantity : int, threshold=0.7):
        '''
        vertical dropping, drop mode must be on
        '''
        rectangles = item.find(self.apply_hsv_filter(self.get_screenshot(),hsv_filter=item.get_hsv_filter()),threshold)
        points = item.get_click_points(rectangles)
        points.sort(key = lambda x: x[0])
        for i in range(quantity):
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
            time.sleep(random.normalvariate(0.21, 0.02))
        
    
class ScreenRegion(Interactions):

    def __init__(self):
        super().__init__()
        
class ChatboxRegion(Interactions):

    def __init__(self):
        super().__init__()
        self.w = 1076
        self.h = 267
        self.x = 48
        self.y = 52
    
        self.tap_here = Vision("Needle\\chatbox\\tap_here_to_continue.png")
        self.please_wait = Vision("Needle\\chatbox\\please_wait.png")
        self.please_wait_black = Vision("Needle\\chatbox\\please_wait_black.png")
    
    def tap_handler(self):

        while True:
            if self.contains(self.tap_here,0.85):
                self.click(self.tap_here, 0.85)
                time.sleep(0.25)
            elif self.contains(self.please_wait, 0.85) or self.contains(self.please_wait_black, 0.85):
                time.sleep(0.25)
            else:
                break

    def contains_dialogue(self):
        if self.contains(self.tap_here):
            return True


    def options(self) -> Tuple[list, int]:
        self.tap_handler()
        if self.contains(Vision("Needle\\chatbox\\select_option.png"), 0.85):
            im = self.get_screenshot()
            gray_im = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
            canny_im = cv.Canny(gray_im, 200, 200)
            blurred_im = cv.GaussianBlur(canny_im, (9, 9), cv.BORDER_DEFAULT)
            contours, _ = cv.findContours(blurred_im, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
            
            rects = []
            for cnt in contours:
                area = cv.contourArea(cnt)
                if area > 200:
                    x, y, w, h = cv.boundingRect(cnt)
                    rects.append((x, y, w, h))

            y_vals = []
            y_vals.append(rects[0][2])
            for x,y,w,h in rects:
                for ht in y_vals:
                    if ht-25 < y < ht+25:
                        match = True
                        break
                    else:
                        match = False
                if match == False:
                    y_vals.append(y)
                
                num = len(y_vals) - 1
            
            y_vals = [y + 30 for y in y_vals]
            y_vals.sort()
            return y_vals, num

    def option_handler(self, options: list):
        for option in options:
            deadloop = 0
            while True:
                try:
                    y_vals, num = self.options()
                    break
                except TypeError:
                    if deadloop > 4:
                        break
                    else:
                        time.sleep(0.2)
                        deadloop += 1
            if option > num or option == 0:
                raise OptionHandlerError("Option was not in range of possible selection!")

            y_val = y_vals[option]
            x_val = int(random.normalvariate(600, 25))
            self.click_point((x_val, y_val))
        

class PlayerRegion(Interactions):

    def __init__(self):
        super().__init__()
        self.w = 206
        self.h = 297
        self.x = 838
        self.y = 386
    
    def is_animating(self, history=100, threshold=40, loops=40):
        object_detector = cv.createBackgroundSubtractorMOG2(history=history, varThreshold=threshold)
        found = False
        im = self.get_screenshot()
        mask = object_detector.apply(im)
        for _ in range(loops):
            im = self.get_screenshot()
            mask = object_detector.apply(im)
            contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
            stencil = np.zeros(im.shape).astype(im.dtype)
            cv.fillPoly(stencil, contours, [255, 255, 255])
            for cnt in contours:
                area = cv.contourArea(cnt)
                if area > 1000:
                    found = True
                    break
                else:
                    pass
            time.sleep(0.05)
        if found == True:
            return True
        else:
            return False
            

class BankRegion(Interactions):

    def __init__(self):
        super().__init__()
        self.w = 1031
        self.h = 697
        self.x = 296
        self.y = 375

        self.quantity = 0
    
        self.stamina_pot = Vision('Needle\\stam.png')
        self.bank_check = Vision('Needle\\inventory_guy.png')
        self.exit = Vision('Needle\\x_bank.png')
        self.withdraw1 = Vision('Needle\\withdraw1.png')
        self.withdraw_all = Vision('Needle\\withdraw_all.png')
    
    def check_quantity(self):
        pass

    def set_quantity(self):
        pass

    def status(self):
        bank_interface = ScreenRegion().contains(self.bank_check,0.9)
        return bank_interface

    def withdraw(self, item, threshold=0.7, quantity=1):

        if self.status() == True:
            for _ in range(quantity):
                self.click(item, threshold)
        else:
            print("Not in bank interface.")    

    def wait_interface(self):
        timeout = time.time() + 10
        while self.status() == False: 
            if time.time() > timeout:
                return False
            time.sleep(0.1)
        return True

    def deposit(self, item, threshold=0.7, quantity=1):
        if self.status() == True:
            for _ in range(quantity):
                InventoryRegion().click(item, threshold)
        else:
            print("Not in bank interface.")
    
    def close(self):
        self.wait_for(self.exit,0.76)
        self.click(self.exit,0.76)

class ShopRegion(Interactions):

    def __init__(self):
        super().__init__()
        self.w = 1014
        self.h = 460
        self.x = 299
        self.y = 480
    
    def set_quantity(self, quantity):
        quantity_region = CustomRegion(539, 74, 767, 958)

        self.quantity1 = Vision('Needle\\shop\\quantity_1.png')
        self.quantity5 = Vision('Needle\\shop\\quantity_5.png')
        self.quantity10 = Vision('Needle\\shop\\quantity_10.png')
        self.quantity50 = Vision('Needle\\shop\\quantity_50.png')
        if quantity == 1:
            if quantity_region.contains(self.quantity1, 0.95):
                quantity_region.click(self.quantity1)
        if quantity == 5:
            if quantity_region.contains(self.quantity5, 0.95):
                quantity_region.click(self.quantity5)
        if quantity == 10:
            if quantity_region.contains(self.quantity10, 0.95):
                quantity_region.click(self.quantity10)
        if quantity == 50:
            if quantity_region.contains(self.quantity50, 0.95):
                quantity_region.click(self.quantity50)
        else:
            print("Incorrect quantity selected")
    
    def items(self) -> Tuple[list, int]:
        im = self.get_screenshot()
        hsv_img = self.apply_hsv_filter(im, HsvFilter(vMax=50))
        gray_im = cv.cvtColor(hsv_img, cv.COLOR_BGR2GRAY)
        canny_im = cv.Canny(gray_im, 1, 1)
        blurred_im = cv.GaussianBlur(canny_im, (9, 9), cv.BORDER_DEFAULT)
        rectangles = contour_boxes(blurred_im, 50)
        num = len(rectangles)
        return rectangles, num
        

    def purchase(self, index, quantity):
        if index > self.items()[1]:
            print("Selected item that is not in purchasable index!")
        else:
            self.set_quantity(quantity)
            point = self.get_click_points(self.items()[0])
            self.click_point(point[index])

class MinimapRegion(Interactions):

    def __init__(self):
        super().__init__()
        self.w = 217
        self.h = 208
        self.x = 1604
        self.y = 96

class RunOrb(Interactions):

    def __init__(self):
        super().__init__()
        self.w = 38
        self.h = 38
        self.x = 1527
        self.y = 292        
    
    def is_active(self):
        if self.contains(Vision('Needle\\orbs\\run_boot.png'),0.95):
            return True
        else:
            return False
    
    def run(self):
        if self.is_active() == True:
            pass
        else:
            self.click_self()

    def walk(self):
        if self.is_active() == True:
            self.click_self()

class HealthOrb(Interactions):

    def __init__(self):
        super().__init__()
        self.w = 42
        self.h = 27
        self.x = 1449
        self.y = 166

        self.filter = HsvFilter(vMin=136,sSub=255)
        self.orbs = Ocr('samples/generalsamples.data', 'responses/generalresponses.data')

        self.hp = 0

    def get_hp(self):
        im = self.apply_hsv_filter(self.get_screenshot(),self.filter)
        return self.orbs.number(im)
    
    def update_hp(self):
        self.hp = self.get_hp()

    def damage_taken(self):
        if self.get_hp() < self.hp:
            self.update_hp()
            return True
        else:
            self.update_hp()
            return False

        
        

