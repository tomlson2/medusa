from hsvfilter import HsvFilter
import time
import random
from interactions import Interactions
from bank import Bank
from vision import Vision
from windowcapture import WindowCapture

screen = Interactions()
inventory = Interactions(area='inventory')
bank = Interactions(area='bank')
chatbox = Interactions(area='chatbox')
sidebar_r = Interactions(area='sidebar_r')

wincap = WindowCapture()


supercompost_filter = HsvFilter(hMax=30, sMax=251, sAdd=55, sSub=69, vAdd=149)

# intializing the Vision() objects (matches/items) that will be called
ash = Vision('Needle\\volcanic_ash.png')
supercompost = Vision('Needle\\supercompost.png',hsv_filter=supercompost_filter)
make = Vision('Needle\\make_compost.png')
ultra_compost = Vision('Needle\\ultracompost.png')
supercompost_bank = Vision('Needle\\supercompost_bank.png',hsv_filter=supercompost_filter)

booth = Bank('Needle\\ge_bank_booth.png')

# while True:
#     screenshot = wincap.get_screenshot()
#     adjusted = vision.apply_hsv_filter(screenshot,hsv_filter=supercompost_filter)
#     cv.imshow('haystack.png',adjusted)
#     cv.imshow('needle.png',supercompost_bank.return_image())

#     if cv.waitKey(1) == ord('q'):
#         cv.destroyAllWindows()
#         break 


while True:

    if inventory.contains(ash, 0.4):
        pass
    else:
        booth.withdraw(ash)
        time.sleep(random.uniform(0.5, 0.8))

    if inventory.contains(supercompost):
        pass
    else:
        if inventory.contains(ultra_compost):
            booth.deposit(ultra_compost)
            time.sleep(random.uniform(0.5,0.8))
        booth.withdraw(supercompost_bank, 0.7)
        time.sleep(random.uniform(0.5,0.8))
    
    if booth.status() == True:
        booth.close()
    
    inventory.click(ash,0.4)
    inventory.click(supercompost)
    chatbox.wait_for(make)
    chatbox.click(make,0.8)

    while inventory.contains(supercompost):
        time.sleep(1)
