from numpy.core.multiarray import empty
from pandas.core.indexes.base import Index
from sqlalchemy import true
from webwalking import WebWalking
from vision import Vision
from hsvfilter import HsvFilter
from windowcapture import BankRegion, ChatboxRegion, CustomRegion, InventoryRegion, PlayerRegion, ScreenRegion
from numpy import array
from wikiapi import Price
import time
import random

to_rockfall = WebWalking('walking_lists\\motherlode1.pkl','map\\motherlode2.png',orientation='West')
to_rocks = WebWalking('walking_lists\\to_rocks.pkl','map\\motherlode2.png',orientation='West')
to_left = WebWalking('walking_lists\\to_left.pkl','map\\motherlode2.png',orientation='West')
to_right = WebWalking('walking_lists\\to_right.pkl','map\\motherlode2.png',orientation='West')
to_water1 = WebWalking('walking_lists\\to_bank_mlm.pkl','map\\motherlode2.png',orientation='West')
to_water2 = WebWalking('walking_lists\\to_bank_mlm2.pkl','map\\motherlode2.png',orientation='West')
to_sack = WebWalking('walking_lists\\to_bank_bag.pkl','map\\motherlode2.png',orientation='West')
to_bank = WebWalking('walking_lists\\to_deposit_mlm.pkl','map\\motherlode2.png',orientation='West')

hopper_region = ([(929,475,82,60)])

veins_filter = HsvFilter(vAdd=65)
sack_filter = HsvFilter(sAdd=165, vAdd=155)

upper_half = CustomRegion(1500,539,7,38)
player_region = CustomRegion(804,346,254,347)
mining_region = CustomRegion(215,229,852,299)
sack_count_region = CustomRegion(181,179,115,103)
depost_box_region = CustomRegion(870, 601, 372, 420)
player = PlayerRegion()
inventory = InventoryRegion()
screen = ScreenRegion()
bank = BankRegion()
chatbox = ChatboxRegion()

sack = Vision('Needle\\motherlode\\sack.png',sack_filter)
zero = Vision('Needle\\motherlode\\zero_ore.png')
deposit = Vision('Needle\\motherlode\\deposit.png')
hopper = Vision('Needle\\motherlode\\hopper.png')
rockfall_v = Vision('Needle\\motherlode\\rockfall1.png')
rockfall_v2 = Vision('Needle\\motherlode\\rockfall2.png')
congrats = Vision('Needle\\motherlode\\congrats.png')
inv_full = Vision('Needle\\motherlode\\inv_full.png')
coal = Vision("Needle\\motherlode\\coal.png")
deposit_checker = Vision('Needle\\motherlode\\deposit_checker.png')
deposit_items = [Vision("Needle\\motherlode\\coal.png"),Vision("Needle\\motherlode\\gold_ore.png"),Vision("Needle\\motherlode\\iron_ore.png"),Vision("Needle\\motherlode\\mithril_ore.png"),Vision("Needle\\motherlode\\gold_nugget.png")]
veins = [Vision('Needle\\motherlode\\right_vein.png',veins_filter), Vision('Needle\\motherlode\\middle_vein.png',veins_filter), Vision('Needle\\motherlode\\left_vein.png',veins_filter)]


player.is_animating()

while True:
    keep_mining = True
    to_rockfall.walk(within=3)
    time.sleep(1)
    try:
        screen.click(rockfall_v,0.8,timeout=0.5)
        time.sleep(6)
    except IndexError:
        pass
    to_rocks.walk(within=3)
    right = True

    while keep_mining == True:
        try:
            t = upper_half.click_list(veins, 0.8, timeout=0.5)
            time.sleep(3)
        except IndexError:
            if to_right.end_of_path(within=4) == True:
                right = False
            if right == True:
                to_right.walk_once(dist=60)
            if to_left.end_of_path(within=4) == True:
                right = True
            if right == False:
                to_left.walk_once(dist=60)
        while mining_region.contains(t,0.75,40):
            if chatbox.contains(inv_full):
                keep_mining = False
                break
            if player.is_animating() == False:
                break
            if chatbox.contains(congrats):
                break
            pass
    to_water1.walk(within=2)
    try:
        screen.click(rockfall_v2,0.85)
        time.sleep(2.5)
    except IndexError:
        pass
    to_water2.walk(within=2)
    counter = 0
    while inventory.is_full() > 15:
        counter += 1
        screen.click(hopper,0.8)
        time.sleep(2)
        if counter > 3:
            break

    if sack_count_region.contains(zero):
        pass
    else:
        to_sack.walk(within=3)
        screen.click(sack,0.85,timeout=15)
        inventory.wait_for(coal)
        to_bank.walk(within=3)
        time.sleep(0.3)
        screen.click(deposit,0.7)
        depost_box_region.wait_for(deposit_checker)
        for item in deposit_items:
            try:
                depost_box_region.click(item,timeout = 0.01)
            except IndexError:
                pass
            time.sleep(0.25)


