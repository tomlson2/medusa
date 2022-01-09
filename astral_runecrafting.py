import time
import random
from bank import Bank
from player import Player
from vision import Vision
from webwalking import WebWalking
from interactions import Interactions
from numpy import array
from ocr import Numbers
from windowcapture import WindowCapture


#instantiate all the objects required
#different click regions
inventory = Interactions(area='inventory')
left_inventory = Interactions(area='left_inventory')
screen = Interactions()
bank = Interactions(area='bank')
run_orb = WindowCapture(area='run_orb')


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

teleport_to_moonclan = Vision('Needle\\teleport_to_moonclan.png')
npc_contact = Vision('Needle\\npc_contact.png')

run_energy = Numbers()
bank_region = array([(924,473,54,69)])


#items
essence = Vision('Needle\\pure_essence.png')
small_pouch = Vision('Needle\\small_pouch.png')
med_pouch = Vision('Needle\\med_pouch.png')
large_pouch = Vision('Needle\\large_pouch.png')
broken_large = Vision('Needle\\broken_large_pouch.png')



#setup
#zoom 3

#WebWalking('walking_lists\\to_lunar_bank.pkl','map\\lunar_isle_map.png').get_path("lunar_bank")

#TODO: fix shift click consistency
#TODO: add degradation checks and repair process
#TODO: add stamina pot support
#TODO: fix banking issues, 1 bank looks exact same but cant access
#TODO: make it unbreakable
#TODO: walk within region, multiple safe squares to end walk

inventory.hold_shift()
inventory.release_shift()

while True:
    
    #time.sleep(10)
    #banking
    
    bank1.withdraw(essence)
    time.sleep(random.normalvariate(0.4, 0.02))
    
    #stamina check and withdraw
    
    
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
    bank1.withdraw(essence)
    time.sleep(random.normalvariate(0.4, 0.02))
    
    
    #walk to altar
    to_altar.walk()
    time.sleep(random.normalvariate(.2, 0.02))
    #craft runes at altar
    screen.click(altar)
    
    #mandatory sleep waiting for runes to craft
    time.sleep(random.uniform(1.9,1.92))
    
    time.sleep(.34)
    
    
    inventory.shift_click(small_pouch)

    inventory.shift_click(med_pouch)
    
    inventory.shift_click(large_pouch)
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
        

    #inventory.click(large_pouch)
    #inventory.click(huge_pouch)
    time.sleep(random.normalvariate(.2, 0.02))
    
    screen.click(altar)
    #mandatory sleep waiting for runes to craft
    time.sleep(random.uniform(1.7,1.8))
    
    #return to bank
    screen.click(spellbook)
    time.sleep(random.normalvariate(.68, 0.02))
    left_inventory.click(teleport_to_moonclan)
    time.sleep(random.normalvariate(.3, 0.02))
    screen.click(bag)
    
    
    #checks if bank is visible from tele, else walks to bank and finds
    #mandatory sleep wait for teleport to complete
    time.sleep(random.normalvariate(2.2, 0.02))
    if screen.contains(bank2, threshold=0.68) == True:
        screen.click(bank2, threshold=0.68)
        #walk to bank
        time.sleep(4)
    else:
        to_bank.walk()
        bank1.findbank
    
    inventory.hold_shift()   
    inventory.release_shift()
    

    
    
    
    
    

    