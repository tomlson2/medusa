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
bank = Interactions(area='bank')
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

teleport_to_moonclan = Vision('Needle\\teleport_to_moonclan.png')
npc_contact = Vision('Needle\\npc_contact.png')
player = Player()
bank_region = array([(924,473,54,69)])

#items
essence = Vision('Needle\\pure_essence.png')
small_pouch = Vision('Needle\\small_pouch.png')
med_pouch = Vision('Needle\\med_pouch.png')
large_pouch = Vision('Needle\\large_pouch.png')
broken_large = Vision('Needle\\broken_large_pouch.png')

stamina1 = Vision('Needle\\stamina1.png')
stamina2 = Vision('Needle\\stamina2.png')
stamina3 = Vision('Needle\\stamina3.png')
stamina4 = Vision('Needle\\stamina4.png')

#setup
#zoom 3

#WebWalking('walking_lists\\to_lunar_bank.pkl','map\\lunar_isle_map.png').get_path("lunar_bank")

#TODO: fix shift click consistency
#TODO: add degradation checks and repair process
#TODO: add stamina pot support
#TODO: fix banking issues, 1 bank looks exact same but cant access
#TODO: make it unbreakable


while True:
    #time.sleep(10)
    #banking
    while screen.contains(xbank) == False:
        bank1.findbank()
        time.sleep(0.14)
    
    #stamina check and withdraw
    if player.run() <= 30:
        print(player.run())
        if screen.contains(stamina1, threshold=0.70):
            screen.click(withdraw1)
            bank1.withdraw(stamina1, threshold=0.70)
            time.sleep(random.normalvariate(.1,.01))
            screen.click(withdraw_all)
        
        bank1.withdraw(essence)
        time.sleep(random.normalvariate(0.4, 0.02))
        screen.click(xbank)
    
        inventory.click(stamina1)
        time.sleep(random.normalvariate(0.4, 0.05))
        inventory.click(small_pouch)
        time.sleep(random.normalvariate(0.18, 0.01))
        inventory.click(med_pouch)
        time.sleep(random.normalvariate(0.08, 0.01))
        inventory.click(large_pouch)
        time.sleep(random.normalvariate(0.6, 0.02))
    else:
        bank1.withdraw(essence)
        time.sleep(random.normalvariate(0.4, 0.02))
    
        screen.click(xbank)
        time.sleep(random.normalvariate(0.4, 0.05))
        inventory.click(small_pouch)
        time.sleep(random.normalvariate(0.18, 0.01))
        inventory.click(med_pouch)
        time.sleep(random.normalvariate(0.08, 0.01))
        inventory.click(large_pouch)
        time.sleep(random.normalvariate(0.6, 0.02))
    
    #broken pouch check and solve
    if inventory.contains(broken_large):
        screen.click(spellbook)
        time.sleep(.2)
        left_inventory.click(npc_contact)
        time.sleep(.2)
        screen.click(dark_mage)
        time.sleep(2.6)
        
    #screen.click_region(bank_region)
    #time.sleep(random.normalvariate(0.1, 0.02))
    while screen.contains(xbank) == False:
        bank1.findbank()
        time.sleep(0.14)
        
    if inventory.contains(stamina1):
        inventory.click(stamina1)
    bank1.withdraw(essence)
    time.sleep(random.normalvariate(0.4, 0.02))
    
    #walk to altar
    to_altar.walk(5)
    time.sleep(random.normalvariate(.2, 0.02))
    #craft runes at altar
    screen.click(altar)
    
    #mandatory sleep waiting for runes to craft
    time.sleep(random.uniform(1.9,1.92))
    time.sleep(.54)
    
    inventory.hold_shift()
    time.sleep(.1)
    inventory.click(small_pouch)
    inventory.click(med_pouch)    
    inventory.click(large_pouch)
    inventory.release_shift()
    time.sleep(.3)
    
    if inventory.amount(essence, threshold=0.7) < 4:
        print('failed to empty pouches...')
        inventory.release_shift()
        time.sleep(.25)
        inventory.shift_click(small_pouch)
        inventory.shift_click(med_pouch)
        inventory.shift_click(large_pouch)
    else:   
        print('pouches emptied...')
        
    #inventory.click(huge_pouch)
    
    screen.click(altar)
    #mandatory sleep waiting for runes to craft
    time.sleep(random.uniform(1.7,1.8))
    
    #return to bank
    screen.click(spellbook)
    time.sleep(random.normalvariate(.58, 0.02))
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
    

    
    
    
    
    

    