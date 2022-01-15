import time
import random
from webwalking import WebWalking
from interactions import Interactions
from player import Player
from bank import Bank
from vision import Vision


inventory = Interactions(area='inventory')

potato = Vision('Needle\\crabs\\potato.png')
attack_potion = Vision('Needle\\crabs\\attack4.png')
strength_potion = Vision('Needle\\crabs\\strength4.png')

to_away = WebWalking('walking_lists\\astral_altar.pkl','map\\lunar_isle_map.png')
to_crabs1 = WebWalking('walking_lists\\to_lunar_bank.pkl','map\\lunar_isle_map.png')
to_crabs2 = WebWalking('walking_lists\\to_lunar_bank.pkl','map\\lunar_isle_map.png')

start_time = time.time()
crab_timer = time.time()
potion_timer = time.time()

while True:

    if Player.health() < 20:
        for i in range(3):
            print('eating food...')
            inventory.fast_click(potato)
            time.sleep(random.normalvariate(0.8, 0.13))
    
    if (time.time() - potion_timer) >= 300:
        print('drinking potions...')
        inventory.fast_click(attack_potion)
        inventory.fast_click(strength_potion)
        potion_timer = time.time()
        
    if (time.time - crab_timer) >= 600:
        print('refreshing crab agro...')
        to_away.walk()
        to_crabs1.walk()