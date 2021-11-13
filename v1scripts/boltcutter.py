import pyautogui
import time
import random
from bank import Bank
from vision import Vision
from windowcapture import WindowCapture

'''
SCRIPT SHOULD CURRENTLY WORK IN GE NE BANK BOOTH
CAMERA UP FACING NORTH 
ZOOM FULL IN
diamonds, chisel
'''

# initializing all of the WindowCapture() objects (screen regions) that will be called
screen = WindowCapture()
inventory = WindowCapture(area='inventory')
bank = WindowCapture(area='bank')
chatbox = WindowCapture(area='chatbox')
sidebar_r = WindowCapture(area='sidebar_r')

# intializing the Vision() objects (matches/items) that will be called
chisel = Vision('Needle\\chisel.png')
diamond = Vision('Needle\\diamond.png')
make = Vision('Needle\\make_diamond_tips.png')

# TODO STILL NEED TO ADD CHECKS FOR INVENTORY BEING OPEN

# starts beginning time so we can calculate current time by subtracting this
start_time = time.time()
run_time = random.randint(600, 820)
break_time = random.randint(42, 142)


while True:

    # check inventory for script items

    # if chisel match is found in inventory...
    if chisel.match(inventory.get_screenshot(),0.40)[0] == True:
        print("chisel in inventory")
    else:
        booth = Bank('Needle\\ge_bank_booth.png')
        booth.withdraw(chisel)
        time.sleep(random.uniform(0.36,1.23))
    # if maple log match is found in inventory...
    if diamond.match(inventory.get_screenshot(),0.8)[0] == True:
        print("gem in inventory")
    else:
        # now check if maple shortbow(u) is in inventory...
        # making sure we deposit the strung bows before trying to grab logs. This could be at the end of the script
        # but I believe it is better and more efficient to have it at the beginning, allowing script to start with 
        # full inv of finished items.
        # if bow.match(inventory.get_screenshot(),0.4)[0] == True:
        #     booth = Bank('Needle\\bankchest.png')
        #     booth.deposit(bow)
        #     time.sleep(random.uniform(0.3,1.2))
        booth = Bank('Needle\\ge_bank_booth.png')
        booth.withdraw(diamond)
        time.sleep(random.normalvariate(0.74, 0.14))
    
    # checking if bank has been accessed (checking existence of Bank() object booth) to know whether or not
    # it needs to be closed.
    try:
        booth
    except NameError:
        print("Inventory ready")
    else:
        booth.close()
    time.sleep(random.uniform(0.3,1.2))
    
    #  TODO find a way to do chisel.click(inventory.get_screenshot())... 
    # need to change up Vision and WindowCaputer methods

    # click the chisel in the inventory
    rectangles = chisel.find(inventory.get_screenshot(),0.40)
    points = chisel.get_click_points(rectangles)
    point = inventory.get_screen_position(points[0])
    pyautogui.click(point[0],point[1])
    time.sleep(random.normalvariate(0.71, 0.11))

    # click the diamonds in the inventory
    rectangles = diamond.find(inventory.get_screenshot(),0.80)
    points = chisel.get_click_points(rectangles)
    point = inventory.get_screen_position(points[0])
    pyautogui.click(point[0],point[1])
    time.sleep(random.normalvariate(0.6, 0.08))

    # waits for fletching interface to show up in chatbox
    while make.match(chatbox.get_screenshot(),0.7)[0] == False:
        print('Waiting for interface...')
        time.sleep(0.5)
    
    # clicks the make bolt tip object in the chat interface
    rectangles = make.find(chatbox.get_screenshot(),0.7)
    points = chisel.get_click_points(rectangles)
    point = chatbox.get_screen_position(points[0])
    pyautogui.click(point[0],point[1])

    # checks to make sure logs are still in inventory (this assumes that it is fletching)
    # TODO add level up handler
    
    # TODO check that the number of logs in the inventory is going down with time, this would not only solve level handler but also other issues in case it stops fletching
    print('Fletching...')
    while diamond.match(inventory.get_screenshot(), 0.81)[0] == True:
        time.sleep(random.uniform(0.6,1.8))
    time.sleep(random.uniform(0.4, 0.95))

    # gets current time
    current_time = (time.time() - start_time)
    current_time_format = time.strftime("%H:%M:%S", time.gmtime(current_time))
    print(f"run time: {current_time_format}")

    # break handler
    if current_time > run_time:
        print(f"breaking for {break_time} seconds")
        time.sleep(break_time)
        # randomize the run time and break time again
        run_time = random.randint(650, 1540)                                                                                                                
        break_time = random.randint(22, 82)
        # resets the run time
        run_time += current_time

    # end