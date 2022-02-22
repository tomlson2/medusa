import time
import random
from webwalking import WebWalking
from player import Player
from vision import Vision
from numpy import array
from windowcapture import ScreenRegion, CustomRegion, InventoryRegion, ChatboxRegion


'''
example setup, need the three circled patches to not be used:
https://imgur.com/a/fcTIHsm
use proper params and function in main while loop:
normal_farming = 12 watering cans
grico_farming = grico watering can (will be able to purchase after 200 points earned)
34 - 54 ~21k xp/hr, 6 hours. param: golo_text
54 - 74 ~55k xp/hr, 17 hours. param: bolo_text
74 - 85 ~80k xp/hr, 27 hours. param: loga_text

brightness 2, zoom 1, camera north, full up
start in the game once youve found a world
'''


chatbox = ChatboxRegion()
screen = ScreenRegion()
screen_right = CustomRegion(980, 1035, 929, 36)
inventory = InventoryRegion()
player = Player()

to_start = WebWalking('walking_lists\\tithe_start.pkl','map\\tithe_farm_map.png')

table = Vision('Needle\\tithe_farm\\table.png')
farm_door = Vision('Needle\\tithe_farm\\farm_door.png')
farm_door_close = Vision('Needle\\tithe_farm\\farm_door_close.png')
door_left = Vision('Needle\\tithe_farm\\farm_door_left.png')
watering_can = Vision('Needle\\tithe_farm\\watering_can.png')
water_barrel = Vision('Needle\\tithe_farm\\water_barrel.png')
seed_bag = Vision('Needle\\tithe_farm\\seed_bag.png')
stamina = Vision('Needle\\stamina1.png')

fertiliser = Vision('Needle\\tithe_farm\\fertiliser.png')
drop = Vision('Needle\\tithe_farm\\drop.png')
tap_here = Vision('Needle\\tap_here_to_continue.png')

golo_text = Vision('Needle\\tithe_farm\\golovanova_seed_text.png')
golo_seed = Vision('Needle\\tithe_farm\\golo_seed.png')
bolo_text = Vision('Needle\\tithe_farm\\bolo_seed_text.png')
loga_text = Vision('Needle\\tithe_farm\\loga_text.png')

plant_check = Vision('Needle\\tithe_farm\\plant_check.png')
logout_tab = Vision('Needle\\tithe_farm\\logout_tab.png')
to_logout = Vision('Needle\\tithe_farm\\to_logout.png')
to_logout1 = Vision('Needle\\tithe_farm\\to_logout1.png')

count = 0


#X,Y,W,H
left_start = array([(820,582,40,20)])
right_start = array([(1110,583,65,22)])
left_middle = array([(780,538,70,34)])
right_middle = array([(1087,543,52,34)])
left_bottom = array([(755,730,50,30)])
left_far_bottom = array([(706,943,110,67)])
lfb_water = array([(849,644,80,76)])
right_far = array([(1124,641,90,55)])
right_single = array([(1288,586,57,65)])
right_up = array([(1019,305,78,55)])
right_up_middle = array([(1087,500,60,55)])
minimap_run_start = array([(1647,80,24,57)])
harvest_left_bottom = array([(746,750,60,30)])

def start_tithe(seed_type_text):
    if inventory.contains(golo_seed, threshold=0.65):
        pass
    else:
        print('getting tithe seeds...')
        screen.click(table,0.63)
        time.sleep(random.normalvariate(2, 0.11))
        chatbox.wait_for(seed_type_text)
        time.sleep(random.normalvariate(0.21, 0.01))
        chatbox.click(seed_type_text)
        time.sleep(random.normalvariate(2, 0.05))
        if screen_right.contains(farm_door, threshold=0.85):
            screen_right.click(farm_door, threshold=0.85)
            time.sleep(random.normalvariate(3, 0.16))
        elif screen_right.contains(farm_door_close, threshold=0.85):
            screen_right.click(farm_door_close, threshold=0.85)
            time.sleep(random.normalvariate(3, 0.16))
        inventory.click(fertiliser, right_click=True)
        time.sleep(random.normalvariate(0.52, 0.01))
        screen.click(drop)
      
def plant_start(seed_type):
    to_start.walk(2)
    time.sleep(0.3)
    time.sleep(random.normalvariate(0.41, 0.02))
    print('planting seeds...')
    inventory.click(seed_type, threshold=0.65)
    time.sleep(0.15)
    screen.click_region(left_start)
    time.sleep(0.2)
    if screen.contains(plant_check, threshold=0.8):
        print('planting successful')
    else:
        print('world crashed, breaking')
        time.sleep(800)
    time.sleep(0.7)
    inventory.click(watering_can)
    time.sleep(0.9)
    screen.click_region(left_start)
    time.sleep(random.normalvariate(0.22, 0.01))
    
    inventory.click(seed_type, threshold=0.65)
    time.sleep(1)
    screen.click_region(right_start)
    time.sleep(0.2)
    if screen.contains(plant_check, threshold=0.8):
        print('planting successful')
    else:
        print('world crashed, breaking')
        time.sleep(800)
    time.sleep(1.0)
    inventory.click(watering_can)
    time.sleep(0.72)
    screen.click_region(right_middle)
    time.sleep(random.normalvariate(0.22, 0.01))

