import numpy as np
import win32gui, win32ui, win32con

class WindowCapture:

    # constructor
    def __init__(self, window_name='BlueStacks', area=None):
        if window_name is None:
            self.hwnd = win32gui.GetDesktopWindow()
        else:
            self.hwnd = win32gui.FindWindow(None, window_name)
            if not self.hwnd:
                raise Exception('Window not found: {}'.format(window_name))


        # set the window size
        win32gui.MoveWindow(self.hwnd, 0, 0, 1920, 1112, True)

        window_rect = win32gui.GetWindowRect(self.hwnd)

        w = window_rect[2] - window_rect[0]
        h = window_rect[3] - window_rect[1]

        # account for the window border and titlebar and cut them off
        border_pixels = 1
        titlebar_pixels = 33
        self.w_diff = (border_pixels * 2)
        self.h_diff = titlebar_pixels - border_pixels
        self.cropped_x = border_pixels
        self.cropped_y = titlebar_pixels

        self.offset_x = window_rect[0]
        self.offset_y = window_rect[1]
        
        if area == None:
            self.w = w - self.w_diff
            self.h = h - self.h_diff
            self.x = self.cropped_x
            self.y = self.cropped_y
        
        if area == 'inventory':
            self.w = 408
            self.h = 559
            self.x = 1388
            self.y = 477

        if area == 'minimap':
            self.w = 217
            self.h = 208
            self.x = 1604
            self.y = 96

        if area == 'chatbox':
            self.w = 1105
            self.h = 297
            self.x = 29
            self.y = 37
        
        if area == 'bank':
            self.w = 1025
            self.h = 688
            self.x = 295
            self.y = 376
        
        if area == 'sidebar_r':
            self.w = 33
            self.h = 243
            self.x = 754
            self.y = 212
        
        if area == 'bank_test':
            self.w = 200
            self.h = 89
            self.x = 317
            self.y = 523
        
        if area == 'xp_bar':
            self.w = 56
            self.h = 30
            self.x = 402
            self.y = 523

        if area == 'character':
            self.w = 175
            self.h = 175
            self.x = 305
            self.y = 175
        
        if area == 'digiting':
            self.w = 121
            self.h = 181
            self.x = 1439
            self.y = 160
        
        if area == 'stat_orbs':
            self.w = 80
            self.h = 120
            self.x = 600
            self.y = 70
        
        if area =='digit':
            self.w = 7
            self.h = 10
            self.x = 609
            self.y = 119
        
        if area == 'health_orb':
            self.w = 43
            self.h = 27
            self.x = 1447
            self.y = 164

        if area == 'prayer_orb':
            self.w = 41
            self.h = 28
            self.x = 1447
            self.y = 238
        
        if area == 'special_orb':
            self.w = 43
            self.h = 28
            self.x = 1517
            self.y = 360

        if area == 'run_orb':
            self.w = 46
            self.h = 30
            self.x = 1470
            self.y = 305
        
        if area == 'map':
            self.w = 976
            self.h = 641
            self.x = 274
            self.y = 98
        
        if area == 'stats':
            self.w = 406
            self.h = 560
            self.x = 1389
            self.y = 474
        
        if area == 'inv1':
            self.w = 50
            self.h = 44
            self.x = 735
            self.y = 271
            
        if area == 'left_inventory':
            self.w = 426    
            self.h = 579
            self.x = 113
            self.y = 468

        
  

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
        img = np.fromstring(signedIntsArray, dtype='uint8')
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

    def get_screen_position(self, pos):
        return (pos[0] + self.x, pos[1] + self.y)
