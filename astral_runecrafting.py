import time
import random
from bank import Bank
from player import Player
from vision import Vision
from webwalking import WebWalking
from interactions import Interactions
from numpy import array
from windowcapture import WindowCapture


#instantiate all the objects required
#different click regions
inventory = Interactions(area='inventory')
left_inventory = Interactions(area='left_inventory')
screen = Interactions()
screen_left = Interactions(area='screen_left')
bank = Interactions(area='bank')
chatbox = Interactions(area='chatbox')
run_orb = WindowCapture(area='health_orb')

#webwalking paths
to_altar = WebWalking('walking_lists\\astral_altar.pkl','map\\lunar_isle_map.png')
to_bank = WebWalking('walking_lists\\to_lunar_bank.pkl','map\\lunar_isle_map.png')

bank1 = Bank('Needle\\lunar_bank_close.png')
bank2 = Vision('Needle\\lunar_bank.png') #0.81 threshold 
altar = Vision('Needle\\lunar_altar.png')
xbank = Vision('Needle\\x_bank.png')
spellbook = Vision('Needle\\magic_tab.png')
bag = Vision('Needle\\bag_tab.png')
dark_mage = Vision('Needle\\dark_mage.png')

withdraw1 = Vision('Needle\\withdraw1.png')
withdraw_all = Vision('Needle\\withdraw_all.png')
empty_pouch = Vision('Needle\\empty_pouch.png')
tap_here = Vision('Needle\\tap_here_to_continue.png')

teleport_to_moonclan = Vision('Needle\\teleport_to_moonclan.png')
npc_contact = Vision('Needle\\npc_contact.png')
player = Player()
bank_region = array([(924,474,52,71)])

#items
essence = Vision('Needle\\pure_essence.png')
cosmic_rune = Vision('Needle\\cosmic_rune.png')
lobster = Vision('Needle\\lobster.png')

small_pouch = Vision('Needle\\small_pouch.png')
med_pouch = Vision('Needle\\med_pouch.png')
large_pouch = Vision('Needle\\large_pouch.png')
huge_pouch = Vision('Needle\\huge_pouch.png')

broken_large = Vision('Needle\\broken_large_pouch.png')
broken_huge = Vision('Needle\\broken_huge_pouch.png')

stamina1 = Vision('Needle\\stamina1.png')

def fix_pouches(broken_type):
    '''
    checks for broken pouch: broken_type
    '''
    if inventory.contains(broken_type, threshold=0.65):
        print('repairing pouches...')
        screen.click(spellbook)
        time.sleep(.4)
        left_inventory.click(npc_contact)
        time.sleep(.3)
        screen.click(dark_mage, threshold=0.87)
        chatbox.wait_for(tap_here)
        chatbox.click(tap_here)
        chatbox.wait_for(tap_here)
        chatbox.click(tap_here)
        chatbox.wait_for(tap_here)
        chatbox.click(tap_here)
        screen.click(bag)
        print('pouches repaired...')

#setup
#zoom 3

#WebWalking('walking_lists\\to_lunar_bank.pkl','map\\lunar_isle_map.png').get_path("lunar_bank")

#TODO: make it unbreakable

start_time = time.time()
astral_count = 0

fix_pouches(broken_huge)

