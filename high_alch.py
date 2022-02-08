import time
import random
from vision import Vision
from windowcapture import ScreenRegion, InventoryRegion

'''
high alchs air bstaffs
have everything in inventory
have spellbook open
'''

high_alch = Vision('Needle\\magic\\high_alch\\high_alch.png')
bstaff = Vision('Needle\\magic\\high_alch\\bstaff.png')

screen = ScreenRegion()
inventory = InventoryRegion()

alch_count = 0
start_time = time.time()

while True:
    
    screen.click(high_alch)
    time.sleep(random.normalvariate(0.25, 0.02))
    inventory.click(bstaff)
    time.sleep(random.normalvariate(2.1, 0.05))
    alch_count += 1
    
    
    if alch_count % 50 == 0:
        current_time = (time.time() - start_time)
        current_time_format = time.strftime("%H:%M:%S", time.gmtime(current_time))
        print(f"run time: {current_time_format}")
        
        print(f'alchs/hr: {alch_count * 3600/current_time}')