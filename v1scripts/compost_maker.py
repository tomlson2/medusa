import cv2 as cv
from hsvfilter import HsvFilter
import win32gui
import pyautogui
import time
import random
from bank import Bank
from vision import Vision
from windowcapture import WindowCapture
'''
makes ultra compost ~400k gp/hr
full zoom at ne ge bank booth, full uptilt, north camera

'''

# initializing all of the WindowCapture() objects (screen regions) that will be called
screen = WindowCapture()
inventory = WindowCapture(area='inventory')
bank = WindowCapture(area='bank')
chatbox = WindowCapture(area='chatbox')
sidebar_r = WindowCapture(area='sidebar_r')

# intializing the Vision() objects (matches/items) that will be called
ash = Vision('Needle\\volcanic_ash.png')
supercompost = Vision('Needle\\supercompost.png')
make = Vision('Needle\\make_compost.png')
ultra_compost = Vision('Needle\\ultracompost.png')
supercompost_bank = Vision('Needle\\supercompost_bank.png')
supercompost_image = 'Needle\\supercompost.png'

# hsv filtering to differentiate supercompost from ultracompost
supercompost_filter = HsvFilter(hMax=30, sMax=251, sAdd=55, sSub=69, vAdd=149)
edited_needle = cv.imread(supercompost_image)
supercompost_edited = supercompost.apply_hsv_filter(edited_needle, supercompost_filter)
final_supercompost = Vision(supercompost_edited, edited=True)
screenshot = inventory.get_screenshot()
adjusted_screenshot = final_supercompost.apply_hsv_filter(screenshot, supercompost_filter)

# TODO STILL NEED TO ADD CHECKS FOR INVENTORY BEING OPEN

# starts beginning time so we can calculate current time by subtracting this
start_time = time.time()
run_time = random.randint(600, 820)
break_time = random.randint(42, 142)


while True:

    # check inventory for script items
    # if ash match is found in inventory...
    if ash.match(inventory.get_screenshot(),0.40)[0] == True:
        print("ash in inventory")
    else:
        booth = Bank('Needle\\ge_bank_booth.png')
        booth.withdraw(ash)
        time.sleep(random.uniform(0.5, 0.8))


    # if maple log match is found in inventory...
    if final_supercompost.match(final_supercompost.apply_hsv_filter(inventory.get_screenshot(), supercompost_filter), 0.75)[0] == True:
        print("compost in inventory")
    else:
        # now check if maple shortbow(u) is in inventory...
        # making sure we deposit the strung bows before trying to grab logs. This could be at the end of the script
        # but I believe it is better and more efficient to have it at the beginning, allowing script to start with 
        # full inv of finished items.
        if ultra_compost.match(inventory.get_screenshot(),0.4)[0] == True:
            booth = Bank('Needle\\ge_bank_booth.png')
            booth.deposit(ultra_compost)
            print("bug")
            time.sleep(random.uniform(0.84,0.97))
            print('check')
        booth = Bank('Needle\\ge_bank_booth.png')
        booth.withdraw(supercompost_bank)
        time.sleep(random.normalvariate(0.5,0.05))


    # checking if bank has been accessed (checking existence of Bank() object booth) to know whether or not
    # it needs to be closed.
    try:
        booth
    except NameError:
        print("Inventory ready")
    else:
        booth.close()
    time.sleep(random.normalvariate(0.46,0.05))


    # click the ash in the inventory
    rectangles = ash.find(inventory.get_screenshot(),0.60)
    points = ash.get_click_points(rectangles)
    point = inventory.get_screen_position(points[0])
    pyautogui.click(point[0],point[1])
    time.sleep(random.normalvariate(0.65,0.12))

    # click the compost in the inventory
    screenshot = inventory.get_screenshot()
    adjusted_screenshot = final_supercompost.apply_hsv_filter(screenshot, supercompost_filter)
    rectangles = final_supercompost.find(adjusted_screenshot, 0.70)
    points = final_supercompost.get_click_points(rectangles)
    point = inventory.get_screen_position(points[0])
    pyautogui.click(point[0],point[1])
    time.sleep(random.uniform(0.5,1.0))

    # waits for compost interface to show up in chatbox
    while make.match(chatbox.get_screenshot(),0.7)[0] == False:
        print('Waiting for interface...')
        time.sleep(0.5)
    
    # clicks the make compost object in the chat interface
    rectangles = make.find(chatbox.get_screenshot(),0.7)
    points = make.get_click_points(rectangles)
    point = chatbox.get_screen_position(points[0])
    pyautogui.click(point[0],point[1])

    # checks to make sure super compost are still in inventory (this assumes that it is making compost)
    print('Making compost...')
    # massive line of code that condenses screenshotting and filtering to one line for the while loop

    while final_supercompost.match(final_supercompost.apply_hsv_filter(inventory.get_screenshot(), supercompost_filter), 0.75)[0] == True:
        time.sleep(random.uniform(0.6, 1.8))
    time.sleep(random.normalvariate(0.84, 0.21))

    # gets current time
    current_time = (time.time() - start_time)
    current_time_format = time.strftime("%H:%M:%S", time.gmtime(current_time))
    print(f"run time: {current_time_format}")

    # break handler
    if current_time > run_time:
        print(f"breaking for {break_time} seconds")
        time.sleep(break_time)
        # randomize the run time and break time again
        run_time = random.randint(600, 940)
        break_time = random.randint(32, 112)
        # resets the run time
        run_time += current_time
