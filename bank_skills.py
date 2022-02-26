from windowcapture import InventoryRegion, ScreenRegion
import time
import random
from numpy import array
from vision import Vision


'''
west GE
full zoom
withdraw set to x (14)
everything in own tab
'''


screen = ScreenRegion()
inventory = InventoryRegion()

bank = Vision('Needle\\bank_skills\\compost\\ge_bank.png')
x = Vision('Needle\\bank_skills\\compost\\x.png')
deposit = Vision('Needle\\bank_skills\\compost\\deposit.png')
compost = Vision('Needle\\bank_skills\\compost\\compost.png')
saltpetre = Vision('Needle\\bank_skills\\compost\\saltpetre.png')

headless = Vision('Needle\\bank_skills\\fletching\\headless.png')
steel_tip = Vision('Needle\\bank_skills\\fletching\\steel_tip.png')

make_region = array([(485,122,199,143)])

def run_timer():
    current_time = (time.time() - start_time)
    current_time_format = time.strftime("%H:%M:%S", time.gmtime(current_time))
    print(f"run time: {current_time_format}")

def saltpetre_compost():
    while screen.contains(x) == False:
        if screen.contains(bank, threshold=0.75):
            screen.click(bank, threshold=0.75)
            time.sleep(0.7)
            screen.click(deposit)
            time.sleep(random.normalvariate(0.64, 0.004))
        else:
            screen.wait_for(bank, threshold=0.75)
    
    time.sleep(0.44)    
    screen.click(compost,1)
    time.sleep(random.normalvariate(0.31, 0.002))
    screen.click(saltpetre,1)
    time.sleep(random.normalvariate(0.44, 0.004))
    screen.click(x)
    
    time.sleep(random.normalvariate(.5, 0.03))
    
    print('making compost...')
    inventory.click(compost, ind=-1)
    time.sleep(random.normalvariate(0.32, 0.004))
    inventory.click(saltpetre)
    time.sleep(random.normalvariate(33, 0.24))
    
    screen.click(bank, threshold=0.75)
    time.sleep(0.9)
    screen.click(deposit)
    inventory.wait_for(compost) == False
    time.sleep(0.62)
    
def arrow_tip(arrow_tip):
    inventory.click(headless, threshold=0.85)
    time.sleep(random.uniform(0.384, 0.47))
    inventory.click(arrow_tip, threshold=0.85)
    time.sleep(random.uniform(0.79, 0.91))
    screen.click_region(make_region)
    time.sleep(12.9)


start_time = time.time()
print('starting script...')

while True:
    
    saltpetre_compost()
    
    run_timer()