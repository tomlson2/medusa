import time
from player import Player
from vision import Vision
from windowcapture import ScreenRegion, InventoryRegion, CustomRegion, ChatboxRegion, MinimapRegion
from webwalking import WebWalking


'''
about ~34k xp/hr
------way better on low population course------
zoom 1, brightness 2
north, full tilt
start either right after an obstacle or near start
'''


player = Player()
screen = ScreenRegion()
screen_top = CustomRegion(1902, 557, 8, 36)
screen_bottom = CustomRegion(1894, 518, 12, 549)
screen_left = CustomRegion(964, 1028, 7, 41)
screen_right = CustomRegion(980, 1035, 929, 36)
screen_close = CustomRegion(582, 396, 745, 384)
inventory = InventoryRegion()
minimap = MinimapRegion()
chatbox = ChatboxRegion()

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
fall1_check = Vision('Needle\\agility\\seers\\fall1_check.png')
end_check = Vision('Needle\\agility\\seers\\end_check.png')

mark0 = Vision('Needle\\agility\\seers\\roof0_mark.png')
mark1 = Vision('Needle\\agility\\seers\\roof1_mark.png')
mark2 = Vision('Needle\\agility\\seers\\roof2_mark.png')
mark3 = Vision('Needle\\agility\\seers\\roof0_mark.png')
mark4 = Vision('Needle\\agility\\seers\\roof4_mark.png')

mark0_jump = Vision('Needle\\agility\\seers\\mark0_jump.png')
mark1_jump = Vision('Needle\\agility\\seers\\mark1_jump.png')
mark2_jump = Vision('Needle\\agility\\seers\\mark2_jump.png')
mark3_jump = Vision('Needle\\agility\\seers\\mark0_jump.png')
mark4_jump = Vision('Needle\\agility\\seers\\mark4_jump.png')

mark_list = [mark0, mark1, mark2, mark3, mark4]
mark_jumps = [mark0_jump, mark1_jump, mark2_jump, mark3_jump, mark4_jump]
mark_jump_threshold = [0.7, 0.64, 0.7, 0.7, 0.84]

current_roof = 5
mark_count = 0
dead_loop = 0
start_time = time.time()

def start0():
    global current_roof, dead_loop
    if current_roof == 5:
        if screen_right.contains(wall_start0, threshold=0.93):
            print('starting0... ')
            try:
                screen_right.click(wall_start0, threshold=0.93)
            except IndexError:
                print('clicking error')
                pass
            time.sleep(4.8)
            current_roof = 0
            dead_loop = 0
        elif screen_close.contains(wall_start3, threshold=0.9):
            print('starting3... ')
            try:
                screen_close.click(wall_start3, threshold=0.89)
            except IndexError:
                print('clicking error')
                pass
            time.sleep(4.8)
            current_roof = 0
            dead_loop = 0
    return current_roof

def start1():
    global current_roof, dead_loop
    if current_roof == 5:
        if screen_close.contains(wall_start1, threshold=0.98):
            print('starting1... ')
            try:
                screen_close.click(wall_start1, threshold=0.98)
            except IndexError:
                print('clicking error')
                pass
            time.sleep(4.8)
            current_roof = 0
            dead_loop = 0
    return current_roof

def start2():
    global current_roof, dead_loop
    if current_roof == 5:
        if screen_top.contains(wall_start2, threshold=0.63):
            print('starting2... ')
            try:
                screen_top.click(wall_start2, threshold=0.625)
            except IndexError:
                time.sleep(1.54)
                screen_top.click(wall_start2, threshold=0.625)
            time.sleep(4.8)
            current_roof = 0
            dead_loop = 0
        return current_roof
    
def first_jump():
    global current_roof, dead_loop
    if current_roof == 0:
        if screen_top.contains(first_gap, threshold=0.68):
            print('jumping first gap... ')
            screen_top.click(first_gap, threshold=0.67)
            time.sleep(6.05)
            current_roof = 1
            dead_loop = 0
    return current_roof

def tightrope_walk():
    global current_roof, dead_loop
    if current_roof == 1:
        if screen_bottom.contains(tightrope, threshold=0.69):
            print('walking tightrope... ')
            screen_bottom.click(tightrope, threshold=0.69)
            time.sleep(9.7)
            current_roof = 2
            dead_loop = 0
    return current_roof

