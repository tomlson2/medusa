import time
import random
from bank import Bank
from player import Player
from vision import Vision
from webwalking import WebWalking
from interactions import Interactions


#instantiate all the objects required
#different click regions
inventory = Interactions(area='inventory')
screen = Interactions()
bank = Interactions(area='bank')

#webwalking paths
to_altar = WebWalking('walking_lists\\astral_altar.pkl','map\\lunar_isle_map.png')
to_bank = WebWalking('walking_lists\\tobelt.pkl','map\\bf.png')

bank = Bank('Needle\\lunar_bank_close.png')
bank2 = Bank('Needle\\lunar_bank.png') #0.81 threshold 
altar = Vision('Needle\\lunar_altar.png')
xbank = Vision('Needle\\x_bank.png')

#items
essence = Vision('Needle\\pure_essence.png')
small_pouch = Vision('Needle\\small_pouch.png')




#setup
#zoom 3

#WebWalking('walking_lists\\to_altar.pkl','map\\lunar_isle_map.png').get_path("astral_altar")




while True:
    #banking
    # bank.findbank
    # time.sleep(random.normalvariate(0.1, 0.02))
    # bank.withdraw(essence)
    # time.sleep(random.normalvariate(0.1, 0.02))
    # screen.click(xbank)
    # time.sleep(random.normalvariate(1, 0.2))
    # inventory.click(small_pouch)
    # time.sleep(random.normalvariate(0.1, 0.02))
    # bank.findbank
    # time.sleep(random.normalvariate(0.1, 0.02))
    # bank.withdraw(essence)
    # time.sleep(random.normalvariate(0.1, 0.02))
    # screen.click(xbank)
    # time.sleep(random.normalvariate(10, 0.2))
    to_altar.walk()
    print("stop")

    pass