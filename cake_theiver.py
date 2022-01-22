import time
import random
from numpy import array
from vision import Vision
from windowcapture import InventoryRegion, ScreenRegion


'''
about ~15k xp/hr
stand under baker
zoom 2 (middle), camera north full up
inventory open and on drop mode
'''


inventory = InventoryRegion()
screen = ScreenRegion()
stall_region = array([(840,530,25,71)])

cake = Vision('Needle\\thieving\\cake_stall\\cake.png')
bread = Vision('Needle\\thieving\\cake_stall\\bread.png')
choco = Vision('Needle\\thieving\\cake_stall\\choco_cake.png')

start_time = time.time()


print('-------starting cake stall thieving-------')
while True:
    print('thieving stalls...')
    while inventory.amount(cake, 0.75) + inventory.amount(bread, 0.75) + inventory.amount(choco, 0.75) < 28:
        screen.click_region(stall_region)
        time.sleep(random.normalvariate(3.3, 0.08))
        
    print('dropping junk...')
    inventory.drop_click(cake, inventory.amount(cake, 0.75))
    time.sleep(0.26)
    inventory.drop_click(bread, inventory.amount(bread, 0.75))
    time.sleep(0.32)
    inventory.drop_click(choco, inventory.amount(choco, 0.75))
    
    current_time = (time.time() - start_time)
    current_time_format = time.strftime("%H:%M:%S", time.gmtime(current_time))
    print(f"run time: {current_time_format}")
    
    time.sleep(1.2)