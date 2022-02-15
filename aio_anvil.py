from msilib.schema import CustomAction
from vision import Vision
from player import Player
from bank import Bank
from windowcapture import BankRegion, ChatboxRegion, InventoryRegion, ScreenRegion, CustomRegion
from numpy import array
import time
import random

inventory = InventoryRegion()
screen = ScreenRegion()
bank = BankRegion()
chatbox = ChatboxRegion()
make_region = CustomRegion(1066, 680, 271, 378)

booth = Bank('Needle\\bf_v2\\bank.png')

player = Player()

iron_bar = Vision('Needle\\aio_anvil\\iron_bar.png')
iron_platebody = Vision('Needle\\aio_anvil\\iron_platebody_inv.png')
steel_platebody = Vision('Needle\\aio_anvil\\steel_platebody.png')
steel_bar = Vision('Needle\\aio_anvil\\steel_bar.png')
make_iron_platebody = Vision('Needle\\aio_anvil\\make_iron_platebody.png')
make_steel_platebody = Vision('Needle\\aio_anvil\\make_steel_plate.png')
make_steel_war = Vision('Needle\\aio_anvil\\make_steel_war.png')
make_iron_war = Vision('Needle\\aio_anvil\\make_iron_warhammer.png')
smithing_level_up = Vision('Needle\\aio_anvil\\smithing_level_up.png')
tap_here = Vision('Needle\\aio_anvil\\tap_here.png')
steel_warhammer = Vision('Needle\\aio_anvil\\steel_warh.png')
iron_warhammer = Vision('Needle\\aio_anvil\\iron_warhammer.png')


anvil_region = array([(1123,1081,25,23)])
bank_region = array([(885,220,12,12)])
anvil_close_region = array([(961,599,11,15)])


def iron_plate():
    while True:
        booth.withdraw(iron_bar,1)
        time.sleep(0.2)
        screen.click_region(anvil_region)
        make_region.wait_for(make_iron_platebody, t = 8)
        screen.click(make_iron_platebody,1)
        while inventory.amount(iron_bar) > 2:
            if chatbox.contains(smithing_level_up, 0.9):
                screen.click_region(anvil_close_region)
                make_region.wait_for(make_iron_platebody, t = 2)
                screen.click(make_iron_platebody)
        time.sleep(1.5)
        while chatbox.contains(tap_here):
            chatbox.click(tap_here)
            time.sleep(random.normalvariate(0.6,0.05))
        screen.click_region(bank_region)
        screen.wait_for(Vision('Needle\\inventory_guy.png'), t = 8)
        booth.deposit(iron_platebody,1)
    
def steel_war():
    while True:
        booth.withdraw(steel_bar,1)
        time.sleep(0.2)
        screen.click_region(anvil_region)
        make_region.wait_for(make_steel_war, t = 8)
        screen.click(make_steel_war,1)
        while inventory.contains(steel_bar):
            if chatbox.contains(smithing_level_up, 0.9):
                screen.click_region(anvil_close_region)
                make_region.wait_for(make_steel_war, t = 2)
                screen.click(make_steel_war)
        time.sleep(1.5)
        while chatbox.contains(tap_here):
            chatbox.click(tap_here)
            time.sleep(random.normalvariate(0.6,0.05))
        screen.click_region(bank_region)
        screen.wait_for(Vision('Needle\\inventory_guy.png'), t = 8)
        booth.deposit(steel_warhammer,1)

def anvil(bar, item, make):
    while True:
        booth.withdraw(bar,1)
        time.sleep(random.normalvariate(0.3,0.02))
        screen.click_region(anvil_region)
        time.sleep(1.5)
        if make_region.wait_for(make, threshold=.9, t = 10) == False:
            break
        else:
            print("Found!")
            time.sleep(random.normalvariate(0.6,0.02))
            make_region.click(make,0.9)
            print("Making")
        while inventory.contains(bar):
            if chatbox.contains(smithing_level_up, 0.9):
                screen.click_region(anvil_close_region)
                if make_region.wait_for(make, t = 2) == False:
                    break
                else:
                    make_region.click(make)
        random.normalvariate(1.5,0.1)
        while chatbox.contains(tap_here):
            chatbox.click(tap_here)
            time.sleep(random.normalvariate(0.6,0.05))
        screen.click_region(bank_region)
        if screen.wait_for(Vision('Needle\\inventory_guy.png'), t = 8) == False:
            break
        else:
            booth.deposit(item,1)



anvil(steel_bar, steel_platebody, make_steel_platebody)

#anvil(steel_bar, steel_warhammer, make_steel_war)