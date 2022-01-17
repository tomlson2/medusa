import time
from player import Player
from interactions import Interactions
from vision import Vision
from webwalking import WebWalking


player = Player()
screen = Interactions()
screen_top = Interactions('screen_top')
screen_bottom = Interactions('screen_bottom')
screen_left = Interactions('screen_left')
screen_right = Interactions('screen_right')
screen_close = Interactions('screen_close')
inventory = Interactions(area='inventory')
minimap = Interactions(area='minimap')
chatbox = Interactions(area='chatbox')

to_start = WebWalking('walking_lists\\to_seers.pkl','map\\seers_agility.png')

wall_start0 = Vision('Needle\\agility\\seers\\wall_start.png')
wall_start1 = Vision('Needle\\agility\\seers\\start_close.png')
wall_start2 = Vision('Needle\\agility\\seers\\wall_start_left.png')
wall_start3 = Vision('Needle\\agility\\seers\\wall_start_far.png')
first_gap = Vision('Needle\\agility\\seers\\first_gap.png')
tightrope = Vision('Needle\\agility\\seers\\tight_rope.png')
second_gap = Vision('Needle\\agility\\seers\\second_gap.png')
third_gap = Vision('Needle\\agility\\seers\\third_gap.png')
end_edge = Vision('Needle\\agility\\seers\\end_edge.png')
fall_check = Vision('Needle\\agility\\seers\\fall_check.png')
end_check = Vision('Needle\\agility\\seers\\end_check.png')

mark0 = Vision('Needle\\agility\\seers\\roof0_mark.png')
mark1 = Vision('Needle\\agility\\seers\\roof1_mark.png')
mark2 = Vision('Needle\\agility\\seers\\roof0_mark.png')
mark3 = Vision('Needle\\agility\\seers\\roof0_mark.png')
mark4 = Vision('Needle\\agility\\seers\\roof4_mark.png')

mark0_jump = Vision('Needle\\agility\\seers\\mark0_jump.png')
mark1_jump = Vision('Needle\\agility\\seers\\mark1_jump.png')
mark2_jump = Vision('Needle\\agility\\seers\\mark0_jump.png')
mark3_jump = Vision('Needle\\agility\\seers\\mark0_jump.png')
mark4_jump = Vision('Needle\\agility\\seers\\mark4_jump.png')

mark_list = [mark0, mark1, mark2, mark3, mark4]
mark_jumps = [mark0_jump, mark1_jump, mark2_jump, mark3_jump, mark4_jump]

current_roof = 0
mark_count = 0
dead_loop = 0

def start0():
    global current_roof, dead_loop
    if current_roof == 0:
        if screen_top.contains(wall_start0, threshold=0.84):
            print('starting0... ')
            screen_top.click(wall_start0, threshold=0.83)
            time.sleep(3.2)
            current_roof = 0
            dead_loop = 0
        elif screen_close.contains(wall_start3, threshold=0.84):
            print('starting3... ')
            screen_close.click(wall_start3, threshold=0.83)
            time.sleep(3.2)
            current_roof = 0
            dead_loop = 0
    return current_roof

def start1():
    global current_roof, dead_loop
    if current_roof == 0:
        if screen_top.contains(wall_start1, threshold=0.89):
            print('starting1... ')
            screen_top.click(wall_start1, threshold=0.88)
            time.sleep(3.2)
            current_roof = 0
            dead_loop = 0
    return current_roof

def start2():
    global current_roof, dead_loop
    if current_roof == 0:
        if screen_top.contains(wall_start2, threshold=0.63):
            print('starting2... ')
            screen_top.click(wall_start2, threshold=0.625)
            time.sleep(3.2)
            current_roof = 0
            dead_loop = 0
        return current_roof
    
def first_jump():
    global current_roof, dead_loop
    if current_roof == 0:
        if screen_top.contains(first_gap, threshold=0.71):
            print('jumping first gap... ')
            screen_top.click(first_gap, threshold=0.70)
            time.sleep(5.4)
            current_roof = 1
            dead_loop = 0
    return current_roof