def plant_seeds(seed_type):
    for i in range(3):
        inventory.click(seed_type, threshold=0.65)
        time.sleep(0.75)
        screen.click_region(left_bottom)
        time.sleep(1.45)
        inventory.click(watering_can)
        time.sleep(0.85)
        screen.click_region(left_middle)
        time.sleep(random.normalvariate(0.22, 0.01))
        
        inventory.click(seed_type, threshold=0.65)
        time.sleep(1)
        screen.click_region(right_middle)
        time.sleep(1.05)
        inventory.click(watering_can)
        time.sleep(0.8)
        screen.click_region(right_middle)
        time.sleep(random.normalvariate(0.22, 0.01))
    time.sleep(0.15)
        
def plant_seeds1(seed_type, grico=False):
    if grico == False:
        index = 1
    else:
        index = 0
    for i in range(3):
        inventory.click(seed_type, threshold=0.65)
        time.sleep(0.75)
        screen.click_region(left_bottom)
        time.sleep(1.41)
        inventory.click(watering_can, ind=index)
        time.sleep(0.9)
        screen.click_region(left_middle)
        time.sleep(random.normalvariate(0.22, 0.01))
        
        inventory.click(seed_type, threshold=0.65)
        time.sleep(0.75)
        screen.click_region(right_middle)
        time.sleep(1)
        inventory.click(watering_can, ind=index)
        time.sleep(0.75)
        screen.click_region(right_middle)
        time.sleep(random.normalvariate(0.22, 0.01))
    time.sleep(0.55)
        
def new_aisle(seed_type, grico=False):
    if grico == False:
        index = 1
    else:
        index = 0
    time.sleep(random.normalvariate(0.33, 0.02))
    inventory.click(seed_type, threshold=0.65)
    time.sleep(random.normalvariate(0.17, 0.005))
    screen.click_region(left_far_bottom)
    time.sleep(0.2)
    if screen.contains(plant_check, threshold=0.8):
        print('planting successful')
    else:
        print('world crashed, breaking')
        logout()
        time.sleep(800)
    time.sleep(2.8)
    inventory.click(watering_can, ind=index)
    time.sleep(0.45)
    screen.click_region(lfb_water)
    time.sleep(random.normalvariate(0.23, 0.01))
    
    inventory.click(seed_type, threshold=0.65)
    time.sleep(0.85)
    screen.click_region(right_far)
    time.sleep(0.2)
    if screen.contains(plant_check, threshold=0.8):
        print('planting successful')
    else:
        print('world crashed, breaking')
        logout()
        time.sleep(800)
    time.sleep(0.75)
    inventory.click(watering_can, ind=index)
    time.sleep(0.858)
    screen.click_region(right_middle)
    time.sleep(random.normalvariate(0.21, 0.01))
    
def single_column(seed_type, grico=False):
    time.sleep(0.2)
    if grico == False:
        index = 4
    else:
        index = 0
    inventory.click(seed_type, threshold=0.65)
    time.sleep(random.normalvariate(0.5, 0.01))
    screen.click_region(right_single)
    time.sleep(0.2)
    if screen.contains(plant_check, threshold=0.8):
        print('planting successful')
    else:
        print('world crashed, breaking')
        logout()
        time.sleep(800)
    time.sleep(2.8)
    inventory.click(watering_can, ind=index)
    time.sleep(0.9)
    screen.click_region(right_up_middle)
    time.sleep(0.32)
    
    for i in range(3):
        inventory.click(seed_type, threshold=0.65)
        time.sleep(0.7)
        screen.click_region(right_up)
        time.sleep(0.71)
        inventory.click(watering_can, ind=index)
        time.sleep(1.8)
        screen.click_region(right_up_middle)
        time.sleep(0.2)
        
def water_plants():
    time.sleep(0.5)
    screen.click_region(minimap_run_start)
    to_start.walk(2)
    time.sleep(0.1)
    # to_start.walk(2)
    print('watering plants...')
    time.sleep(0.35)
    screen.click_region(left_start)
    time.sleep(random.normalvariate(2.3, 0.01))
    screen.click_region(right_start)
    time.sleep(random.normalvariate(2.5, 0.01))
    for i in range(3):
        screen.click_region(left_bottom)
        time.sleep(3)
        screen.click_region(right_middle)
        time.sleep(random.normalvariate(2.65, 0.01))
           
    screen.click_region(left_far_bottom)
    time.sleep(3.7)
    screen.click_region(right_far)
    time.sleep(2.3)
    for i in range(3):
        screen.click_region(left_bottom)
        time.sleep(2.9)
        screen.click_region(right_middle)
        time.sleep(random.normalvariate(2.55, 0.01))
        
    screen.click_region(right_single)
    time.sleep(3.95)
    for i in range(3):
        time.sleep(0.45)
        screen.click_region(right_up)
        time.sleep(2.35)
        time.sleep(random.normalvariate(0.1, 0.001))
        
    time.sleep(0.12)

