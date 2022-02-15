import time
import random
from vision import Vision
from model import Model
from windowcapture import ScreenRegion, InventoryRegion, MinimapRegion, CustomRegion
from player import Player

print("Initializing")

screen = ScreenRegion()
screen_left = CustomRegion(964, 1028, 7, 41)
inventory = InventoryRegion()
minimap = MinimapRegion()
player = Player()

potato = Vision('Needle\\sandcrab\\potato.png')
seed_box = Vision('Needle\\thieving\\mf\\seed_box.png')
bank_area = Vision('Needle\\thieving\\mf\\bank_area.png')
to_mf = Vision('Needle\\thieving\\mf\\to_mf.png')
to_mf1 = Vision('Needle\\thieving\\mf\\to_mf1.png')
bank_booth = Vision('Needle\\thieving\\mf\\bank_booth.png')
click_check = Vision('Needle\\thieving\\mf\\mf_check.png')
x = Vision('Needle\\bank_skills\\compost\\x.png')
deposit = Vision('Needle\\bank_skills\\compost\\deposit.png')
master_farmer = Model('model_data\weights\master_famer_best.pt')
#bank_booth_model = Model('model_data\weights\bank_booth_best.pt')

xp = Vision('Needle\\thieving\\mf\\xp.png')

def look_for_mf():
    if screen.contains(master_farmer, threshold=0.55):
        return True
    else:
        print('looking for master farmer')
        screen.click(to_mf, threshold=0.72)
        time.sleep(3.8)
        if screen.contains(master_farmer, threshold=0.55):
            return True
        screen.click(to_mf1, threshold=0.70)
        print('looking west')
        time.sleep(2.7)
        if screen.contains(master_farmer, threshold=0.55):
            return True
        else:
            time.sleep(random.randint(2, 4))
            return look_for_mf()

bank_count = 0
dead_click_check = 0
start_time = time.time()
dodgy_timer = time.time()

while True:
    
    current_health = player.health()
    while player.health() >= current_health:
        try:
            screen.click(master_farmer, threshold=0.58)
            #changed from .1
            time.sleep(0.2)
            if screen.contains(click_check):
                dead_click_check = 0
            else:
                dead_click_check += 1
            if dead_click_check > 7:
                print('not pickpocketing master farmer\nkilling script')
                break
            time.sleep(0.3)
        except IndexError:
            print('master farmer not found')
            time.sleep(3)
            look_for_mf()
            
    if player.health() <= random.randint(20, 35):
        if inventory.contains(potato):
            time.sleep(random.normalvariate(0.5, 0.01))
            inventory.click(potato)
            time.sleep(random.normalvariate(3.0, 0.115))
            
        # bank
        else:
            time.sleep(random.normalvariate(3.22, 0.115))
            print('banking...')
            time.sleep(1)
            screen.click(bank_area, threshold=0.7)
            time.sleep(4)
            while screen.contains(x) == False:
                bank_count += 1
                try:
                    screen.click(bank_booth)
                    time.sleep(random.normalvariate(1.5, 0.03))
                    if bank_count > 4:
                        screen.click(bank_area)
                        time.sleep(random.normalvariate(1.21, 0.05))
                        bank_count = 0
                except IndexError:
                    pass
            time.sleep(random.normalvariate(.15, 0.02))
            screen.click(deposit)
            bank_count = 0
            time.sleep(random.normalvariate(.45, 0.02))
            screen_left.click(seed_box)
            time.sleep(random.normalvariate(.27, 0.02))
            for i in range(3):
                screen_left.click(potato)
                time.sleep(random.normalvariate(.07, 0.01))
            time.sleep(1.2)
            
            look_for_mf()    
            
            current_time = (time.time() - start_time)
            current_time_format = time.strftime("%H:%M:%S", time.gmtime(current_time))
            print(f"run time: {current_time_format}")
    else:
        time.sleep(random.normalvariate(3.42, 0.115))
        
    if dead_click_check > 4:
        look_for_mf()
        
    if dead_click_check > 7:
        print('not pickpocketing master farmer\nkilling script')
        break
        
