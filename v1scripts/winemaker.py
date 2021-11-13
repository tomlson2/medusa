import win32gui
import pyautogui
import time
import random
from bank import Bank
from vision import Vision
from windowcapture import WindowCapture

'''
makes wines ~450k xp/hr
full zoom at ne ge bank booth, full uptilt, north camera
no jugs of wines visible in bank screen
'''

# initializing all of the WindowCapture() objects (screen regions) that will be called
screen = WindowCapture()
inventory = WindowCapture(area='inventory')
bank = WindowCapture(area='bank')
chatbox = WindowCapture(area='chatbox')
sidebar_r = WindowCapture(area='sidebar_r')

# initialize vision objects
grape = Vision('Needle\\grape.png')
water = Vision('Needle\\jug_of_water.png')
make = Vision('Needle\\make_wine.png')
wine = Vision('Needle\\wine.png')
deposit = Vision('Needle\\deposit_inventory.png')

# time stuff
start_time = time.time()
run_time = random.randint(600, 760)
break_time = random.randint(23, 117)


while(True):
    if grape.match(inventory.get_screenshot(), 0.5)[0] == True:
        print("Grape(s) in inventory")
    else:
        booth = Bank('Needle\\bankchest.png')
        booth.withdraw(deposit)
        time.sleep(random.uniform(0.3,1.2))
        booth.withdraw(grape)
        time.sleep(random.normalvariate(0.52,.11))
        booth.withdraw(water)
        time.sleep(random.normalvariate(0.41, 0.12))

    # if water.match(inventory.get_screenshot(), 0.5)[0] == True:
    #     print("Water jug(s) in inventory")
    # else:
    #     booth = Bank('Needle\\ge_bank_booth.png')
    #     booth.withdraw(water)

    try:
        booth
    except NameError:
        print("Inventory ready")
    else:
        booth.close()
    time.sleep(random.uniform(0.38,1.23))

    # click the grape in the inventory
    rectangles = grape.find(inventory.get_screenshot(),0.6)
    points = grape.get_click_points(rectangles)
    point = inventory.get_screen_position(points[-1])
    pyautogui.click(point[0],point[1])
    time.sleep(random.uniform(0.35, 0.92))

    # click the water jugs in the inventory
    rectangles = water.find(inventory.get_screenshot(),0.65)
    points = water.get_click_points(rectangles) 
    point = inventory.get_screen_position(points[0])
    pyautogui.click(point[0],point[1])
    time.sleep(random.uniform(0.38, 1.21))

    # waits for wine making interface to show up in chatbox
    while make.match(chatbox.get_screenshot(),0.7)[0] == False:
        print('Waiting for interface...')
        time.sleep(0.6)

    # clicks the make wine object in the make interface
    rectangles = make.find(chatbox.get_screenshot(),0.7)
    points = grape.get_click_points(rectangles)
    point = chatbox.get_screen_position(points[0])
    time.sleep(random.normalvariate(0.5, 0.08))
    pyautogui.click(point[0],point[1])

    print('Making wine...')
    while grape.match(inventory.get_screenshot())[0] == True:
        time.sleep(random.uniform(0.6, 1.2))
    time.sleep(random.normalvariate(.94, .21))

    # gets current time
    current_time = (time.time() - start_time)
    current_time_format = time.strftime("%H:%M:%S", time.gmtime(current_time))
    print(f"run time: {current_time_format}")

    # break handler
    if current_time > run_time:
        print(f"breaking for {break_time} seconds")
        time.sleep(break_time)
        run_time = random.randint(600, 760)
        break_time = random.randint(23, 117)        
        # resets the run time for 
        run_time += current_time
