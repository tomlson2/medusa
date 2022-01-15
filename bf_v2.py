from numpy.core.multiarray import empty
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

chest = Bank('Needle\\bf_v2\\bank.png', stam = True)

player = Player()

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


belt_bank = array([(802,274,16,13)])
belt_close = array([(987,566,16,15)])
dispenser_belt = array([(883,704,19,19)])
dispenser_close = array([(984,556,26,22)])
bank_dispenser = array([(1312,821,34,23)])
bank_belt = array([(1188,987,28,16)])

start = time.time()
bars = 0

def anticheat_sleep():
    time.sleep(random.normalvariate(0.25,0.02))

def click_sleep():
    time.sleep(random.normalvariate(0.15,0.01))

def empty_bag():
    inventory.click(coal_bag,1,right_click=True)
    while(inventory.contains(coal,0.7) or inventory.contains(adamant_ore,0.7)):
        pass
    screen.click(empty_cb,.90)
    inventory.wait_for(coal)

def fill_bag():
    chest.findbank()
    inventory.click(coal_bag,1,right_click=True)
    screen.click(fill_cb,.90)

while True:
    chest.withdraw(adamant_ore,1)
    fill_bag()
    chest.close()
    screen.click_region(belt_bank)
    time.sleep(random.normalvariate(1,0.2))
    empty_bag()
    screen.click_region(belt_close)
    while(inventory.contains(coal,0.7) or inventory.contains(adamant_ore,0.7)):
        pass
    to_bank.walk()
    chest.withdraw(coal,1)
    fill_bag()
    screen.click_region(belt_bank)
    empty_bag()
    screen.click_region(belt_close)
    while(inventory.contains(coal,0.7) or inventory.contains(adamant_ore,0.7)):
        pass
    screen.click_region(dispenser_belt)
    chatbox.wait_for(make_adamant_bars,0.9)
    chatbox.click(make_adamant_bars,0.9)
    to_bank.walk()
    bars = bars + inventory.amount(addy_bar,0.7)
    print(f'{time.strftime("%H:%M:%S. ", time.gmtime(time.time()-start))} --- {bars} bars --- {round(bars/(time.time()-start)*3600)} bars/hr --- {round((bars/(time.time()-start)*3600) * profit_per_adamant_bar) - 120000} gp/hr')
    chest.deposit(addy_bar,1)
    
