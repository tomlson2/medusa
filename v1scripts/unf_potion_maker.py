import win32gui
import pyautogui
import time
import random
from bank import Bank
from vision import Vision
from windowcapture import WindowCapture

'''
makes unf potion 
no other vials/potions visible in bank screen
'''

# initializing all of the WindowCapture() objects (screen regions) that will be called
screen = WindowCapture()
inventory = WindowCapture(area='inventory')
bank = WindowCapture(area='bank')
chatbox = WindowCapture(area='chatbox')
sidebar_r = WindowCapture(area='sidebar_r')

# initialize vision objects
ranarr = Vision('Needle\\toadflax.png')
water = Vision('Needle\\vial_of_water.png')
make = Vision('Needle\\make_toadflax_potion.png')
wine = Vision('Needle\\wine.png')
deposit = Vision('Needle\\deposit_inventory.png')


start_time = time.time()
run_time = random.randint(600, 820)
break_time = random.randint(42, 142)


while(True):
    if ranarr.match(inventory.get_screenshot(), 0.65)[0] == True:
        print("Ranarr(s) in inventory")
    else:
        booth = Bank('Needle\\ge_bank_booth.png')
        booth.withdraw(deposit)
        time.sleep(random.normalvariate(0.6, 0.13))
        booth.withdraw(ranarr)
        time.sleep(random.normalvariate(0.86, 0.11))
        booth.withdraw(water)
        time.sleep(random.uniform(0.55,1.2))

    # if water.match(inventory.get_screenshot(), 0.5)[0] == True:
    #     print("Water vial(s) in inventory")
    # else:
    #     booth = Bank('Needle\\ge_bank_booth.png')
    #     booth.withdraw(water)

    try:
        booth
    except NameError:
        print("Inventory ready")
    else:
        booth.close()
    time.sleep(random.uniform(0.3,1.2))

    # click the knife in the inventory
    rectangles = ranarr.find(inventory.get_screenshot(),0.6)
    points = ranarr.get_click_points(rectangles)
    point = inventory.get_screen_position(points[-1])
    pyautogui.click(point[0],point[1])
    time.sleep(random.normalvariate(0.56, 0.11))

    # click the logs in the inventory
    rectangles = water.find(inventory.get_screenshot(),0.65)
    points = water.get_click_points(rectangles) 
    point = inventory.get_screen_position(points[0])
    pyautogui.click(point[0],point[1])
    time.sleep(random.uniform(0.4, 1.11))

    # waits for interface to show up in chatbox
    while make.match(chatbox.get_screenshot(),0.7)[0] == False:
        print('Waiting for interface...')
        time.sleep(0.45)

    # clicks the make unfinished potion object in the chat interface
    rectangles = make.find(chatbox.get_screenshot(),0.7)
    points = make.get_click_points(rectangles)
    point = chatbox.get_screen_position(points[0])
    pyautogui.click(point[0],point[1])

    print('Making unf potions...')
    while ranarr.match(inventory.get_screenshot(), threshold=0.7)[0] == True:
        time.sleep(random.uniform(0.6, 1.8))
    time.sleep(random.uniform(0.551,1.8))

    # gets current time
    current_time = (time.time() - start_time)
    print(f"run time: {(round(current_time, 2))} seconds")

    # break handler
    if current_time > run_time:
        print(f"breaking for {break_time} seconds")
        time.sleep(break_time)
        # randomize the run time and break time again
        run_time = random.randint(661, 840)
        break_time = random.randint(33, 101)
        # resets the run time
        run_time += current_time
