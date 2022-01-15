import time

from player import Player
from interactions import Interactions
from vision import Vision
from webwalking import WebWalking

'''
setup: 
full north 3 zoom 
start near the start of the varrock agility course
no tabs open, no inventory or stats, no chat
'''

screen = Interactions()
screen_top = Interactions('screen_top')
screen_bottom = Interactions('screen_bottom')
screen_left = Interactions('screen_left')
screen_right = Interactions('screen_right')
inventory = Interactions(area='inventory')

to_start = WebWalking('walking_lists\\end_to_start.pkl','map\\varrock_agility.png')
fall2_to_start = WebWalking('walking_lists\\fall2_to_start.pkl','map\\varrock_agility.png')

#agility obstacles in order
start = Vision('Needle\\agility\\varrock_start.png')
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

#WebWalking('walking_lists\\fall2_to_start.pkl','map\\varrock_agility.png').get_path("fall2_to_start")

dead_loop_counter = 0

while True:
    
    if screen_left.contains(start, threshold=0.81):
        print('starting... ')
        screen_left.click(start, threshold=0.80)
        time.sleep(2.4)
        dead_loop_counter = 0
        
    if screen_left.contains(rough_wall, threshold=0.80):
        print('starting... ')
        screen_left.click(rough_wall, threshold=0.80)
        time.sleep(2.4)
        dead_loop_counter = 0
        
    if screen_left.contains(rough_wall_close, threshold=0.80):
        print('starting... ')
        screen_left.click(rough_wall_close, threshold=0.80)
        time.sleep(2.4)
        dead_loop_counter = 0
    
    
    if screen_left.contains(clothes_line, threshold=0.80):
        print('jumping clothes line... ')
        screen_left.click(clothes_line, threshold=0.75)
        time.sleep(8.1)
        dead_loop_counter = 0
        
    if screen_left.contains(corner_gap, threshold=0.85):
        print('jumping corner gap... ')
        screen_left.click(corner_gap, threshold=0.75)
        time.sleep(2.5)
        dead_loop_counter = 0
    
    if screen_left.contains(balance_wall, threshold=0.75):
        print('balancing wall... ')
        screen_left.click(balance_wall, threshold=0.75)
        time.sleep(9.3)
        dead_loop_counter = 0
        
    # if screen_bottom.contains(leap_gap, threshold=0.93):
    #     print('leaping small gap... ')
    #     screen_bottom.click(leap_gap, threshold=0.75)
    #     time.sleep(1.8)
        
    if screen_right.contains(big_gap, threshold=0.82):
        print('leaping big gap... ')
        screen_right.click(big_gap, threshold=0.75)
        time.sleep(4)
        dead_loop_counter = 0
        
    if screen_right.contains(red_gap, threshold=0.85):
        print('leaping red gap... ')
        screen_right.click(red_gap, threshold=0.75)
        time.sleep(3)
        dead_loop_counter = 0
        
    if screen_top.contains(hurdle_gap, threshold=0.65):
        print('hurdling ledge... ')
        screen_top.click(hurdle_gap, threshold=0.65)
        time.sleep(2.5)
        dead_loop_counter = 0
        
    if screen_top.contains(end, threshold=0.85):
        print('jumping off edge... ')
        screen_top.click(end, threshold=0.75)
        time.sleep(1.8)
        dead_loop_counter = 0
        
    if screen_bottom.contains(leap_gap, threshold=0.95):
        print('leaping small gap... ')
        screen_bottom.click(leap_gap, threshold=0.75)
        time.sleep(1.8)
        dead_loop_counter = 0
        
    if screen_top.contains(walk_check, threshold=0.8):
        print('walking to start of course...')
        to_start.walk(within=3)
        
        dead_loop_counter = 0
        
    if screen_left.contains(fall2_check):
        print('ive fallen and cant get up...')
        fall2_to_start.walk(within=3)
        
        
    if dead_loop_counter > 3:
        print('loop broken, walking to start...')
        to_start.walk(within=3)
        dead_loop_counter = 0
        if screen_left.contains(rough_wall, threshold=0.8):
            screen_left.click(rough_wall, threshold=0.76)
            time.sleep(.3)
        
    dead_loop_counter += 1
    
    time.sleep(0.5)