from numpy import empty, ndarray
from webwalking import WebWalking
from vision import Vision
from player import Player
from bank import Bank
from interactions import Interactions
from numpy import array
import time
import random

inventory = Interactions(area='inventory')
screen = Interactions()
bank = Interactions(area='bank')
chatbox = Interactions(area='chatbox')

to_belt = WebWalking('walking_lists\\tobelt.pkl','map\\bf.png')
to_bank = WebWalking('walking_lists\\bank.pkl','map\\bf.png')
to_dispenser = WebWalking('walking_lists\\dispenser.pkl','map\\bf.png')

chest = Bank('Needle\\bchest.png', stam = True)

player = Player()

#chest = Vision('Needle\\bchest.png')
coal_bag = Vision('Needle\\cb.png')
coal = Vision('Needle\\coal.png')
fill_cb = Vision('Needle\\fcb.png')
empty_cb = Vision('Needle\\ecb.png')
adamant_ore = Vision('Needle\\adamant_ore.png')
make_bars = Vision('Needle\\make_adamant.png')
addy_bar = Vision('Needle\\addy_bar.png')


belt = array([(1097,569,65,58)])
dispenser = array([(1090,529,106,93)])

bars = 0

def anticheat_sleep():
    time.sleep(random.normalvariate(0.2,0.02))

def click_sleep():
    time.sleep(random.normalvariate(0.1,0.01))

def empty_bag():
    inventory.click(coal_bag,1,right_click=True)
    screen.click(empty_cb,1)
    inventory.wait_for(coal)

def fill_bag():
    chest.findbank()
    inventory.click(coal_bag,1,right_click=True)
    screen.click(fill_cb,1)
    click_sleep()

def put_ore_on():
    if inventory.contains(coal,0.7) or inventory.contains(adamant_ore,0.7):
        screen.click_region(belt)
        click_sleep()
        empty_bag()
        screen.click_region(belt)
        click_sleep()
    # if inventory.contains(coal,0.7) or inventory.contains(adamant_ore,0.7):
    #     if to_belt.end_of_path() == True:
    #         screen.click_region(belt)
    #     else:
    #         to_belt.walk()
    #         screen.click_region(belt)

def take_bars():
    screen.click_region(dispenser)
    try:
        chatbox.wait_for(make_bars)
        chatbox.click(make_bars,0.8)
    except IndexError:
        to_dispenser.walk()
        screen.click_region(dispenser)
        chatbox.click(make_bars,0.8)

start = time.time()

while True:
    while to_bank.end_of_path(within=2) == False:
        to_bank.walk(within=2)
    chest.withdraw(adamant_ore, 1)
    click_sleep()
    fill_bag()
    click_sleep()
    to_belt.walk()
    put_ore_on()
    while to_bank.end_of_path(within=2) == False:
        to_bank.walk(within=2)
    chest.withdraw(coal, 1)
    click_sleep()
    fill_bag()
    click_sleep()
    to_belt.walk()
    put_ore_on()
    to_dispenser.walk()
    take_bars()
    while to_bank.end_of_path(within=2) == False:
        to_bank.walk(within=2)
    bars = bars + inventory.amount(addy_bar,0.7)
    print(time.strftime("%H:%M:%S. ", time.gmtime(time.time()-start)) + str(bars) + " bars made. " + str(round((bars/(time.time()-start)*3600))) + " bars/hour")
    chest.deposit(addy_bar,1)
        

        
