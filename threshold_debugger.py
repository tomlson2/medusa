from turtle import Screen
import cv2 as cv
from hsvfilter import HsvFilter
from windowcapture import InventoryRegion, PlayerRegion, RunOrb, ScreenRegion, ShopRegion, WindowCapture, CustomRegion
from vision import Vision
import numpy as np

wincap = ScreenRegion()
needle_path = 'Needle\\sandcrab\\strength4.png'
scale = 0.5
vision = Vision(needle_path, scale = 0.5)
window_name = "Threshold"

def nothing(position):
    pass
needle = 'Needle\\sandcrab\\strength4.png'


vision = Vision(needle)

vision.init_control_gui()

def init_trackbars():
    cv.namedWindow(window_name, cv.WINDOW_NORMAL)
    cv.createTrackbar('Match Threshold', window_name, 85, 100, nothing)
    cv.createTrackbar('Blur', window_name, 10, 100, nothing)
    cv.createTrackbar('Edge Detection', window_name, 1, 1, nothing)
    cv.createTrackbar('Edge Thresh1', window_name, 0, 200, nothing)
    cv.createTrackbar('Edge Thresh2', window_name, 0, 200, nothing)
    cv.getTrackbarPos('Match Threshold', window_name) * .01

def blur(img):
    blur_val = (cv.getTrackbarPos('Blur', window_name))
    if (blur_val % 2) == 0:
        blur_val -= 1 
    if blur_val > 1:
        img = cv.GaussianBlur(img, (blur_val, blur_val), cv.BORDER_DEFAULT)
    return img

def edge_detection(img):
    if cv.getTrackbarPos('Edge Detection', window_name) > 0:
        edge1 = cv.getTrackbarPos('Edge Thresh1', window_name)
        edge2 = cv.getTrackbarPos('Edge Thresh2', window_name)
        gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        canned_img = cv.Canny(gray_img, edge1, edge2)
        return canned_img
    else:
        return img

def edit_image(img):
    img = edge_detection(img)
    img = blur(img)
    return img

def testing():
    object_detector = cv.createBackgroundSubtractorMOG2(history=20, varThreshold=10)
    while True:
        found = False
        im = ScreenRegion().get_screenshot()
        im = vision.apply_hsv_filter(im, vision.get_hsv_filter_from_controls())
        mask = object_detector.apply(im)
        contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        stencil = np.zeros(im.shape).astype(im.dtype)
        cv.fillPoly(stencil, contours, [255, 255, 255])
        for cnt in contours:
            area = cv.contourArea(cnt)
            if area > 1000:
                x, y, w, h = cv.boundingRect(cnt)
                cv.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv.imshow('test',im)

        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            break 

        print('Done.')

init_trackbars()
testing()
# while True:
#     threshold = (cv.getTrackbarPos('Match Threshold', window_name) * .01)
#     hsv_filter1 = vision.get_hsv_filter_from_controls()
#     needle = Vision(needle_path, hsv_filter=hsv_filter1)
#     screenshot = wincap.get_screenshot()
#     screenshot = vision.apply_hsv_filter(screenshot,hsv_filter=hsv_filter1)
#     og = screenshot.copy()
#     # edited_needle = edit_image(needle.get_image())
#     # edited_image = edit_image(screenshot)
#     # scaled_img = cv.resize(screenshot,(0,0))
#     rectangles = needle.find(screenshot, threshold=threshold)
#     edited_image = vision.draw_rectangles(screenshot,rectangles=rectangles)
#     edited_image = cv.putText(edited_image,"Threshold = " + str(round(threshold,4)),(50,40),cv.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
#     edited_image = cv.putText(edited_image,"Matches = " + str(len(rectangles)),(50,85),cv.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
#     # edited_image = cv.adaptiveThreshold(edited_image,255,1,1,11,2)
#     # contours, _ = cv.findContours(edited_image, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
#     # edited_image = cv.cvtColor(edited_image, cv.COLOR_GRAY2BGR)
#     # for cnt in contours:
#     #     area = cv.contourArea(cnt)
#     #     if area > 25:
#     #         x, y, w, h = cv.boundingRect(cnt)
#     #         cv.rectangle(edited_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
#     # cv.drawContours(edited_image,contours,-1, (0, 255, 0), 2)
#     cv.imshow('needle', needle.get_image())
#     cv.imshow('canny', edited_image)
    
        
#     if cv.waitKey(1) == ord('q'):
#         cv.destroyAllWindows()
#         break 

# print('Done.')