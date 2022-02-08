import time
import random
from player import Player
from vision import Vision
from numpy import array
from windowcapture import ScreenRegion, InventoryRegion, CustomRegion, ChatboxRegion, MinimapRegion


'''
==========TURN RUN OFF==========
zoom 4 (all the way in) look east, leave cam as is after looking east
have bank tab with just food and dodgy necklaces, BANK WITHDRAW AT 5!!!!!
inventory open
how it should look: https://imgur.com/a/h4HP6RB
'''


inventory = InventoryRegion()
screen = ScreenRegion()
screen_left = CustomRegion(964, 1028, 7, 41)

knight_region = array([(864,398,170,203)])
bank_region = array([(1286,213,100,215)])
knight_from_bank_region = array([(559,481,141,252)])

player = Player()

potato = Vision('Needle\\sandcrab\\potato.png')
dodgy = Vision('Needle\\thieving\\knights\\dodgy.png')
coin_pouch = Vision('Needle\\thieving\\knights\\coin_pouch.png')
x = Vision('Needle\\bank_skills\\compost\\x.png')
click_check = Vision('Needle\\thieving\\knights\\click_check.png')

coin_pouch_count = 1
dead_click_check = 0
bank_count = 0
food_count = (inventory.amount(potato, 0.7))
start_time = time.time()
dodgy_timer = time.time()


print('-----starting pickpocketer-----')
while True:
    
    current_health = player.health()
    while player.health() == current_health:
        screen.click_region(knight_region)
        #changed from .1
        time.sleep(0.2)
        if screen.contains(click_check):
            dead_click_check = 0
            coin_pouch_count += 1
        else:
            print('check not found')
            dead_click_check += 1
            if dead_click_check > 8:
                break
        time.sleep(random.normalvariate(0.35, 0.01))
        
        if coin_pouch_count > 22:
            print('cashing out...')
            time.sleep(random.normalvariate(0.6, 0.04))
            inventory.click(coin_pouch)
            time.sleep(0.1)
            coin_pouch_count = 0
            
    coin_pouch_count -= 1
    if player.health() < 12:
        time.sleep(random.normalvariate(0.1, 0.001))
        inventory.click(potato)
        print('eating...')
        time.sleep(random.normalvariate(1.1, 0.1))
        
        current_time = (time.time() - start_time)
        current_time_format = time.strftime("%H:%M:%S", time.gmtime(current_time))
        print(f"run time: {current_time_format}")
    
        if inventory.amount(potato, 0.7) < 2:
            print('banking...')
            time.sleep(3.5)
            screen.click_region(bank_region)
            time.sleep(3.5)
            if inventory.amount(dodgy, 0.7) < 2:
                screen_left.click(dodgy)
                time.sleep(0.36)
            screen_left.click(potato)
            time.sleep(random.normalvariate(0.3, 0.008))
            screen_left.click(potato)
            time.sleep(random.normalvariate(0.2, 0.005))
            screen_left.click(potato)
            time.sleep(random.normalvariate(0.32, 0.01))
            screen.click(x)
            time.sleep(random.normalvariate(0.44, 0.002))
            screen.click_region(knight_from_bank_region)
            time.sleep(random.normalvariate(0.1, 0.001))
            coin_pouch_count += 1
            bank_count += 1
        
        time.sleep(1)
        
    if screen.contains(x):
        screen.click(x)
        time.sleep(random.normalvariate(0.9, 0.1))
        screen.click_region(knight_from_bank_region)
        time.sleep(0.2)
        if screen.contains(click_check):
            dead_click_check = 0
        time.sleep(random.normalvariate(1, 0.1))
        
        
    if time.time() - dodgy_timer > random.randint(295, 320):
        print('refreshing dodgy...')
        if inventory.contains(dodgy):
            time.sleep(random.normalvariate(0.32, 0.03))
            inventory.click(dodgy)
            time.sleep(random.normalvariate(0.62, 0.12))
            dodgy_timer = time.time()
        else:
            dodgy_timer = time.time()
            
    if dead_click_check > 8:
        print('not thieving, sleep')
        time.sleep(5)
        
    if dead_click_check > 9:
        print('knight no longer being clicked')
        print('killing script')
        
        current_time = (time.time() - start_time)
        current_time_format = time.strftime("%H:%M:%S", time.gmtime(current_time))
        print(f"run time: {current_time_format}")
        break
        
    time.sleep(random.normalvariate(3.64, 0.13))
        