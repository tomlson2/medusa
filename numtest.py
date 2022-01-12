from ocr import Numbers
import cv2 as cv

num = Numbers()

word = num.number(cv.imread("fonts\\numberstest.png"))
print(word)