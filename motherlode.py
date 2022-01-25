from numpy.core.multiarray import empty
from pandas.core.indexes.base import Index
from webwalking import WebWalking
from vision import Vision
from player import Player
from bank import Bank
from windowcapture import BankRegion, ChatboxRegion, CustomRegion, InventoryRegion, ScreenRegion
from numpy import array
from wikiapi import Price
import time
import random


player_region = CustomRegion(804,346,254,347)
mining_region = CustomRegion(867,345,148,180)
inventory = InventoryRegion()
screen = ScreenRegion()
bank = BankRegion()
chatbox = ChatboxRegion()

veins = [Vision('Needle\\motherlode\\right_vein.png'), Vision('Needle\\motherlode\\middle_vein.png'), Vision('Needle\\motherlode\\left_vein.png')]

t = player_region.click_list(veins, 0.8)
time.sleep(3)

while mining_region.contains(t,0.8):
    print("True")

print('False')