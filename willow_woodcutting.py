import time
import random
from player import Player
from vision import Vision
from windowcapture import InventoryRegion, ChatboxRegion, MinimapRegion, CustomRegion, ScreenRegion, WindowCapture


'''
go to triple willow spot north of barbarian outpost tp
north full up
2 zoom (middle), 2 brightness (middle)
inventory open, TAP DROP MODE ON
'''


player = Player()
inventory = InventoryRegion()
chatbox = ChatboxRegion()

tree_right_region = CustomRegion(972,343,285,261)
tree_bottom_region = CustomRegion(757,577,324,268)
tree_left_region = CustomRegion(675,374,232,259)

willow_log = Vision('Needle\\woodcutting\\willows\\willow_log.png')

tree_r = Vision('Needle\\woodcutting\\willows\\tree_right.png')
tree_b = Vision('Needle\\woodcutting\\willows\\tree_bottom.png')
tree_l = Vision('Needle\\woodcutting\\willows\\tree_left.png')

tap_here = Vision('Needle\\tap_here_to_continue.png')

start_time = time.time()


print('------starting willow woodcutting------')
while True:
    
    while inventory.amount(willow_log, 0.7) < 27:
        print(f'log count: {inventory.amount(willow_log, 0.7)}')
        
        if tree_right_region.contains(tree_r, 0.63):
            tree_right_region.click(tree_r, 0.63)
            # sleep so mouse click confirmation doesnt cover the tree
            time.sleep(1.25)
            while tree_right_region.contains(tree_r, 0.63):
                time.sleep(1.5)
                if chatbox.contains(tap_here):
                    break
                elif inventory.amount(willow_log, 0.7) > 26:
                    break
            
        elif tree_bottom_region.contains(tree_b, 0.63):
            tree_bottom_region.click(tree_b, 0.63)
            time.sleep(1.25)
            while tree_bottom_region.contains(tree_b, 0.63):
                time.sleep(1.5)
                if chatbox.contains(tap_here):
                    break
                elif inventory.amount(willow_log, 0.7) > 26:
                    break
        
        elif tree_left_region.contains(tree_l, 0.63):
            tree_left_region.click(tree_l, 0.63)
            time.sleep(1.25)
            while tree_left_region.contains(tree_l, 0.63):
                time.sleep(1.5)
                if chatbox.contains(tap_here):
                    break
                elif inventory.amount(willow_log, 0.7) > 26:
                    break
            
        else:
            print('waiting for trees to respawn...')
            time.sleep(2.1)
    
    print('dropping logs...')
    inventory.drop_click(willow_log, inventory.amount(willow_log, 0.7))
    time.sleep(0.23)
        
    current_time = (time.time() - start_time)
    current_time_format = time.strftime("%H:%M:%S", time.gmtime(current_time))
    print(f"run time: {current_time_format}")