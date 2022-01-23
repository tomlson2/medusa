import time
import random
from webwalking import WebWalking
from player import Player
from vision import Vision
from windowcapture import InventoryRegion, WindowCapture


inventory = InventoryRegion()
player = Player()

potato = Vision('Needle\\sandcrab\\potato.png')
attack_potion = Vision('Needle\\sandcrab\\attack4.png')
strength_potion = Vision('Needle\\sandcrab\\strength4.png')

to_away = WebWalking('walking_lists\\reset_crab1.pkl','map\\sandcrab_isle.png')
to_crab1 = WebWalking('walking_lists\\to_crab1.pkl','map\\sandcrab_isle.png')
#to_crabs2 = WebWalking('walking_lists\\to_lunar_bank.pkl','map\\lunar_isle_map.png')

start_time = time.time()
crab_timer = time.time()
potion_timer = time.time()



while True:
    time.sleep(35)
    print('checking status...')

    if player.health() < 10:
        for i in range(2):
            print('eating food...')
            if inventory.contains(potato):
                inventory.fast_click(potato)
                time.sleep(random.normalvariate(0.8, 0.13))
    
    if (time.time() - potion_timer) >= 400:
        print('drinking potions...')
        if inventory.contains(attack_potion):
            inventory.fast_click(attack_potion)
        time.sleep(.2)
        if inventory.contains(strength_potion):
            inventory.fast_click(strength_potion)
        potion_timer = time.time()
        
    if (time.time() - crab_timer) >= 610:
        print('refreshing crab agro...')
        to_away.walk(within=5)
        to_crab1.walk(within=2)
        crab_timer = time.time()