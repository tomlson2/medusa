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
iron_ore = Vision('Needle\\iron_ore.png')
take_bars = Vision('Needle\\make_steel.png')
steel_bar = Vision('Needle\\steel_bar.png')

belt = array([(1079,582,110,105)])
dispenser = array([(1074,512,133,121)])

def anticheat_sleep():
    time.sleep(random.normalvariate(0.7,0.1))

def empty_bag():
    inventory.click(coal_bag,1,right_click=True)
    screen.click(empty_cb,1)
    anticheat_sleep()

def fill_bag():
    inventory.click(coal_bag,1,right_click=True)
    screen.click(fill_cb,1)


# while True:
#     print(Player().bank_number())

while True:
    chest.findbank()
    fill_bag()
    anticheat_sleep()
    chest.withdraw(iron_ore,1)
    chest.close()
    to_belt.walk()
    screen.click_region(belt)
    anticheat_sleep()
    empty_bag()
    anticheat_sleep()
    screen.click_region(belt)
    to_dispenser.walk()
    anticheat_sleep()
    screen.click_region(dispenser)
    anticheat_sleep()
    chatbox.click(take_bars,.9)
    to_bank.walk()
    chest.findbank()
    chest.deposit(steel_bar,0.7)


