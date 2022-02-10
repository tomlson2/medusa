from numpy.core.multiarray import empty
from pandas.core.indexes.base import Index
from sqlalchemy import true
from webwalking import WebWalking
from vision import Vision
from hsvfilter import HsvFilter
from windowcapture import BankRegion, ChatboxRegion, CustomRegion, InventoryRegion, PlayerRegion, RunOrb, ScreenRegion
from model import Model
import time
import random

print("Initializing")

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
runorb = RunOrb()


rockfalls = Model('model_data/weights/rockfall.pt')

pay_dirt = Vision('Needle\\motherlode\\pay-dirt.png')
sack = Vision('Needle\\motherlode\\sack.png',sack_filter)
zero = Vision('Needle\\motherlode\\zero_ore.png')
deposit = Vision('Needle\\motherlode\\deposit.png')
hopper = Vision('Needle\\motherlode\\hopper.png')
rockfall_v = Vision('Needle\\motherlode\\rockfall1.png')
rockfall_v2 = Vision('Needle\\motherlode\\rockfall2.png')
congrats = Vision('Needle\\motherlode\\congrats.png')
inv_full = Vision('Needle\\motherlode\\inv_full.png')
coal = Vision("Needle\\motherlode\\coal.png")
gold_ore = Vision("Needle\\motherlode\\gold_ore.png")
mitrhil_ore = Vision("Needle\\motherlode\\mithril_ore.png")
gold_nugget = Vision("Needle\\motherlode\\gold_nugget.png")
gem1 = Vision("Needle\\motherlode\\gem1.png")
gem2 = Vision("Needle\\motherlode\\gem2.png")
gem3 = Vision("Needle\\motherlode\\gem3.png")
gem4 = Vision("Needle\\motherlode\\gem4.png")
deposit_checker = Vision('Needle\\motherlode\\deposit_checker.png')
deposit_items = [coal,gold_ore,mitrhil_ore,gold_nugget,gem1,gem2,gem3,gem4]
veins = [Vision('Needle\\motherlode\\right_vein.png',veins_filter), Vision('Needle\\motherlode\\middle_vein.png',veins_filter), Vision('Needle\\motherlode\\left_vein.png',veins_filter)]


print("Starting script")

def handle_rockfalls(walk):
    print("Rockfall handler...")
    num_falls = screen.amount(rockfalls, 0.4)
    while True:
        while screen.amount(rockfalls, 0.4) > 1:
            print("Clicking rockfall")
            screen.click(rockfalls,0.5,timeout=0.5)
            time.sleep(5)
        walk.walk_once(dist=105)
        if to_rocks.coords_change(threshold=3) == True:
            break

while True:
    keep_mining = True
    print("Toggling run")
    runorb.run()
    print("Walking to rockfall")
    to_rockfall.walk(within=4, ind_len=-2)
    time.sleep(1)
    handle_rockfalls(walk=to_rocks)
    print("Walking to mining area")
    to_rocks.walk(within=8, ind_len=-4)
    time.sleep(1)
    right = True
    print("Toggling walk")
    print("Begin mining")
    while keep_mining == True:
        while True:
            deadloop = 0
            try:
                t = upper_half.click_list(veins, 0.8, timeout=0.5)
                print("Clicked rock")
                time.sleep(3.5)
                break
            except IndexError:
                if deadloop > 5:
                    print("Didn't find any rocks after walking 5 times! breaking loop.")
                    break
                print("Didn't find rock, walking to find rock")
                if to_right.end_of_path(within=4) == True:
                    print("At the end of right walk, switching to left walk")
                    right = False
                if right == True:
                    print("Walking once right")
                    to_right.walk_once(dist=55)
                if to_left.end_of_path(within=4) == True:
                    print("At the end of left walk, switching to right")
                    right = True
                if right == False:
                    print("Walking once left")
                    to_left.walk_once(dist=55)
                time.sleep(random.normalvariate(1.75,0.08))
                deadloop += 1
        print("Mining! waiting for rock to disappear or animation to stop.")
        while mining_region.contains(t,0.75,40):
            if chatbox.contains(inv_full):
                keep_mining = False
                print("Inventory full! Must bank.")
                break
            if player.is_animating() == False:
                print("Player no longer animating! Looking for new rock.")
                break
            if chatbox.contains(congrats):
                print("Leveled up! Clicking rock again.")
                break
            pass
    print("Toggling Run")
    runorb.run()
    print("Walking to rockfall.")
    to_water1.walk(within=4,ind_len=-2)
    handle_rockfalls(walk=to_water2)
    print("Walking to hopper")
    to_water2.walk(within=5,ind_len=-2)
    counter = 0
    while inventory.is_full() > 15:
        deadloop = 0
        try:
            print("Clicking hopper")
            screen.click(hopper,0.8)
        except IndexError:
            print("Hopper not found, rewalking")
            if deadloop > 4:
                break
            to_water2.walk(within=1, ind_len=-2)
            time.sleep(1.0)
            deadloop += 1
        time.sleep(2.0)
    for _ in range(10):
        if inventory.contains(pay_dirt):
            time.sleep(0.5)
    if inventory.contains(pay_dirt):
        print("Couldn't put pay-dirt in hopper.")
        break
    if sack_count_region.contains(zero):
        print("Nothing to collect")
        pass
    else:
        deadloop = 0
        print("Walking to sack")
        to_sack.walk(within=3, ind_len=-2)
        time.sleep(0.5)
        while True:
            try:
                print("Clicking sack")
                screen.click(sack,0.75,timeout=30)
                break
            except IndexError:
                print("Couldn't find sack, walking again")
                if deadloop > 4:
                    break
                to_sack.walk(within=2, ind_len=-2)
                deadloop += 1
        print("Waiting for ore")
        inventory.wait_for(coal)
        if inventory.contains(coal) == False:
            print("Didnt successfully collect ore, breaking")
            break
        print("Walking to bank")
        to_bank.walk(within=3,ind_len=-2)
        time.sleep(0.3)
        deadloop = 0
        while True:
            try:
                print("Clicking bank deposit")
                screen.click(deposit,0.7)
                break
            except IndexError:
                print("Couldn't find bank deposit, walking again")
                if deadloop > 4:
                    break
                to_bank.walk(within=2, ind_len=-2)
                deadloop += 1
                time.sleep(1)
        depost_box_region.wait_for(deposit_checker)
        if screen.contains(deposit_checker) == False:
            print("Couldn't successfully deposit items, breaking")
            break
        for item in deposit_items:
            try:
                print("Depositing items")
                depost_box_region.click(item,timeout = 0.01)
            except IndexError:
                pass
            time.sleep(0.25)


