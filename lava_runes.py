import time
import random
from numpy import array
from vision import Vision
from webwalking import WebWalking
from player import Player
from windowcapture import ScreenRegion, CustomRegion, InventoryRegion, ChatboxRegion

'''
~24k xp/hr, 2 hours to 44
brightness 2, zoom 1, camera north, full up
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
lava_rune = Vision('Needle\\runecrafting\\lava_runes\\lava_rune.png')
bneck = Vision('Needle\\runecrafting\\lava_runes\\binding_neck_bank.png')
earth_tally_bank = Vision('Needle\\runecrafting\\lava_runes\\earth_talisman_bank.png')
earth_tally = Vision('Needle\\runecrafting\\lava_runes\\earth_talisman.png')
duel_ring = Vision('Needle\\runecrafting\\lava_runes\\ring_of_dueling.png')
stam1 = Vision('Needle\\runecrafting\\lava_runes\\stam1.png')

bag = Vision('Needle\\runecrafting\\lava_runes\\inventory.png')
equipment = Vision('Needle\\runecrafting\\lava_runes\\equipment.png')
castle_wars = Vision('Needle\\runecrafting\\lava_runes\\castle_wars.png')
duel_arena = Vision('Needle\\runecrafting\\lava_runes\\duel_arena.png')

fire_altar = Vision('Needle\\runecrafting\\lava_runes\\fire_altar.png')
altar_entrance = Vision('Needle\\runecrafting\\lava_runes\\fire_entrance.png')
to_entrance = WebWalking('walking_lists\\to_entrance.pkl','map\\duel_arena.png')
to_bank = WebWalking('walking_lists\\to_bank_chest_cw.pkl','map\\castle_wars.png')

player = Player()

minimap_fire_altar = array([(1750,230,45,45)])
bank_fix = array([(912,662,109,83)])
start_time = time.time()

rod_count = 0
bneck_count = 0
lava_count = 0

print('******starting lava runecrafter******')
# WebWalking('walking_lists\\to_bank_chest_cw.pkl','map\\castle_wars.png').get_path("to_bank_chest_cw")
# print('done')
# time.sleep(10)

while True:
    
    if screen.contains(x):
        screen.click(x)
        
    time.sleep(random.normalvariate(1.2, 0.06))
    screen.click(equipment)
    time.sleep(random.normalvariate(0.4, 0.003))
    inventory.click(duel_ring, right_click=True)
    time.sleep(random.normalvariate(0.31, 0.05))
    inventory.click(duel_arena)
    time.sleep(random.normalvariate(0.51, 0.05))
    screen.click(bag)
    time.sleep(2)
    
    to_entrance.walk(3)
    time.sleep(0.32)
    screen.click(altar_entrance, threshold=0.65)
    time.sleep(2)
    screen.click_region(minimap_fire_altar)
    time.sleep(3)
    inventory.click(earth_tally)
    time.sleep(random.normalvariate(0.8, 0.05))
    if screen.contains(fire_altar, threshold=0.85):
        print('crafting lava runes...')
        screen.click(fire_altar, threshold=0.85)
        bneck_count += 1
        lava_count += 26
    else:
        break
    
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
        time.sleep(random.normalvariate(0.32, 0.05))
        screen.click(stam1)
        time.sleep(random.normalvariate(0.311, 0.05))
        screen.click(withdraw_all)
        time.sleep(random.normalvariate(0.312, 0.05))
        lava_count -= 1
            
    if bneck_count > 16:
        print('replacing binding neck...')
        screen.click(withdraw1)
        time.sleep(random.normalvariate(0.31, 0.05))
        screen.click(bneck)
        time.sleep(random.normalvariate(0.31, 0.05))
        screen.click(withdraw_all)
        time.sleep(random.normalvariate(0.31, 0.05))
        bneck_count = 0
        lava_count -= 1
        pass
    
    if rod_count > 3:
        print('replacing ring of dueling...')
        screen.click(withdraw1)
        time.sleep(random.normalvariate(0.31, 0.05))
        screen.click(duel_ring)
        time.sleep(random.normalvariate(0.31, 0.05))
        screen.click(withdraw_all)
        time.sleep(random.normalvariate(0.45, 0.05))
        rod_count = 0
        lava_count -= 1
        pass
    
    time.sleep(0.15)
    screen.click(essence, threshold=0.92)
    time.sleep(random.normalvariate(0.4, 0.04))
    inventory.click(lava_rune)
    time.sleep(random.normalvariate(0.41, 0.06))
    screen.click(earth_tally_bank)
    time.sleep(random.normalvariate(0.31, 0.05))
    
    screen.click(x)
    time.sleep(random.normalvariate(0.5, 0.05))

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
    print(f'xp/hr: {((3600/current_time) * (lava_count * 10.5))}')
