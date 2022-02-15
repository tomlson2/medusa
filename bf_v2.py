from pandas.core.indexes.base import Index
from webwalking import WebWalking
from vision import Vision
from player import Player
from bank import Bank
from windowcapture import BankRegion, ChatboxRegion, InventoryRegion, ScreenRegion
from numpy import array
from wikiapi import Price
import time
import random


price = Price()

coal_price = price.load_price('Coal')
iron_ore_price = price.load_price('Iron ore')
steel_bar_price = price.load_price('Steel bar')
profit_per_steel_bar = steel_bar_price - (coal_price + iron_ore_price)

adamant_ore_price = price.load_price('Adamantite ore')
adamant_bar_price = price.load_price('Adamantite bar')
profit_per_adamant_bar = adamant_bar_price - ((coal_price * 3) + adamant_ore_price)
rune_ore_price = price.load_price('Runite ore')
rune_bar_price = price.load_price('Runite bar')
profit_per_rune_bar = rune_bar_price - ((coal_price * 4) + rune_ore_price)

inventory = InventoryRegion()
screen = ScreenRegion()
bank = BankRegion()
chatbox = ChatboxRegion()

to_belt = WebWalking('walking_lists\\tobelt.pkl','map\\bf.png')
to_bank = WebWalking('walking_lists\\bank.pkl','map\\bf.png')
to_dispenser = WebWalking('walking_lists\\todispenserv2.pkl','map\\bf.png')

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
make_steel_bars = Vision('Needle\\make_steel.png')
iron_ore = Vision('Needle\\iron_ore.png')
steel_bar = Vision('Needle\\steel_bar.png')


belt_bank = array([(722,119,21,14)])
belt_close = array([(1003,564,27,25)])
dispenser_belt = array([(841,776,35,34)])
dispenser_close = array([(947,601,36,36)])
bank_dispenser = array([(1497,1072,45,25)])

start = time.time()
bars = 0

def anticheat_sleep():
    time.sleep(random.normalvariate(0.25,0.02))

def click_sleep():
    time.sleep(random.normalvariate(0.1,0.005))

def empty_bag():
    inventory.click(coal_bag,1,right_click=True)
    while(inventory.contains(coal,0.7) or inventory.contains(adamant_ore,0.7)):
        pass
    screen.click(empty_cb,.85)
    inventory.wait_for(coal)

def fill_bag():
    chest.findbank()
    inventory.click(coal_bag,1,right_click=True)
    screen.click(fill_cb,.85)
    

def coal_run():
    while(to_bank.end_of_path() == False):
        to_bank.walk()
    try:
        chest.withdraw(coal,1)
    except IndexError:
        while(to_bank.end_of_path() == False):
            to_bank.walk()
        chest.withdraw(coal,1)
    print("filling bag")
    fill_bag()
    print("checking bank pos")
    while(to_bank.end_of_path() == False):
        to_bank.walk()
    print("clicking belt...")
    screen.click_region(belt_bank)
    time.sleep(random.normalvariate(2,0.3))
    print("right clicking coal_bag")
    inventory.click(coal_bag,1,right_click=True)
    print("waiting for coal drop off")
    inv_t = time.time()
    while(inventory.contains(coal,0.7)):
        if time.time() - inv_t > 8:
            to_belt.walk()
            screen.click_region(belt_close)
            break
        else:
            pass
    try:
        print("emptying coal bag")
        screen.click(empty_cb,.90)
    except IndexError:
        print("error found: didn't empty coal bag")
        to_belt.walk()
        inventory.click(coal_bag,1,right_click=True)
        screen.click(empty_cb,0.9)
    inventory.wait_for(coal)
    click_sleep()
    screen.click_region(belt_close)
    inv_t = time.time()
    while(inventory.contains(coal,0.7)):
        if time.time() - inv_t > 5:
            break
        else:
            pass


