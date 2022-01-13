from numpy import empty, ndarray
from webwalking import WebWalking
from vision import Vision
from player import Player
from bank import Bank
from interactions import Interactions
from numpy import array
from wikiapi import Price
import time
import random


price = Price()

coal_price = price.load_price('Coal')
adamant_ore_price = price.load_price('Adamantite ore')
adamant_bar_price = price.load_price('Adamantite bar')
profit_per_adamant_bar = adamant_bar_price - ((coal_price * 3) + adamant_ore_price)
rune_ore_price = price.load_price('Runite ore')
rune_bar_price = price.load_price('Runite bar')
profit_per_rune_bar = rune_bar_price - ((coal_price * 4) + rune_ore_price)

inventory = Interactions(area='inventory')
screen = Interactions()
bank = Interactions(area='bank')
chatbox = Interactions(area='chatbox')

to_belt = WebWalking('walking_lists\\tobelt.pkl','map\\bf.png')
to_bank = WebWalking('walking_lists\\bank.pkl','map\\bf.png')
to_dispenser = WebWalking('walking_lists\\dispenser.pkl','map\\bf.png')

chest = Bank('Needle\\bchest.png', stam = True)

player = Player()

#chest = Vision('Needle\\bchest.png')
coal_bag = Vision('Needle\\cb.png')
coal = Vision('Needle\\coal.png')
fill_cb = Vision('Needle\\fcb.png')
empty_cb = Vision('Needle\\ecb.png')
rune_ore = Vision('Needle\\rune_ore.png')
rune_bar = Vision('Needle\\rune_bar.png')
make_rune_bars = Vision('Needle\\make_rune_bars.png')
adamant_ore = Vision('Needle\\adamant_ore.png')
make_adamant_bars = Vision('Needle\\make_adamant.png')
addy_bar = Vision('Needle\\addy_bar.png')


belt = array([(1097,569,65,58)])
dispenser = array([(1090,529,106,93)])

bars = 0
start = time.time()

def anticheat_sleep():
    time.sleep(random.normalvariate(0.25,0.02))

def click_sleep():
    time.sleep(random.normalvariate(0.15,0.01))

def empty_bag():
    inventory.click(coal_bag,1,right_click=True)
    screen.click(empty_cb,1)
    inventory.wait_for(coal)

def fill_bag():
    chest.findbank()
    inventory.click(coal_bag,1,right_click=True)
    screen.click(fill_cb,1)

def put_ore_on():
    print("PUTTING ORE ON")
    if inventory.contains(coal,0.7) or inventory.contains(adamant_ore,0.7):
        screen.click_region(belt)
        empty_bag()
        screen.click_region(belt)
        while inventory.contains(coal,0.7):
            pass
    # if inventory.contains(coal,0.7) or inventory.contains(adamant_ore,0.7):
    #     if to_belt.end_of_path() == True:
    #         screen.click_region(belt)
    #     else:
    #         to_belt.walk()
    #         screen.click_region(belt)

def take_bars(make_bars):
    print("TAKING BARS")
    screen.click_region(dispenser)
    try:
        chatbox.wait_for(make_bars)
        chatbox.click(make_bars,0.8)
    except IndexError:
        to_dispenser.walk()
        screen.click_region(dispenser)
        chatbox.click(make_bars,0.8)

def ore_trip(ore, make_bars, disp=False, bars = bars):
    chest.withdraw(ore, 1)
    fill_bag()
    to_belt.walk()
    put_ore_on()
    if disp == True:
        to_dispenser(make_bars)
        take_bars()
        to_bank.walk(within=2)
        bars = bars + inventory.amount(rune_bar, 0.7)

        print(time.strftime("%H:%M:%S. ", time.gmtime(time.time()-start)) + 
            str(bars) + " bars made. " + str(round((bars/(time.time()-start)*3600))) + 
            " bars/hour | " + str(bars * profit_per_rune_bar) + "gp profit // " + 
            str(round(((bars/(time.time()-start)*3600) * profit_per_rune_bar) - 120000)) + 
            "gp profit/hr.")
        
        chest.deposit(rune_bar, 1)
    else:
        to_bank.walk(within=2)
    
    return bars
        
def coal_trip(make_bars, disp = False, bars = bars):
    chest.withdraw(coal, 1)
    fill_bag()
    to_belt.walk()
    put_ore_on()
    if disp == True:
        to_dispenser.walk()
        take_bars(make_bars)
        to_bank.walk(within=2)
        bars = bars + inventory.amount(rune_bar, 0.7)
        
        print(time.strftime("%H:%M:%S. ", time.gmtime(time.time()-start)) + 
            str(bars) + " bars made. " + str(round((bars/(time.time()-start)*3600))) + 
            " bars/hour | " + str(bars * profit_per_rune_bar) + "gp profit // " + 
            str(round(((bars/(time.time()-start)*3600) * profit_per_rune_bar) - 120000)) + 
            "gp profit/hr.")

        chest.deposit(rune_bar, 1)
    else:
        to_bank.walk(within=2)
    
    return bars



def adamant():
    start = time.time()
    while True:
        to_bank.walk(within=2)
        chest.withdraw(adamant_ore, 1)
        fill_bag()
        to_belt.walk()
        put_ore_on()
        to_bank.walk(within=2)
        chest.withdraw(coal, 1)
        fill_bag()
        to_belt.walk()
        put_ore_on()
        to_dispenser.walk()
        take_bars(make_adamant_bars)
        to_bank.walk(within=2)
        bars = bars + inventory.amount(addy_bar,0.7)
        print(time.strftime("%H:%M:%S. ", time.gmtime(time.time()-start)) + str(bars) + " bars made. " + str(round((bars/(time.time()-start)*3600))) + " bars/hour | " + str(bars * profit_per_adamant_bar) + "gp profit // " + str(round((bars/(time.time()-start)*3600) * profit_per_adamant_bar)) + "gp profit/hr.")
        chest.deposit(addy_bar,1)

def rune():
    to_bank.walk(within = 2)
    coal_trip(make_rune_bars)
    coal_trip(make_rune_bars)
    bars = 0
    while True:
        bars = ore_trip(rune_ore, make_rune_bars, bars = bars)
        bars = coal_trip(make_rune_bars,disp=True, bars = bars)
        bars = ore_trip(rune_ore, make_rune_bars, bars = bars)
        bars = coal_trip(make_rune_bars, disp=True, bars = bars)
        bars = coal_trip(make_rune_bars, bars = bars)

rune()

        

        
