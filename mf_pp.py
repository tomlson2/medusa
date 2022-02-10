import time
import random
from turtle import Screen
from vision import Vision
from windowcapture import ScreenRegion

screen = ScreenRegion()

mf0 = Vision('Needle\\thieving\\mf\\mf0.png')

while True:
    if screen.contains(mf0):
        screen.click(mf0)
        time.sleep(0.3)
    pass