def adamant():
    bars=0
    while True:
        while(to_bank.end_of_path() == False):
            to_bank.walk()
        try:
            chest.withdraw(adamant_ore,1)
        except IndexError:
            while(to_bank.end_of_path() == False):
                to_bank.walk()
            chest.withdraw(adamant_ore,1)
        print("filling bag")
        fill_bag()
        print("checking bank pos")
        while(to_bank.end_of_path() == False):
            to_bank.walk()
        print("clicking belt...")
        screen.click_region(belt_bank)
        time.sleep(random.normalvariate(2,0.3))
        print("right clicking coal_bag")
        inventory.click(coal_bag,1,right_click=True)
        print("waiting for coal drop off")
        inv_t = time.time()
        while(inventory.contains(coal,0.7) or inventory.contains(adamant_ore,0.7)):
            if time.time() - inv_t > 8:
                to_belt.walk()
                screen.click_region(belt_close)
                break
            else:
                pass
        try:
            print("emptying coal bag")
            screen.click(empty_cb,.90)
        except IndexError:
            print("error found: didn't empty coal bag")
            to_belt.walk()
            inventory.click(coal_bag,1,right_click=True)
            screen.click(empty_cb,0.9)
        inventory.wait_for(coal)
        click_sleep()
        screen.click_region(belt_close)
        inv_t = time.time()
        while(inventory.contains(coal,0.7) or inventory.contains(adamant_ore,0.7)):
            if time.time() - inv_t > 5:
                break
            else:
                pass
        while(to_bank.end_of_path() == False):
            to_bank.walk()
        try:
            chest.withdraw(coal,1)
        except IndexError:
            while(to_bank.end_of_path() == False):
                to_bank.walk()
            chest.withdraw(coal,1)
        inventory.wait_for(coal,0.7)
        fill_bag()
        screen.click_region(belt_bank)
        time.sleep(random.normalvariate(2,0.3))
        inventory.click(coal_bag,1,right_click=True)
        print("waiting for coal drop off")
        inv_t = time.time()
        while(inventory.contains(coal,0.7) or inventory.contains(adamant_ore,0.7)):
            if time.time() - inv_t > 8:
                to_belt.walk()
                screen.click_region(belt_close)
                break
            else:
                pass
        try:
            print("emptying coal bag")
            screen.click(empty_cb,.90)
        except IndexError:
            print("error found: didn't empty coal bag")
            to_belt.walk()
            inventory.click(coal_bag,1,right_click=True)
            screen.click(empty_cb,0.9)
        inventory.wait_for(coal)
        screen.click_region(belt_close)
        while(inventory.contains(coal,0.7) or inventory.contains(adamant_ore,0.7)):
            pass
        screen.click_region(dispenser_belt)
        try:
            chatbox.wait_for(make_adamant_bars,0.9)
        except IndexError:
            to_dispenser.walk()
            screen.click_region(dispenser_close)
            chatbox.wait_for(make_adamant_bars,0.9)
        chatbox.click(make_adamant_bars,0.9)
        while(to_bank.end_of_path() == False):
            to_bank.walk()
        bars = bars + inventory.amount(addy_bar,0.7)
        print(f'{time.strftime("%H:%M:%S. ", time.gmtime(time.time()-start))} --- {bars} bars --- {round(bars/(time.time()-start)*3600)} bars/hr --- {round((bars/(time.time()-start)*3600) * profit_per_adamant_bar) - 120000} gp/hr')
        try:
            chest.deposit(addy_bar,1)
        except IndexError:
            to_bank.walk()
            chest.deposit(addy_bar,1)


