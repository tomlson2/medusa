from vision import Vision
from player import Player
from bank import Bank
from windowcapture import BankRegion, ChatboxRegion, InventoryRegion, ScreenRegion
from numpy import array
import time
import random

inventory = InventoryRegion()
screen = ScreenRegion()
bank = BankRegion()
chatbox = ChatboxRegion()

booth = Bank('Needle\\bf_v2\\bank.png')

player = Player()

iron_bar = Vision('Needle\\aio_anvil\\iron_bar.png')
iron_platebody = Vision('Needle\\aio_anvil\\iron_platebody_inv.png')
make_iron_platebody = Vision('Needle\\aio_anvil\\iron_platebody.png')
smithing_level_up = Vision('Needle\\aio_anvil\\smithing_level_up.png')
tap_here = Vision('Needle\\aio_anvil\\tap_here.png')


anvil_region = array([(1123,1081,25,23)])
bank_region = array([(875,207,20,30)])
anvil_close_region = array([(956,606,18,27)])

while True:
    booth.withdraw(iron_bar,1)
    screen.click_region(anvil_region)
    screen.wait_for(make_iron_platebody)
    screen.click(make_iron_platebody,1)
    while inventory.contains(iron_bar):
        if chatbox.contains(smithing_level_up, 0.9):
            screen.click_region(anvil_close_region)
            screen.wait_for(make_iron_platebody)
            screen.click(make_iron_platebody)
        else:
            pass
    while chatbox.contains(tap_here):
        chatbox.click(tap_here)
        time.sleep(random.normalvariate(0.6,0.05))
    screen.click_region(bank_region)
    screen.wait_for(Vision('Needle\\inventory_guy.png'))
    booth.deposit(iron_platebody,1)
    