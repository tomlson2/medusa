import time
import random
from tracemalloc import start
from player import Player
from vision import Vision
from windowcapture import InventoryRegion, ChatboxRegion, CustomRegion


'''
go to triple iron spot north of duel arena
north full up
full zoom, 1 brightness
inventory open, TAP DROP MODE ON
'''


player = Player()
inventory = InventoryRegion()
chatbox = ChatboxRegion()

top_rock = CustomRegion(731,261,326,256)
bot_rock = CustomRegion(731,757,382,344)
left_rock = CustomRegion(457,533,369,320)

iron_ore = Vision('Needle\\aio_mining\\iron_ore.png')
top_rockv = Vision('Needle\\aio_mining\\top_rock.png')
bot_rockv = Vision('Needle\\aio_mining\\bot_rock.png')
left_rockv = Vision('Needle\\aio_mining\\left_rock.png')
tap_here = Vision('Needle\\tap_here_to_continue.png')
gem = Vision('Needle\\aio_mining\\gem.png')

start_time = time.time()

ore = 0
ore_xp = 35

print('------starting mining------')
while True:
    count = random.randrange(5,9)
    while inventory.amount(iron_ore, 0.7) < count:
        current_ore = inventory.amount(iron_ore, 0.7)
        while current_ore == inventory.amount(iron_ore, 0.7):
            if top_rock.contains(top_rockv, 0.93):
                top_rock.click(top_rockv, 0.93)
                # sleep so mouse click confirmation doesnt cover the tree
                time.sleep(1)
                loop_start = time.time()
                while top_rock.contains(top_rockv, 0.95):
                    if chatbox.contains(tap_here) or (time.time() - loop_start > 15):
                        break
                
            elif left_rock.contains(left_rockv, 0.95):
                left_rock.click(left_rockv, 0.95)
                # sleep so mouse click confirmation doesnt cover the tree
                time.sleep(1)
                loop_start = time.time()
                while left_rock.contains(left_rockv, 0.95):
                    if chatbox.contains(tap_here) or (time.time() - loop_start > 15):
                        break
            
            elif bot_rock.contains(bot_rockv, 0.95):
                bot_rock.click(bot_rockv, 0.95)
                # sleep so mouse click confirmation doesnt cover the tree
                time.sleep(1)
                loop_start = time.time()
                while bot_rock.contains(bot_rockv, 0.95):
                    if chatbox.contains(tap_here) or (time.time() - loop_start > 15):
                        break
            
            if inventory.amount(iron_ore, 0.7) > current_ore:
                ore += 1
                break
            
            # print(f'ore mined: {ore} // ore mined per hr: {round((ore / (time.time() - start_time)) * 3600)} // xp per hr: {round(((ore / (time.time() - start_time)) * 3600) * ore_xp)}')
    
    # print('dropping ore...')
    inventory.drop_click(iron_ore, inventory.amount(iron_ore, 0.7))
    if inventory.contains(gem, 0.6):
        print('GEM!!!')
        inventory.drop_click(gem, inventory.amount(gem, 0.6))
    time.sleep(random.normalvariate(0.24,0.005))
        
    current_time = (time.time() - start_time)
    current_time_format = time.strftime("%H:%M:%S", time.gmtime(current_time))
    # print(f"run time: {current_time_format}")