while True:
    #time.sleep(10)
    #banking
    while screen.contains(xbank) == False:
        bank1.findbank()
        time.sleep(0.14)
        
    if player.health() < 34:
        hp = player.health()
        print(f'hp: {hp}')
        bank1.withdraw(lobster)
        screen.click(xbank)
        
        for i in range(random.randint(5, 8)):
            inventory.click(lobster)
            time.sleep(random.normalvariate(.45, .03))
            
        while screen.contains(xbank) == False:
            bank1.findbank()
            time.sleep(0.14)
            
        inventory.click(lobster)
        
    bank1.withdraw(essence, threshold=0.81)
    time.sleep(random.normalvariate(0.2, 0.02))
    screen.click(xbank)
    
    inventory.fast_click(huge_pouch)
    time.sleep(0.6)
    fix_pouches(broken_huge)
    
    screen.click_region(bank_region)
    time.sleep(0.84)
           
    #stamina check and withdraw
    if player.run() <= 40:
        print(f'run energy: {player.run()}')
        if screen.contains(stamina1, threshold=0.60):
            screen.click(withdraw1)
            bank1.withdraw(stamina1, threshold=0.60)
            time.sleep(random.normalvariate(.1,.01))
            screen.click(withdraw_all)
        
    bank1.withdraw(essence, threshold=0.81)
    time.sleep(random.normalvariate(0.4, 0.02))
    screen.click(xbank)
    
    if inventory.contains(stamina1, threshold=0.71):
        inventory.fast_click(stamina1)
        time.sleep(random.normalvariate(0.42, 0.05))
        
    inventory.fast_click(small_pouch)
    time.sleep(random.normalvariate(0.21, 0.01))
    inventory.fast_click(med_pouch)
    time.sleep(random.normalvariate(0.2, 0.01))
    inventory.fast_click(large_pouch)
    time.sleep(random.normalvariate(0.64, 0.02)) 
    
    fix_pouches(broken_huge)
    
    #broken large pouch check and solve (if below 75)
    # if inventory.contains(broken_large, threshold=0.65):
    #     print('repairing pouches...')
    #     # for no rune pouch
    #     # while screen.contains(xbank) == False:
    #     #     bank1.findbank()
    #     #     time.sleep(0.14)
            
    #     # bank1.withdraw(cosmic_rune)
    #     # time.sleep(random.normalvariate(.1,.01))
    #     # screen.click(xbank)
    #     screen.click(spellbook)
    #     time.sleep(.4)
    #     left_inventory.click(npc_contact)
    #     time.sleep(.3)
    #     screen.click(dark_mage, threshold=0.87)
    #     time.sleep(4.8)
    #     chatbox.fast_click(tap_here)
    #     time.sleep(random.normalvariate(0.72, 0.01))
    #     chatbox.fast_click(tap_here)
    #     time.sleep(random.normalvariate(0.76, 0.01))
    #     chatbox.fast_click(tap_here)
    #     screen.click(bag)
    #     print('pouches repaired...')
            
    screen.click_region(bank_region)
    time.sleep(random.normalvariate(0.85, 0.02))
    #time.sleep(random.normalvariate(0.1, 0.02))
    
    # when no rune pouch    
    # if inventory.contains(cosmic_rune):
    #     inventory.click(cosmic_rune)
        
    if inventory.contains(stamina1):
        inventory.click(stamina1)
    bank1.withdraw(essence, threshold=0.83)
    time.sleep(random.normalvariate(0.35, 0.02))
    
    #walk to altar
    print('walking to astral altar...')
    to_altar.walk(5)
    time.sleep(random.normalvariate(.44, 0.02))
    #craft runes at altar
    screen.click(altar)
    
    time.sleep(random.uniform(1.95,1.99))
    inventory.fast_click(huge_pouch, right_click=True)
    time.sleep(0.05)
    screen.click(empty_pouch) 
    
    screen.click(altar)
    
    #mandatory sleep waiting for runes to craft
    time.sleep(random.uniform(1.9,1.92))
    time.sleep(0.66)
    
    inventory.fast_click(med_pouch, right_click=True)
    time.sleep(0.05)
    screen.click(empty_pouch) 
    inventory.fast_click(small_pouch, right_click=True)
    time.sleep(0.25)
    screen.click(empty_pouch) 
    #inventory.click(med_pouch)    
    inventory.fast_click(large_pouch, right_click=True)
    time.sleep(0.25)
    screen.click(empty_pouch) 
    
    time.sleep(.1)
    
    # if inventory.amount(essence, threshold=0.7) < 4:
    #     print('failed to empty pouches...')
        
    #     inventory.fast_click(med_pouch, right_click=True)
    #     time.sleep(0.05)
    #     screen.click(empty_pouch) 
    #     inventory.fast_click(small_pouch, right_click=True)
    #     time.sleep(0.25)
    #     screen.click(empty_pouch) 
    #     #inventory.click(med_pouch)    
    #     inventory.fast_click(broken_large, right_click=True)
    #     time.sleep(0.25)
    #     screen.click(empty_pouch) 
    # else:   
    #     print('pouches emptied...')
        
    #inventory.click(huge_pouch)
    
    screen.click(altar)
    #mandatory sleep waiting for runes to craft
    time.sleep(random.uniform(1.85,1.92))
    
    #return to bank
    time.sleep(.25)
    screen.click(spellbook)
    time.sleep(0.15)
    left_inventory.wait_for(teleport_to_moonclan)
    if left_inventory.contains(teleport_to_moonclan,threshold=0.77):
        print('teleporting...')
        left_inventory.click(teleport_to_moonclan,threshold=0.76)
        time.sleep(random.normalvariate(.3, 0.02))
        screen.click(bag)
    else:
        screen.click(spellbook)
        print('opening tab fix...')
        left_inventory.wait_for(teleport_to_moonclan)
        left_inventory.click(teleport_to_moonclan)
        time.sleep(random.normalvariate(.3, 0.02))
        screen.click(bag)
        
    
    #checks if bank is visible from tele, else walks to bank and finds
    #mandatory sleep wait for teleport to complete
    time.sleep(random.normalvariate(2.2, 0.02))
    if screen.contains(bank2, threshold=0.68) == True:
        screen.click(bank2, threshold=0.68)
        #walk to bank
        screen.wait_for(xbank)
    else:
        screen.wait_for(bank2, threshold=0.68)
        screen.wait_for(bank2, threshold=0.68)
        screen.wait_for(bank2, threshold=0.68)
        screen.click(bank2, threshold=0.68)
        #walk to bank
        screen.wait_for(xbank)
        
        
    #info for script user
    astral_count += 50
    print(f'astrals made: {astral_count}')
    profit = astral_count * 151
    print(f'profit: {profit}')
    
    #run time and format    
    current_time = (time.time() - start_time)
    current_time_format = time.strftime("%H:%M:%S", time.gmtime(current_time))
    print(f"run time: {current_time_format}")
    
    profit_hr = ((3600/current_time) * profit)
    print(f'profit/hr: {profit_hr}')