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

#obstacles
tree = Vision('Needle\\agility\\canifis\\tree_start.png')
tree2 = Vision('Needle\\agility\\canifis\\walk_start.png')
covered_start = Vision('Needle\\agility\\canifis\\covered_start.png')
first_gap = Vision('Needle\\agility\\canifis\\first_gap.png')
second_gap = Vision('Needle\\agility\\canifis\\second_gap.png')
third_gap = Vision('Needle\\agility\\canifis\\third_gap.png')
fourth_gap = Vision('Needle\\agility\\canifis\\fourth_gap.png')
pole_vault = Vision('Needle\\agility\\canifis\\pole_vault.png')
fifth_gap = Vision('Needle\\agility\\canifis\\fifth_gap.png')
end_gap = Vision('Needle\\agility\\canifis\\end_gap.png')

#jumps from marks
mark1_jump = Vision('Needle\\agility\\canifis\\mark1_jump.png')
mark11_jump = Vision('Needle\\agility\\canifis\\mark11_jump.png')
mark3_jump = Vision('Needle\\agility\\canifis\\mark3_jump.png')
mark4_jump = Vision('Needle\\agility\\canifis\\mark4_jump.png')

#fall stuff
fall_check = Vision('Needle\\agility\\canifis\\fall_check.png')
fall_to_start = WebWalking('walking_lists\\canifis_fall.pkl','map\\canifis_city.png')
glitch = Vision('Needle\\agility\\canifis\\gap5_glitch.png')

#marks
mark1 = Vision('Needle\\agility\\canifis\\mark11.png')
mark2 = Vision('Needle\\agility\\canifis\\mark1.png')
mark3 = Vision('Needle\\agility\\canifis\\mark3.png')
mark4 = Vision('Needle\\agility\\canifis\\mark4.png')

# WebWalking('walking_lists\\canifis_fall.pkl','map\\canifis_city.png').get_path("canifis_fall")
# time.sleep(10)

dead_loop_counter = 0
marks = 0 
start_time = time.time()

while True:
    
    if screen_top.contains(tree, threshold=0.81):
        print('starting... ')
        screen_top.click(tree, threshold=0.80)
        time.sleep(4.4)
        dead_loop_counter = 0
        
    if screen_top.contains(tree2, threshold=0.77):
        print('starting2... ')
        screen_top.click(tree2, threshold=0.76)
        time.sleep(4.4)
        dead_loop_counter = 0
        
    if screen_top.contains(tree2, threshold=0.77):
        print('starting3... ')
        screen_top.click(tree2, threshold=0.76)
        time.sleep(4.4)
        dead_loop_counter = 0
    
    # if screen_top.contains(mark0):
    #     screen_top.click(mark0)
    #     screen_top.click(mark0_jump)
        
    if screen_top.contains(first_gap, threshold=0.71):
        print('jumping first gap... ')
        screen_top.click(first_gap, threshold=0.7)
        time.sleep(4.25)
        dead_loop_counter = 0
        
        if screen_left.contains(mark1, threshold=0.81):
            print('collecting mark1... ')
            screen_left.click(mark1, threshold=0.8)
            time.sleep(2)
            marks += 1
            
            if screen_left.contains(mark11_jump, threshold=0.71):
                print('jumping second gap from mark... ')
                screen_left.click(mark11_jump, threshold=0.7)
                time.sleep(4.2)
         
    if screen_left.contains(second_gap, threshold=0.66):
        print('jumping second gap... ')
        screen_left.click(second_gap, threshold=0.65)
        time.sleep(4.5)
        dead_loop_counter = 0
        
        if screen_left.contains(mark2, threshold=0.71):
            print('collecting mark2... ')
            screen_left.click(mark2, threshold=0.7)
            time.sleep(2)
            marks += 1
            
            if screen_left.contains(mark1_jump, threshold=0.63):
                print('jumping third gap from mark... ')
                screen_left.click(mark1_jump, threshold=0.62)
                time.sleep(2)
        
    if screen_left.contains(third_gap, threshold=0.66):
        print('jumping third gap... ')
        screen_left.click(third_gap, threshold=0.65)
        time.sleep(5.4)
        dead_loop_counter = 0
        
        if screen_bottom.contains(mark3, threshold=0.61):
            print('collecting mark3... ')
            screen_bottom.click(mark3, threshold=0.6)
            time.sleep(2)
            marks += 1
            
            if screen_bottom.contains(mark3_jump, threshold=0.61):
                print('jumping fourth gap from mark... ')
                screen_bottom.click(mark3_jump, threshold=0.6)
                time.sleep(2)
        
    if screen_bottom.contains(fourth_gap, threshold=0.71):
        print('jumping fourth gap... ')
        screen_bottom.click(fourth_gap, threshold=0.7)
        time.sleep(4.4)
        dead_loop_counter = 0
        
        if screen_bottom.contains(mark4, threshold=0.61):
            print('collecting mark4... ')
            screen_bottom.click(mark4, threshold=0.6)
            time.sleep(2)
            marks += 1
            
            if screen_bottom.contains(mark4_jump, threshold=0.71):
                print('jumping pole vault from mark... ')
                screen_bottom.click(mark4_jump, threshold=0.7)
                time.sleep(4)
        
    if screen_bottom.contains(pole_vault, threshold=0.71):
        print('jumping pole vault... ')
        screen_bottom.click(pole_vault, threshold=0.7)
        time.sleep(4)
        dead_loop_counter = 0
        
    if screen_right.contains(fifth_gap, threshold=0.71):
        print('jumping fifth gap... ')
        screen_right.click(fifth_gap, threshold=0.7)
        time.sleep(5.2)
        dead_loop_counter = 0
        
    if screen_top.contains(end_gap, threshold=0.71):
        print('jumping end gap... ')
        screen_top.click(end_gap, threshold=0.7)
        time.sleep(4.1)
        dead_loop_counter = 0
        
        current_time = (time.time() - start_time)
        current_time_format = time.strftime("%H:%M:%S", time.gmtime(current_time))
        print(f"run time: {current_time_format}")
        print(f'marks collected: {marks}')
        
    if screen_left.contains(fall_check, threshold=0.71):
        print('failed jump... ')
        fall_to_start.walk(within=3)
        dead_loop_counter = 0
        
    dead_loop_counter += 1
    
    # if dead_loop_counter > 5:
    #     print('dead loop protocol...')
    #     if screen_right.contains(glitch):
    #         screen_right.click(glitch)
    #         dead_loop_counter = 0
    
    if dead_loop_counter > 7:
        print('dead loop protocol...')
        fall_to_start.walk(within=3)
        dead_loop_counter = 0
        
    time.sleep(0.8)
        