def harvest_plants():
    to_start.walk(2)
    print('harvesting plants...')
    time.sleep(0.35)
    screen.click_region(left_start)
    time.sleep(random.normalvariate(1.95, 0.01))
    screen.click_region(right_middle)
    time.sleep(random.normalvariate(2.2, 0.01))
    for i in range(3):
        screen.click_region(left_bottom)
        time.sleep(3)
        screen.click_region(right_middle)
        time.sleep(random.normalvariate(2.65, 0.01))
           
    screen.click_region(left_far_bottom)
    time.sleep(3.7)
    screen.click_region(right_far)
    time.sleep(2.3)
    for i in range(3):
        screen.click_region(left_bottom)
        time.sleep(2.9)
        screen.click_region(right_middle)
        time.sleep(random.normalvariate(2.55, 0.01))
        
    screen.click_region(right_single)
    time.sleep(3.95)
    for i in range(3):
        time.sleep(0.45)
        screen.click_region(right_up)
        time.sleep(2.35)
        time.sleep(random.normalvariate(0.1, 0.001))
        
    time.sleep(0.12)
    pass

def refill_cans(grico=True):
    global count
    count += 1
    print(count)
    if grico == False:
        print('filling watering cans...')
        time.sleep(random.normalvariate(0.4, 0.05))
        inventory.click(watering_can)
        time.sleep(random.normalvariate(0.3, 0.05))
        screen.click(water_barrel)
        time.sleep(random.randint(23, 24))
    else:
        if count > 4:
            
            time.sleep(random.normalvariate(0.4, 0.05))
            inventory.click(watering_can)
            time.sleep(random.normalvariate(0.3, 0.05))
            screen.click(water_barrel)
            time.sleep(random.randint(5, 7))
            count = 0

def reset_game():
    # turn in plants
    screen.click(seed_bag, threshold=0.8)
    time.sleep(random.normalvariate(2.4, 0.05))
    chatbox.wait_for(tap_here)
    if chatbox.contains(tap_here):
        while chatbox.contains(tap_here):
            chatbox.click(tap_here)
            time.sleep(random.normalvariate(1.4, 0.02))
        time.sleep(random.normalvariate(0.25, 0.001))
        screen.click(door_left, threshold=0.82)
    time.sleep(random.normalvariate(3, 0.1))
    
    if player.run() <= 50:
        inventory.click(stamina)
        time.sleep(random.uniform(.6, .94))
        
def logout():
    screen.click(logout_tab)
    time.sleep(random.uniform(0.4, 1.25))
    try:
        inventory.click(to_logout)
    except IndexError:
        inventory.click(to_logout1)

# script for once the grico can is acquired
def grico_farming(text):
    global start_time, tithe_count
    start_tithe(text)
    for i in range (5):
        plant_start(golo_seed)
        plant_seeds(golo_seed)
        new_aisle(golo_seed, grico=True)
        plant_seeds1(golo_seed, grico=True)
        single_column(golo_seed, grico=True)
        water_plants()
        water_plants()
        water_plants()

        current_time = (time.time() - start_time)
        current_time_format = time.strftime("%H:%M:%S", time.gmtime(current_time))
        print(f"run time: {current_time_format}")
        
        refill_cans(grico=True)
    time.sleep(0.2)

    reset_game()
    tithe_count += 1
    print(f'tithe rounds completed: {tithe_count}')

# normal watering cans script    
def normal_farming(text):
    global start_time, tithe_count
    start_tithe(text)
    for i in range (5):
        plant_start(golo_seed)
        plant_seeds(golo_seed)
        new_aisle(golo_seed)
        plant_seeds1(golo_seed)
        single_column(golo_seed)
        water_plants()
        water_plants()
        water_plants()

        current_time = (time.time() - start_time)
        current_time_format = time.strftime("%H:%M:%S", time.gmtime(current_time))
        print(f"run time: {current_time_format}")
        
        refill_cans(grico=False)

    reset_game()
    tithe_count += 1
    print(f'tithe rounds completed: {tithe_count}')

# WebWalking('walking_lists\\tithe_start.pkl','map\\tithe_farm_map.png').get_path("tithe_start")
# print('done')
# time.sleep(10)

print('=====starting tithe farm=====')
start_time = time.time()
tithe_count = 0

while True:
    grico_farming(bolo_text)
    #normal_farming(bolo_text)