def steel():
    start_xp = int(player.xp())
    bars = 0
    
    while True:
        xp = player.xp()
        while(to_bank.end_of_path() == False):
            to_bank.walk()
        try:
            chest.withdraw(iron_ore,1)
        except IndexError:
            while(to_bank.end_of_path() == False):
                to_bank.walk()
            chest.withdraw(rune_ore,1)
        print("filling bag")
        fill_bag()
        while(to_bank.end_of_path() == False):
            to_bank.walk()
        print("clicking belt...")
        screen.click_region(belt_bank)
        time.sleep(random.normalvariate(2,0.3))
        print("right clicking coal_bag")
        inventory.click(coal_bag,1,right_click=True)
        print("waiting for coal drop off")
        inv_t = time.time()
        while(inventory.contains(coal,0.7) or inventory.contains(rune_ore,0.7)):
            if time.time() - inv_t > 8:
                to_belt.walk()
                screen.click_region(belt_close)
                break
            else:
                pass
        try:
            print("emptying coal bag")
            screen.click(empty_cb,.90)
        except IndexError:
            print("error found: didn't empty coal bag")
            to_belt.walk()
            inventory.click(coal_bag,1,right_click=True)
            screen.click(empty_cb,0.9)
        inventory.wait_for(coal)
        click_sleep()
        screen.click_region(belt_close)
        inv_t = time.time()
        while(inventory.contains(coal,0.7) or inventory.contains(rune_ore,0.7)):
            if time.time() - inv_t > 5:
                break
            else:
                pass
        to_dispenser.walk(ind_len=-2)
        while True:
            try:
                while xp == player.xp():
                    pass
                break
            except TypeError():
                pass
        time.sleep(random.normalvariate(0.25,0.002))
        try:
            screen.click_region(dispenser_close)
            try:
                chatbox.wait_for(make_steel_bars,0.9)
            except IndexError:
                to_dispenser.walk(ind_len=-2)
                screen.click_region(dispenser_close)
                chatbox.wait_for(make_steel_bars,0.9)
            chatbox.click(make_steel_bars,0.9)
            screen.click_region(bank_dispenser)
        except IndexError:
            to_dispenser.walk()
            screen.click_region(dispenser_close)
            try:
                chatbox.wait_for(make_steel_bars,0.9)
            except IndexError:
                to_dispenser.walk(ind_len=-2)
                screen.click_region(dispenser_close)
                chatbox.wait_for(make_steel_bars,0.9)
            chatbox.click(make_steel_bars,0.9)
            screen.click_region(bank_dispenser)
        try:
            screen.wait_for(Vision('Needle\\inventory_guy.png'),0.9)
        except IndexError:
            to_bank.walk()
        bars = bars + inventory.amount(steel_bar,0.7)
        try:
            xp = int(player.xp()) - start_xp
        except TypeError:
            pass
        print(f'{time.strftime("%H:%M:%S. ", time.gmtime(time.time()-start))} --- {bars} bars --- {round(bars/(time.time()-start)*3600)} bars/hr --- {round((bars/(time.time()-start)*3600) * profit_per_steel_bar) - 120000} gp/hr --- {float(xp)} xp gained --- {round((float(xp)/(time.time()-start))*3600)} xp/hr')
        try:
            chest.deposit(steel_bar,1)
        except IndexError:
            to_bank.walk()
            chest.deposit(steel_bar,1)


        