def second_jump():
    global current_roof, dead_loop
    if current_roof == 2:
        if screen_bottom.contains(second_gap, threshold=0.65):
            print('jumping second gap... ')
            screen_bottom.click(second_gap, threshold=0.65)
            time.sleep(5.5)
            current_roof = 3
            dead_loop = 0
    return current_roof

def third_jump():
    global current_roof, dead_loop
    if current_roof == 3:
        if screen_bottom.contains(third_gap, threshold=0.73):
            print('jumping third gap... ')
            screen_bottom.click(third_gap, threshold=0.725)
            time.sleep(5.2)
            current_roof = 4
            dead_loop = 0
    return current_roof

def end_jump():
    global current_roof, dead_loop
    if current_roof == 4:
        if screen_bottom.contains(end_edge, threshold=0.71):
            print('jumping end gap... ')
            screen_bottom.click(end_edge, threshold=0.70)
            time.sleep(3.2)
            current_roof = 5
            dead_loop = 0
            
            current_time = (time.time() - start_time)
            current_time_format = time.strftime("%H:%M:%S", time.gmtime(current_time))
            print(f"run time: {current_time_format}")
            
            to_start.walk(within=3)
            time.sleep(0.2)
    return current_roof

def end_walk():
    global current_roof, dead_loop
    if current_roof == 5:
        to_start.walk(within=3)
    return True
        
        

def find_roof0():
    global current_roof
    print('finding current roof...')
    if screen_top.contains(wall_start0, threshold=0.94):
        current_roof = 5
    elif screen_top.contains(first_gap, threshold=0.71):
        current_roof = 0
    elif screen_bottom.contains(tightrope, threshold=0.69):
        current_roof = 1    
    elif screen_bottom.contains(second_gap, threshold=0.65):
        current_roof = 2
    elif screen_bottom.contains(third_gap, threshold=0.65):
        current_roof = 3
    elif screen_bottom.contains(end_edge, threshold=0.71):
        current_roof = 4
    elif screen_left.contains(fall1_check, threshold=0.65):
        to_start.walk(within=2)
        time.sleep(0.2)
        current_roof = 5
    elif screen_top.contains(fall_check, threshold=0.65):
        to_start.walk(within=2)
        time.sleep(0.2)
        current_roof = 5
    elif minimap.contains(end_check):
        to_start.walk(within=2)
        time.sleep(0.2)
        current_roof = 5
    else:
        current_roof = 5
    return current_roof

def find_roof1():
    global current_roof
    print('finding current roof...')
    if screen_top.contains(mark0_jump, threshold=0.94):
        print('0')
        screen.click(mark_jumps[0])
        current_roof += 1
    elif screen_top.contains(mark1_jump, threshold=0.71):
        print('1')
        screen.click(mark_jumps[1])
        current_roof += 1
    elif screen_bottom.contains(mark2_jump, threshold=0.71):
        print('2')
        screen.click(mark_jumps[2])
        current_roof += 1
    elif screen_bottom.contains(third_gap, threshold=0.71):
        print('3')
        screen.click(mark_jumps[3])
        current_roof += 1
    elif screen_bottom.contains(mark4_jump, threshold=0.84):
        print('4')
        screen.click(mark_jumps[4])
        current_roof += 1
    return current_roof
    
def marks():
    global current_roof, mark_count, dead_loop
    for i in range(0,5):
        if i == current_roof:
            if screen.contains(mark_list[i],threshold=0.81):
                time.sleep(.59)
                screen.click(mark_list[i],threshold=0.81)
                print(f'collecting mark {i}')
                time.sleep(4)
                screen.wait_for(mark_jumps[i], mark_jump_threshold[i])
                print('jump found')
                screen.click(mark_jumps[i], mark_jump_threshold[i])
                time.sleep(4.5)
                mark_count += 1
                print(f'marks collected: {mark_count}')
                current_roof += 1
                dead_loop = 0
                if current_roof == 5:
                    to_start.walk()
                    time.sleep(1)
                    
            return current_roof


find_roof0()

while True:

    start0()
    start1()
    start2()
    time.sleep(0.1)
    marks()
    first_jump()
    time.sleep(0.14)
    marks()
    time.sleep(.35)
    tightrope_walk()
    marks()
    second_jump()
    marks()
    third_jump()
    marks()
    time.sleep(.5)
    end_jump()
    
    dead_loop += 1
    if dead_loop > 6:
        find_roof0()
    if dead_loop > 10:
        find_roof1()
    if dead_loop > 10:
        to_start.walk(within=2)
        time.sleep(0.24)
        dead_loop = 0
    
    print('loop')
    time.sleep(.5)