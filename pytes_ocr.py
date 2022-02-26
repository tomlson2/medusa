import cv2 as cv
import numpy as np
import pytesseract
from vision import Vision
from hsvfilter import HsvFilter
from image_tools import sharpen, concat_images, pad
from windowcapture import CustomRegion


class OCR():

    def __init__(self):
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        self.im = None
        self.vision = Vision()
        
    def process_image(self, im):
        im = self.vision.apply_hsv_filter(im, HsvFilter(vMin=141))
        gray_im = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
        final_im = sharpen(gray_im)
        return final_im

    def find_click_box(self, click_point) -> np.ndarray:

        search_w = 600
        search_h = 100
        search_x = click_point[0]
        search_y = click_point[1]

        box_region = None
        object_detector = cv.createBackgroundSubtractorMOG2(history=5, varThreshold=5)

        # check what side the click is on
        if click_point[0] > 963:
            search_x = search_x - search_w
        
        search_region = CustomRegion(search_w, search_h, search_x, search_y)

        for _ in range(500):
            im = search_region.get_screenshot()
            mask = object_detector.apply(im)
            contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                area = cv.contourArea(cnt)
                if area > 500:
                    x, y, w, h = cv.boundingRect(cnt)
                    if search_w > w > 250:
                        box_region = CustomRegion(w, h, x + search_x, y + search_y)
                        break
            if box_region is not None:
                break
        
        if box_region is None:
            return None
        else:
            im = box_region.get_screenshot()
            return im
    
    def read_click(self, click_point):
        im = self.find_click_box(click_point)
        if im is None:
            return "error"
        else:
            processed_im = self.process_image(im)
            res = self.ocr_result(processed_im)
            return res

    def ocr_result(self, im) -> str:
        text = pytesseract.image_to_string(im)
        return text

    def test_image(self, im):
        im = self.process_image(im)
        result = self.ocr_result(im)
        print(f'result: {result}')
        cv.imshow('im',im)
        cv.waitKey(0)
        cv.destroyAllWindows()

# images = []
# region = CustomRegion(36, 25, 1454, 486)

# for _ in range(3):
#     im = region.get_screenshot()
#     images.append(im)
#     region.x += 135

# concat_im = concat_images(images)
# padded_im = pad(im, 100, 100)


# OCR().test_image(padded_im)
