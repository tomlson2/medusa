import time
import random
from numpy import array
from vision import Vision
from webwalking import WebWalking
from player import Player
from windowcapture import ScreenRegion, CustomRegion, InventoryRegion, ChatboxRegion

'''
~17k xp/hr, 300k gp/hr
brightness 2, zoom 1, camera north, full up
start with full inv and fresh jewelry teleports
'''


screen = ScreenRegion()
inventory = InventoryRegion()

bank_chest = Vision('Needle\\runecrafting\\lava_runes\\bank_chest.png')
bank_chest1 = Vision('Needle\\runecrafting\\lava_runes\\bank_chest1.png')
bank_chest2 = Vision('Needle\\runecrafting\\lava_runes\\bank_chest2.png')
bank_chest3 = Vision('Needle\\runecrafting\\lava_runes\\bank_chest3.png')
bank_chest4 = Vision('Needle\\runecrafting\\lava_runes\\bank_chest4.png')
x = Vision('Needle\\runecrafting\\lava_runes\\x.png')
withdraw1 = Vision('Needle\\runecrafting\\lava_runes\\withdraw1.png')
withdraw_all = Vision('Needle\\runecrafting\\lava_runes\\withdraw_all.png')

essence = Vision('Needle\\runecrafting\\lava_runes\\pure_essence.png')
mud_rune = Vision('Needle\\runecrafting\\mud_runes\\mud_rune.png')
bneck = Vision('Needle\\runecrafting\\lava_runes\\binding_neck_bank.png')
digsite = Vision('Needle\\runecrafting\\mud_runes\\digsite_pendant.png')
water_tally = Vision('Needle\\runecrafting\\mud_runes\\water_tally.png')
duel_ring = Vision('Needle\\runecrafting\\lava_runes\\ring_of_dueling.png')
castle_wars = Vision('Needle\\runecrafting\\lava_runes\\castle_wars.png')
stam1 = Vision('Needle\\runecrafting\\lava_runes\\stam1.png')
rub_digsite = Vision('Needle\\runecrafting\\mud_runes\\rub_digsite.png')

fence = Vision('Needle\\runecrafting\\mud_runes\\fence.png')
earth_altar = Vision('Needle\\runecrafting\\mud_runes\\earth_altar.png')
earth_altar2 = Vision('Needle\\runecrafting\\mud_runes\\earth_altar2.png')

bag = Vision('Needle\\runecrafting\\lava_runes\\inventory.png')
equipment = Vision('Needle\\runecrafting\\lava_runes\\equipment.png')
to_bank = WebWalking('walking_lists\\to_bank_chest_cw.pkl','map\\castle_wars.png')
to_fence = WebWalking('walking_lists\\to_earth_altar_fence.pkl','map\\earth_altar.png')
to_altar = WebWalking('walking_lists\\to_earth_altar.pkl','map\\earth_altar.png')
minimap_earth_altar = array([(1710,78,30,42)])

player = Player()
start_time = time.time()

digsite_count = 0
rod_count = 0
bneck_count = 0
mud_count = 0

#WebWalking('walking_lists\\to_earth_altar.pkl','map\\earth_altar.png').get_path("to_earth_altar")
#print('done')
#time.sleep(10)  