def tightrope_walk():
    global current_roof, dead_loop
    if current_roof == 1:
        if screen_bottom.contains(tightrope, threshold=0.71):
            print('walking tightrope... ')
            screen_bottom.click(tightrope, threshold=0.70)
            time.sleep(4.9)
            current_roof = 2
            dead_loop = 0
    return current_roof

def second_jump():
    global current_roof, dead_loop
    if current_roof == 2:
        if screen_bottom.contains(second_gap, threshold=0.61):
            print('jumping second gap... ')
            screen_bottom.click(second_gap, threshold=0.60)
            time.sleep(4.4)
            current_roof = 3
            dead_loop = 0
    return current_roof

def third_jump():
    global current_roof, dead_loop
    if current_roof == 3:
        if screen_bottom.contains(third_gap, threshold=0.74):
            print('jumping third gap... ')
            screen_bottom.click(third_gap, threshold=0.73)
            time.sleep(4.7)
            current_roof = 4
            dead_loop = 0
    return current_roof

def end_jump():
    global current_roof, dead_loop
    if current_roof == 4:
        if screen_bottom.contains(end_edge, threshold=0.71):
            print('jumping end gap... ')
            screen_bottom.click(end_edge, threshold=0.70)
            time.sleep(3.1)
            current_roof = 0
            dead_loop = 0
            to_start.walk(within=3)
    return current_roof

def find_roof0():
    global current_roof
    print('finding current roof...')
    if screen_top.contains(wall_start0, threshold=0.71):
        current_roof = 0
    elif screen_top.contains(first_gap, threshold=0.71):
        current_roof = 0
    elif screen_bottom.contains(tightrope, threshold=0.71):
        current_roof = 1    
    elif screen_bottom.contains(second_gap, threshold=0.71):
        current_roof = 2
    elif screen_bottom.contains(third_gap, threshold=0.71):
        current_roof = 3
    elif screen_bottom.contains(end_edge, threshold=0.71):
        current_roof = 4
    elif screen_top.contains(fall_check, threshold=0.6):
        to_start.walk(within=3)
    elif minimap.contains(end_check):
        to_start.walk(within=3)
        current_roof = 0
    return current_roof

def find_roof1():
    global current_roof
    print('finding current roof...')
    if screen_top.contains(mark0_jump, threshold=0.71):
        screen.click(mark_jumps[0])
        current_roof += 1
    elif screen_top.contains(mark1_jump, threshold=0.71):
        screen.click(mark_jumps[1])
        current_roof += 1
    elif screen_bottom.contains(mark2_jump, threshold=0.71):
        screen.click(mark_jumps[2])
        current_roof += 1
    elif screen_bottom.contains(third_gap, threshold=0.71):
        screen.click(mark_jumps[3])
        current_roof += 1
    elif screen_bottom.contains(mark4_jump, threshold=0.71):
        screen.click(mark_jumps[4])
        current_roof += 1
    return current_roof
    
def marks():
    global current_roof, mark_count, dead_loop
    for i in range(0,5):
        if i == current_roof:
            if screen.contains(mark_list[i]):
                screen.click(mark_list[i])
                time.sleep(2)
                screen.wait_for(mark_jumps[i])
                screen.click(mark_jumps[i])
                mark_count += 1
                print(f'marks collected: {mark_count}')
                current_roof += 1
                dead_loop = 0
            return current_roof


find_roof0()

while True:

    start0()
    start1()
    start2()
    marks()
    first_jump()
    marks()
    tightrope_walk()
    marks()
    second_jump()
    marks()
    third_jump()
    marks()
    end_jump()
    
    dead_loop += 1
    if dead_loop > 5:
        find_roof0()
    if dead_loop > 6:
        find_roof1()
    if dead_loop > 7:
        to_start.walk(within=3)
        dead_loop = 0
    
    time.sleep(1)