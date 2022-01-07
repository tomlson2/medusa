import time
import random
from bank import Bank
from player import Player
from vision import Vision
from webwalking import WebWalking
from interactions import Interactions
from numpy import array


#instantiate all the objects required
#different click regions
inventory = Interactions(area='inventory')
left_inventory = Interactions(area='left_inventory')
screen = Interactions()
bank = Interactions(area='bank')

#webwalking paths
to_altar = WebWalking('walking_lists\\astral_altar.pkl','map\\lunar_isle_map.png')
to_bank = WebWalking('walking_lists\\to_lunar_bank.pkl','map\\lunar_isle_map.png')

bank1 = Bank('Needle\\lunar_bank_close.png')
bank2 = Vision('Needle\\lunar_bank.png') #0.81 threshold 
altar = Vision('Needle\\lunar_altar.png')
xbank = Vision('Needle\\x_bank.png')
spellbook = Vision('Needle\\magic_tab.png')
bag = Vision('Needle\\bag_tab.png')
teleport_to_moonclan = Vision('Needle\\teleport_to_moonclan.png')
bank_region = array([(924,473,54,69)])

#items
essence = Vision('Needle\\pure_essence.png')
small_pouch = Vision('Needle\\small_pouch.png')




#setup
#zoom 3

#WebWalking('walking_lists\\to_lunar_bank.pkl','map\\lunar_isle_map.png').get_path("lunar_bank")


#TODO: add degradation checks and repair process

while True:
    
    #time.sleep(10)
    #banking
    
    
    
    bank1.withdraw(essence)
    time.sleep(random.normalvariate(0.1, 0.02))
    screen.click(xbank)
    time.sleep(random.normalvariate(0.4, 0.05))
    inventory.click(small_pouch)
    time.sleep(random.normalvariate(0.1, 0.02))
    screen.click_region(bank_region)
    time.sleep(random.normalvariate(0.1, 0.02))
    bank1.withdraw(essence)
    time.sleep(random.normalvariate(0.1, 0.02))
    screen.click(xbank)
    time.sleep(random.normalvariate(.2, 0.02))
    
    #walk to altar
    to_altar.walk()
    time.sleep(random.normalvariate(.2, 0.02))
    #craft runes at altar
    screen.click(altar)
    time.sleep(random.uniform(1.82,1.88))
    inventory.shift_click(small_pouch)
    #inventory.shift_click(med_pouch)
    #inventory.shift_click(large_pouch)
    #inventory.shift_click(huge_pouch)
    time.sleep(random.normalvariate(.2, 0.02))
    screen.click(altar)
    time.sleep(random.uniform(1.4,1.5))
    
    #return to bank
    screen.click(spellbook)
    time.sleep(random.normalvariate(.2, 0.02))
    left_inventory.click(teleport_to_moonclan)
    time.sleep(random.normalvariate(.2, 0.02))
    screen.click(bag)
    
    
    #checks if bank is visible from tele, else walks to bank and finds
    time.sleep(random.normalvariate(2.6, 0.02))
    if screen.contains(bank2, threshold=0.68) == True:
        screen.click(bank2, threshold=0.68)
    else:
        to_bank.walk()
        bank1.findbank
        
    time.sleep(4)
    
    
    
    
    

    