while True:
    
    inventory.click(digsite, right_click=True)
    time.sleep(0.2)
    screen.click(rub_digsite, threshold=0.8)
    digsite_count += 1
    time.sleep(2.9)
    to_fence.walk(4)
    time.sleep(random.normalvariate(0.45,0.02))
    if screen.contains(fence):
        print('opening fence...')
        screen.click(fence)
        time.sleep(3)
        to_altar.walk(4)
    else:
        to_altar.walk(4)
        
    time.sleep(0.4)
    screen.click(earth_altar)
    time.sleep(2.1)
    screen.click_region(minimap_earth_altar)
    time.sleep(2)
    inventory.click(water_tally)
    time.sleep(random.normalvariate(1.9, 0.02))
    print('crafting runes...')
    screen.click(earth_altar2, threshold=0.8)
    mud_count += 25
    bneck_count += 1
    
    time.sleep(random.normalvariate(1.2, 0.06))
    screen.click(equipment)
    time.sleep(random.normalvariate(0.9, 0.003))
    inventory.click(duel_ring, right_click=True)
    time.sleep(random.normalvariate(0.31, 0.05))
    inventory.click(castle_wars)
    rod_count += 1
    time.sleep(random.normalvariate(0.5, 0.05))
    screen.click(bag)
    time.sleep(1.5)
    
    # banking
    print('banking...')
    while screen.contains(x) == False:
        if screen.contains(bank_chest):
            screen.click(bank_chest)
            screen.wait_for(x)
            time.sleep(0.2)
        elif screen.contains(bank_chest1):
            screen.click(bank_chest1)
            screen.wait_for(x)
            time.sleep(0.2)
        elif screen.contains(bank_chest2):
            screen.click(bank_chest2)
            screen.wait_for(x)
            time.sleep(0.2)
        elif screen.contains(bank_chest3):
            screen.click(bank_chest3)
            screen.wait_for(x)
            time.sleep(0.2)
        elif screen.contains(bank_chest4):
            screen.click(bank_chest4)
            screen.wait_for(x)
            time.sleep(0.2)
        else:
            to_bank.walk(2)
            time.sleep(0.8)
            screen.click(bank_chest4)
            screen.wait_for(x)
            time.sleep(0.2)
            
    
    if inventory.contains(stam1):
        inventory.click(stam1)
        time.sleep(random.normalvariate(0.3, 0.07))
            
    if player.run() < 30:
        print('restoring run energy...')
        screen.click(withdraw1)
        time.sleep(random.normalvariate(0.32, 0.045))
        screen.click(stam1)
        time.sleep(random.normalvariate(0.311, 0.025))
        screen.click(withdraw_all)
        time.sleep(random.normalvariate(0.312, 0.035))
        mud_count -= 1
            
    if bneck_count > 15:
        print('replacing binding neck...')
        screen.click(withdraw1)
        time.sleep(random.normalvariate(0.32, 0.05))
        screen.click(bneck)
        time.sleep(random.normalvariate(0.33, 0.044))
        screen.click(withdraw_all)
        time.sleep(random.normalvariate(0.31, 0.02))
        bneck_count = 0
        mud_count -= 1
    
    if rod_count > 7:
        print('replacing ring of dueling...')
        screen.click(withdraw1)
        time.sleep(random.normalvariate(0.31, 0.03))
        screen.click(duel_ring)
        time.sleep(random.normalvariate(0.30, 0.04))
        screen.click(withdraw_all)
        time.sleep(random.normalvariate(0.45, 0.05))
        rod_count = 0
        mud_count -= 1
    
    if digsite_count > 4:
        print('replacing digsite pendant..')
        screen.click(withdraw1)
        time.sleep(random.normalvariate(0.34, 0.01))
        screen.click(digsite)
        time.sleep(random.normalvariate(0.30, 0.02))
        screen.click(withdraw_all)
        time.sleep(random.normalvariate(0.42, 0.05))
        digsite_count = 0
        mud_count -= 1
            
    time.sleep(0.15)
    screen.click(essence, threshold=0.95)
    time.sleep(random.normalvariate(0.37, 0.01))
    if inventory.contains(mud_rune):
        inventory.click(mud_rune)
    time.sleep(random.normalvariate(0.39, 0.04))
    screen.click(water_tally)
    time.sleep(random.normalvariate(0.324, 0.05))
    
    screen.click(x)
    time.sleep(random.normalvariate(0.4, 0.05))
    
    if inventory.contains(bneck):
        inventory.click(bneck)
        time.sleep(random.normalvariate(0.3, 0.05))
        
    if inventory.contains(duel_ring):
        inventory.click(duel_ring)
        time.sleep(random.normalvariate(0.3, 0.05))
        
    if inventory.contains(stam1):
        inventory.click(stam1)
        time.sleep(random.normalvariate(0.3, 0.05))
    
    current_time = (time.time() - start_time)
    current_time_format = time.strftime("%H:%M:%S", time.gmtime(current_time))
    print(f"run time: {current_time_format}")
    print(f'profit: {mud_count * 185}')
    print(f'xp/hr: {((3600/current_time) * (mud_count * 9.5))}')