import win32gui
import pyautogui
import time
import random
from bank import Bank
from vision import Vision
from windowcapture import WindowCapture
'''

SCRIPT SHOULD CURRENTLY WORK IN CASTLE WARS BANK CHEST 
CAMERA UP FACING NORTH 
ZOOM OUT ON 2ND LEVEL FROM THE RIGHT
MAPLE LOGS, KNIFE, UNSTRUNG MAPLE BOWS

'''

# initializing all of the WindowCapture() objects (screen regions) that will be called
screen = WindowCapture()
inventory = WindowCapture(area='inventory')
bank = WindowCapture(area='bank')
chatbox = WindowCapture(area='chatbox')
sidebar_r = WindowCapture(area='sidebar_r')

# intializing the Vision() objects (matches/items) that will be called
knife = Vision('Needle\\knife.png')
mlog = Vision('Needle\\willowlog.png')
make = Vision('Needle\\make_shortbow.png')
bow = Vision('Needle\\maple_short.png')

# TODO STILL NEED TO ADD CHECKS FOR INVENTORY BEING OPEN


while True:

    # check inventory for script items

    # if knife match is found in inventory...
    if knife.match(inventory.get_screenshot(),0.5)[0] == True:
        print("Knife in inventory")
    else:
        booth = Bank('Needle\\bankchest.png')
        booth.withdraw(knife)
        time.sleep(random.uniform(0.3,1.2))
    # if maple log match is found in inventory...
    if mlog.match(inventory.get_screenshot(),0.65)[0] == True:
        print("Maple Logs in inventory")
    else:
        # now check if maple shortbow(u) is in inventory...
        # making sure we deposit the strung bows before trying to grab logs. This could be at the end of the script
        # but I believe it is better and more efficient to have it at the beginning, allowing script to start with 
        # full inv of finished items.
        if bow.match(inventory.get_screenshot(),0.4)[0] == True:
            booth = Bank('Needle\\bankchest.png')
            booth.deposit(bow)
            time.sleep(random.uniform(0.3,1.2))
        booth = Bank('Needle\\bankchest.png')
        booth.withdraw(mlog)
        time.sleep(random.uniform(0.3,1.2))
    
    # checking if bank has been accessed (checking existence of Bank() object booth) to know whether or not
    # it needs to be closed.
    try:
        booth
    except NameError:
        print("Inventory ready")
    else:
        booth.close()
    time.sleep(random.uniform(0.3,1.2))
    
    #  TODO find a way to do knife.click(inventory.get_screenshot())... 
    # need to change up Vision and WindowCaputer methods

    # click the knife in the inventory
    rectangles = knife.find(inventory.get_screenshot(),0.6)
    points = knife.get_click_points(rectangles)
    point = inventory.get_screen_position(points[0])
    pyautogui.click(point[0],point[1])
    time.sleep(random.uniform(0.3,1.2))

    # click the logs in the inventory
    rectangles = mlog.find(inventory.get_screenshot(),0.5)
    points = knife.get_click_points(rectangles)
    point = inventory.get_screen_position(points[0])
    pyautogui.click(point[0],point[1])
    time.sleep(random.uniform(0.3,1.2))

    # waits for fletching interface to show up in chatbox
    while make.match(chatbox.get_screenshot(),0.7)[0] == False:
        print('Waiting for interface...')
        time.sleep(0.5)
    
    # clicks the make unstrung bow object in the fletching interface
    rectangles = make.find(chatbox.get_screenshot(),0.7)
    points = knife.get_click_points(rectangles)
    point = chatbox.get_screen_position(points[0])
    pyautogui.click(point[0],point[1])

    # checks to make sure logs are still in inventory (this assumes that it is fletching)
    # TODO add level up handler
    # TODO check that the number of logs in the inventory is going down with time, this would not only solve level handler but also other issues in case it stops fletching
    while mlog.match(inventory.get_screenshot())[0] == True:
        print('Fletching...')
        time.sleep(0.5)
    time.sleep(random.uniform(0.3,1.2))



    