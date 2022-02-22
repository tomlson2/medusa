import time
import random
from webwalking import WebWalking
from player import Player
from vision import Vision
from windowcapture import InventoryRegion, WindowCapture, ScreenRegion


inventory = InventoryRegion()
screen = ScreenRegion()
player = Player()

potato = Vision('Needle\\sandcrab\\potato.png')
attack_potion = Vision('Needle\\sandcrab\\attack4.png')
strength_potion = Vision('Needle\\sandcrab\\strength4.png')
strength1 = Vision('Needle\\sandcrab\\strength1.png')
attack1 = Vision('Needle\\sandcrab\\attack1.png')
spec_button = Vision('Needle\\sandcrab\\spec_button.png')

#3 spot south center
to_away1 = WebWalking('walking_lists\\reset_crab1.pkl','map\\sandcrab_isle.png')
to_crab1 = WebWalking('walking_lists\\to_crab1.pkl','map\\sandcrab_isle.png')
#4 spot west south
to_crab2 = WebWalking('walking_lists\\to_crab2.pkl','map\\sandcrab_isle.png')
to_away2 = WebWalking('walking_lists\\reset_crab2.pkl','map\\sandcrab_isle.png')

start_time = time.time()
crab_timer = time.time()
potion_timer = time.time()
spec_timer = time.time() 

def run_timer():
    current_time = (time.time() - start_time)
    current_time_format = time.strftime("%H:%M:%S", time.gmtime(current_time))
    print(f"run time: {current_time_format}")

# WebWalking('walking_lists\\to_crab2.pkl','map\\sandcrab_isle.png').get_path("to_crab2")
# print('done')
# time.sleep(10)

spec = True
if screen.contains(spec_button, threshold=0.97):
    print('spec found')
    spec = True
else:
    print('spec not found')
    spec = False

# choose crab spot:    
crab_walk = to_crab2
walk_away = to_away2

print('-----starting crab killer-----')
while True:
    time.sleep(10)

    if player.health() < 10:
        for i in range(2):
            print('eating food...')
            if inventory.contains(potato):
                inventory.fast_click(potato)
                time.sleep(random.normalvariate(0.8, 0.13))
    
    if (time.time() - potion_timer) >= 420:
        print('drinking potions...')
        if inventory.contains(attack1, threshold=0.80):
            inventory.fast_click(attack1, threshold=0.80)
        elif inventory.contains(attack_potion, threshold=0.85):
            inventory.fast_click(attack_potion, threshold=0.85)
        time.sleep(1.8)
        if inventory.contains(strength1, threshold=0.80):
            inventory.fast_click(strength1, threshold=0.80)
        elif inventory.contains(strength_potion, threshold=0.85):
            inventory.fast_click(strength_potion, threshold=0.85)
        time.sleep(.2)
        
        potion_timer = time.time()
        
    if (time.time() - crab_timer) >= 600:
        print('refreshing crab agro...')
        walk_away.walk(within=3)
        crab_walk.walk(within=3)
        crab_timer = time.time()
        time.sleep(0.5)
        crab_walk.walk(within=1)
        run_timer()
        
    if (time.time() - spec_timer) >= 180 and spec == True:
        print('speccing...')
        screen.click(spec_button)
        
        spec_timer = time.time()