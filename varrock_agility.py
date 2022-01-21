import time
from player import Player
from windowcapture import ScreenRegion, InventoryRegion, CustomRegion
from vision import Vision
from webwalking import WebWalking

'''
about ~12k-14k xp/hr
setup: 
full north, 2 zoom, brightness 3 (middle)
start on the path to the right of the course
no tabs open, no inventory or stats, no chat
'''

screen = ScreenRegion()
screen_top = CustomRegion(1902, 557, 8, 36)
screen_bottom = CustomRegion(1894, 518, 12, 549)
screen_left = CustomRegion(964, 1028, 7, 41)
screen_right = CustomRegion(980, 1035, 929, 36)
inventory = InventoryRegion()

to_start = WebWalking('walking_lists\\end_to_start.pkl','map\\varrock_agility.png')
fall2_to_start = WebWalking('walking_lists\\fall2_to_start.pkl','map\\varrock_agility.png')

#agility obstacles in order
start = Vision('Needle\\agility\\wall_far.png')
rough_wall = Vision('Needle\\agility\\rough_wall.png')
rough_wall_close = Vision('Needle\\agility\\rough_wall_close.png')

clothes_line = Vision('Needle\\agility\\clothes_line.png')
corner_gap = Vision('Needle\\agility\\corner_gap.png')
balance_wall = Vision('Needle\\agility\\balance_wall.png')
leap_gap = Vision('Needle\\agility\\leap_gap.png')
big_gap = Vision('Needle\\agility\\big_gap.png')
red_gap = Vision('Needle\\agility\\big_red_gap.png')
hurdle_gap = Vision('Needle\\agility\\hurdle_ledge.png')
end = Vision('Needle\\agility\\off_edge.png')
walk_check = Vision('Needle\\agility\\walk_check.png')
fall2_check = Vision('Needle\\agility\\fall2_check.png')

bag = Vision('Needle\\bag_tab.png')
stamina = Vision('Needle\\stamina1.png')
#WebWalking('walking_lists\\end_to_start.pkl','map\\varrock_agility.png').get_path("end_to_start")

player = Player()
start_time = time.time()
dead_loop_counter = 0

while True:
    
    if screen_left.contains(start, threshold=0.7):
        print('starting0... ')
        screen_left.click(start, threshold=0.7)
        time.sleep(5.7)
        dead_loop_counter = 0
        
    if screen_left.contains(rough_wall, threshold=0.7):
        print('starting1... ')
        screen_left.click(rough_wall, threshold=0.7)
        time.sleep(5.4)
        dead_loop_counter = 0
        
    if screen_left.contains(rough_wall_close, threshold=0.80):
        print('starting2... ')
        screen_left.click(rough_wall_close, threshold=0.80)
        time.sleep(4.4)
        dead_loop_counter = 0
    
    
    if screen_left.contains(clothes_line, threshold=0.7):
        print('jumping clothes line... ')
        screen_left.click(clothes_line, threshold=0.7)
        time.sleep(8.1)
        dead_loop_counter = 0
        
    if screen_left.contains(corner_gap, threshold=0.78):
        print('jumping corner gap... ')
        screen_left.click(corner_gap, threshold=0.76)
        time.sleep(4.0)
        dead_loop_counter = 0
    
    if screen_left.contains(balance_wall, threshold=0.75):
        print('balancing wall... ')
        screen_left.click(balance_wall, threshold=0.75)
        time.sleep(9.9)
        dead_loop_counter = 0
        
    # if screen_bottom.contains(leap_gap, threshold=0.93):
    #     print('leaping small gap... ')
    #     screen_bottom.click(leap_gap, threshold=0.75)
    #     time.sleep(1.8)
        
    if screen_right.contains(big_gap, threshold=0.8):
        print('leaping big gap... ')
        screen_right.click(big_gap, threshold=0.8)
        time.sleep(9.2)
        dead_loop_counter = 0
        
    if screen_right.contains(red_gap, threshold=0.72):
        print('leaping red gap... ')
        screen_right.click(red_gap, threshold=0.72)
        time.sleep(5.6)
        dead_loop_counter = 0
        
    if screen_top.contains(hurdle_gap, threshold=0.65):
        print('hurdling ledge... ')
        screen_top.click(hurdle_gap, threshold=0.65)
        time.sleep(4.2)
        dead_loop_counter = 0
        
    if screen_top.contains(end, threshold=0.75):
        print('jumping off edge... ')
        screen_top.click(end, threshold=0.75)
        time.sleep(4.2)
        
        if player.run() < 50:
            print('low run energy')
            screen_right.click(bag)
            time.sleep(0.74)
            inventory.click(stamina,threshold=0.6)
            time.sleep(0.7)
            screen_right.click(bag)
        
        current_time = (time.time() - start_time)
        current_time_format = time.strftime("%H:%M:%S", time.gmtime(current_time))
        print(f"run time: {current_time_format}")
        
        dead_loop_counter = 0
        
    if screen_right.contains(leap_gap, threshold=0.90):
        print('leaping small gap... ')
        screen_right.click(leap_gap, threshold=0.90)
        time.sleep(3.2)
        dead_loop_counter = 0
        
    if screen_top.contains(walk_check, threshold=0.8):
        print('walking to start of course...')
        to_start.walk(within=3)
        time.sleep(.45)
        dead_loop_counter = 0
        
    if screen_left.contains(fall2_check):
        print('ive fallen and cant get up...')
        fall2_to_start.walk(within=3)
        time.sleep(.45)
        
        
    if dead_loop_counter > 5:
        print('loop broken, walking to start...')
        to_start.walk(within=3)
        time.sleep(.45)
        dead_loop_counter = 0
        if screen_left.contains(rough_wall, threshold=0.8):
            screen_left.click(rough_wall, threshold=0.76)
            time.sleep(.3)
        
    dead_loop_counter += 1
    time.sleep(0.5)