def rune():
    bars = 0
    coal_run()
    coal_run()
    while True:
        while(to_bank.end_of_path() == False):
            to_bank.walk()
        try:
            chest.withdraw(rune_ore,1)
        except IndexError:
            while(to_bank.end_of_path() == False):
                to_bank.walk()
            chest.withdraw(rune_ore,1)
        print("filling bag")
        fill_bag()
        print("checking bank pos")
        while(to_bank.end_of_path() == False):
            to_bank.walk()
        print("clicking belt...")
        screen.click_region(belt_bank)
        time.sleep(random.normalvariate(2,0.3))
        print("right clicking coal_bag")
        inventory.click(coal_bag,1,right_click=True)
        print("waiting for coal drop off")
        inv_t = time.time()
        while(inventory.contains(coal,0.7) or inventory.contains(rune_ore,0.7)):
            if time.time() - inv_t > 8:
                to_belt.walk()
                screen.click_region(belt_close)
                break
            else:
                pass
        try:
            print("emptying coal bag")
            screen.click(empty_cb,.90)
        except IndexError:
            print("error found: didn't empty coal bag")
            to_belt.walk()
            inventory.click(coal_bag,1,right_click=True)
            screen.click(empty_cb,0.9)
        inventory.wait_for(coal)
        click_sleep()
        screen.click_region(belt_close)
        inv_t = time.time()
        while(inventory.contains(coal,0.7) or inventory.contains(rune_ore,0.7)):
            if time.time() - inv_t > 5:
                break
            else:
                pass
        
        while(to_bank.end_of_path() == False):
            to_bank.walk()
        try:
            chest.withdraw(coal,1)
        except IndexError:
            while(to_bank.end_of_path() == False):
                to_bank.walk()
            chest.withdraw(coal,1)
        inventory.wait_for(coal,0.7)
        fill_bag()
        screen.click_region(belt_bank)
        time.sleep(random.normalvariate(2,0.3))
        inventory.click(coal_bag,1,right_click=True)
        print("waiting for coal drop off")
        inv_t = time.time()
        while(inventory.contains(coal,0.7)):
            if time.time() - inv_t > 8:
                to_belt.walk()
                screen.click_region(belt_close)
                break
            else:
                pass
        try:
            print("emptying coal bag")
            screen.click(empty_cb,.90)
        except IndexError:
            print("error found: didn't empty coal bag")
            to_belt.walk()
            inventory.click(coal_bag,1,right_click=True)
            screen.click(empty_cb,0.9)
        inventory.wait_for(coal)
        screen.click_region(belt_close)
        while(inventory.contains(coal,0.7)):
            pass
        screen.click_region(dispenser_belt)
        try:
            chatbox.wait_for(make_rune_bars,0.9)
        except IndexError:
            to_dispenser.walk()
            screen.click_region(dispenser_close)
            chatbox.wait_for(make_rune_bars,0.9)
        chatbox.click(make_rune_bars,0.9)
        while(to_bank.end_of_path() == False):
            to_bank.walk()
        bars = bars + inventory.amount(rune_bar,0.7)
        print(f'{time.strftime("%H:%M:%S. ", time.gmtime(time.time()-start))} --- {bars} bars --- {round(bars/(time.time()-start)*3600)} bars/hr --- {round((bars/(time.time()-start)*3600) * profit_per_rune_bar) - 120000} gp/hr')
        try:
            chest.deposit(rune_bar,1)
        except IndexError:
            to_bank.walk()
            chest.deposit(rune_bar,1)
        
        while(to_bank.end_of_path() == False):
            to_bank.walk()
        try:
            chest.withdraw(rune_ore,1)
        except IndexError:
            while(to_bank.end_of_path() == False):
                to_bank.walk()
            chest.withdraw(rune_ore,1)
        print("filling bag")
        fill_bag()
        print("checking bank pos")
        while(to_bank.end_of_path() == False):
            to_bank.walk()
        print("clicking belt...")
        screen.click_region(belt_bank)
        time.sleep(random.normalvariate(2,0.3))
        print("right clicking coal_bag")
        inventory.click(coal_bag,1,right_click=True)
        print("waiting for coal drop off")
        inv_t = time.time()
        while(inventory.contains(coal,0.7) or inventory.contains(rune_ore,0.7)):
            if time.time() - inv_t > 8:
                to_belt.walk()
                screen.click_region(belt_close)
                break
            else:
                pass
        try:
            print("emptying coal bag")
            screen.click(empty_cb,.90)
        except IndexError:
            print("error found: didn't empty coal bag")
            to_belt.walk()
            inventory.click(coal_bag,1,right_click=True)
            screen.click(empty_cb,0.9)
        inventory.wait_for(coal)
        click_sleep()
        screen.click_region(belt_close)
        inv_t = time.time()
        while(inventory.contains(coal,0.7) or inventory.contains(rune_ore,0.7)):
            if time.time() - inv_t > 5:
                break
            else:
                pass

        while(to_bank.end_of_path() == False):
            to_bank.walk()
        try:
            chest.withdraw(coal,1)
        except IndexError:
            while(to_bank.end_of_path() == False):
                to_bank.walk()
            chest.withdraw(coal,1)
        inventory.wait_for(coal,0.7)
        fill_bag()
        screen.click_region(belt_bank)
        time.sleep(random.normalvariate(2,0.3))
        inventory.click(coal_bag,1,right_click=True)
        print("waiting for coal drop off")
        inv_t = time.time()
        while(inventory.contains(coal,0.7)):
            if time.time() - inv_t > 8:
                to_belt.walk()
                screen.click_region(belt_close)
                break
            else:
                pass
        try:
            print("emptying coal bag")
            screen.click(empty_cb,.90)
        except IndexError:
            print("error found: didn't empty coal bag")
            to_belt.walk()
            inventory.click(coal_bag,1,right_click=True)
            screen.click(empty_cb,0.9)
        inventory.wait_for(coal)
        screen.click_region(belt_close)
        while(inventory.contains(coal,0.7)):
            pass
        screen.click_region(dispenser_belt)
        try:
            chatbox.wait_for(make_rune_bars,0.9)
        except IndexError:
            to_dispenser.walk()
            screen.click_region(dispenser_close)
            chatbox.wait_for(make_rune_bars,0.9)
        chatbox.click(make_rune_bars,0.9)
        while(to_bank.end_of_path() == False):
            to_bank.walk()
        bars = bars + inventory.amount(rune_bar,0.7)
        print(f'{time.strftime("%H:%M:%S. ", time.gmtime(time.time()-start))} --- {bars} bars --- {round(bars/(time.time()-start)*3600)} bars/hr --- {round((bars/(time.time()-start)*3600) * profit_per_rune_bar) - 120000} gp/hr')
        try:
            chest.deposit(rune_bar,1)
        except IndexError:
            to_bank.walk()
            chest.deposit(rune_bar,1)

        coal_run()

if __name__ == "__main__":
    steel()