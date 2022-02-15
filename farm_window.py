import win32gui, win32api, win32ui, win32con
import cv2 as cv
import numpy as np
import time

wins = []
def winEnumHandler(hwnd, ctx):
    if win32gui.IsWindowVisible(hwnd):
        if win32gui.GetWindowText(hwnd).__contains__('Stacks'):
            wins.append(win32gui.GetWindowText(hwnd))

win32gui.EnumWindows(winEnumHandler, None)

while True:
    images = []
    for win in wins:
        hwnd = win32gui.FindWindow(None, win)
        window_rect = win32gui.GetWindowRect(hwnd)
        w = window_rect[2] - window_rect[0]
        h = window_rect[3] - window_rect[1]
        if h != 1112:
            win32gui.MoveWindow(hwnd, 0, 0, 1920, 1112, True)
        wDC = win32gui.GetWindowDC(hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (w, h), dcObj, (1, 33), win32con.SRCCOPY)

        # convert the raw data into a format opencv can read
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.frombuffer(signedIntsArray, dtype='uint8')
        img.shape = (h, w, 4)

        # free resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        img = img[...,:3]

        img = np.ascontiguousarray(img)
        resized = cv.resize(img, (0,0), fx=0.4,fy=0.4)
        images.append(resized)
        time.sleep(0.5)

    image_num = 0
    for im in images:
        if image_num == 0:
            grouped = im
        else:
            grouped = np.concatenate((grouped, im))
        image_num += 1
    
    cv.imshow('all', grouped)

    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break 
