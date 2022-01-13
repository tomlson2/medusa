import cv2 as cv
from vision import Vision
from hsvfilter import HsvFilter
import numpy as np
from player import Player
from ocr import Ocr
from interactions import Interactions

# imagergb = cv.imread('fonts2/ff.png')
# #converting the image to HSV color space using cvtColor function
# imagehsv = cv.cvtColor(imagergb, cv.COLOR_BGR2HSV)
# #defining the lower threshold and upper threshold for a range of black color in HSV
# lower_black = np.array([26, 215, 150])
# upper_black = np.array([30,255,250])
# #masking the HSV image to get only black colors
# imagemask = cv.inRange(imagehsv, lower_black, upper_black)
# #displaying the resulting HSV image with only black colors masked
# cv.imwrite("fonts2/result.png", imagemask)

ocr = Ocr('samples/bold12lowersamples.data','responses/bold12lowerresponses.data')
print(ocr.number(cv.imread('fonts2/resi.png')))

# vision = Vision('fonts2/booth.png')
# screen = Interactions()

# screen.click(vision)
