import time
import random
from tracemalloc import start
from turtle import Screen
from player import Player
from vision import Vision
from windowcapture import InventoryRegion, ChatboxRegion, CustomRegion, ScreenRegion


'''
go to triple iron spot north of duel arena
north full up
full zoom, 1 brightness
inventory open, TAP DROP MODE ON
'''


player = Player()
inventory = InventoryRegion()
chatbox = ChatboxRegion()
screen = ScreenRegion()

top_rock = CustomRegion(731,261,326,256)
bot_rock = CustomRegion(731,757,382,344)
left_rock = CustomRegion(457,533,369,320)

iron_ore = Vision('Needle\\aio_mining\\iron_ore.png')
top_rockv = Vision('Needle\\aio_mining\\top_rock.png')
bot_rockv = Vision('Needle\\aio_mining\\bot_rock.png')
left_rockv = Vision('Needle\\aio_mining\\left_rock.png')
tap_here = Vision('Needle\\tap_here_to_continue.png')
gem = Vision('Needle\\aio_mining\\gem.png')
gem2 = Vision('Needle\\aio_mining\\gem2.png')

# login/logout needles

inventory_closed = Vision('Needle\\aio_mining\\inventory_pane.png')
logout_pane = Vision('Needle\\aio_mining\\logout_pane.png')
tap_here_to_logout = Vision('Needle\\aio_mining\\tap_here_to_logout.png')
play_now = Vision('Needle\\aio_mining\\play_now.png')
tap_here_to_play = Vision('Needle\\aio_mining\\tap_here_to_play.png')

start_time = time.time()

ore = 0
ore_xp = 35

def logout():
    screen.click(logout_pane)
    screen.wait_for(tap_here_to_logout)
    screen.click(tap_here_to_logout)
    print('player logged out!')

def login():
    screen.click(play_now)
    screen.wait_for(tap_here_to_play, t = 25)
    screen.click(tap_here_to_play)
    screen.wait_for(inventory_closed)
    print('player logged in!')

def break_handler(start, hours_until_break):
    if time.time() - start > (hours_until_break * 3600):
        print('handling break...')
        logout()
        time.sleep(random.randrange(12, 15)*60)
        login()
        screen.click(inventory_closed)
        print('break completed!')
    else:
        pass

print('------starting mining------')
while True:
    count = random.randrange(17,23)
    while inventory.amount(iron_ore, 0.7) < count:
        current_ore = inventory.amount(iron_ore, 0.7)
        while current_ore == inventory.amount(iron_ore, 0.7):
            if top_rock.contains(top_rockv, 0.93):
                top_rock.click(top_rockv, 0.93)
                # sleep so mouse click confirmation doesnt cover the tree
                time.sleep(0.75)
                loop_start = time.time()
                while top_rock.contains(top_rockv, 0.95):
                    if chatbox.contains(tap_here) or (time.time() - loop_start > 15):
                        break
                
            elif left_rock.contains(left_rockv, 0.95):
                left_rock.click(left_rockv, 0.95)
                # sleep so mouse click confirmation doesnt cover the tree
                time.sleep(0.75)
                loop_start = time.time()
                while left_rock.contains(left_rockv, 0.95):
                    if chatbox.contains(tap_here) or (time.time() - loop_start > 15):
                        break
            
            elif bot_rock.contains(bot_rockv, 0.95):
                bot_rock.click(bot_rockv, 0.95)
                # sleep so mouse click confirmation doesnt cover the tree
                time.sleep(0.75)
                loop_start = time.time()
                while bot_rock.contains(bot_rockv, 0.95):
                    if chatbox.contains(tap_here) or (time.time() - loop_start > 15):
                        break
            
            if inventory.amount(iron_ore, 0.7) > current_ore:
                ore += 1
                break

    print('dropping ore...')
    inventory.drop_list_vert(list=[gem, gem2, iron_ore])
    current_time = (time.time() - start_time)
    current_time_format = time.strftime("%H:%M:%S", time.gmtime(current_time))
    print(f"run time: {current_time_format}")
    print(f'ore mined: {ore} // ore mined per hr: {round((ore / (time.time() - start_time)) * 3600)} // xp: {(ore * ore_xp)} // xp per hr: {round(((ore / (time.time() - start_time)) * 3600) * ore_xp)}')
    break_handler(start_time, 4)