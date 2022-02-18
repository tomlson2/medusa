from webwalking import WebWalking
from windowcapture import ChatboxRegion, CustomRegion, HealthOrb, ScreenRegion, BankRegion, InventoryRegion
from player import Player
from vision import Vision
from numpy import array
import time, random

path = 'Needle\\wintertodt\\'

screen = ScreenRegion()
bank_region = BankRegion()
inventory = InventoryRegion()
brazier_status = CustomRegion(69, 68, 136, 311)

close_root_region = array([(918,628,43,44)])
root_region = array([(890,1003,40,50)])
exit_door_region = array([(835,532,261,135)])
enter_door_region = array([(766,198,379,178)])
brazier_region = array([(927,406,73,51)])

player = Player()

health = HealthOrb()

to_door = WebWalking('walking_lists\\wintertodt_door.pkl', 'map\\wintertodt.png')
to_brazier = WebWalking('walking_lists\\wintertodt_brazier.pkl', 'map\\wintertodt.png')

next_round = Vision(path + 'returning.png')
kindling = Vision(path + 'kindling.png')
logs = Vision(path + 'logs.png')
knife = Vision(path + 'knife.png')
bank_chest = Vision(path + 'bank_chest.png')
unlit_brazier = Vision(path + 'unlit_brazier.png')
cake1 = Vision(path + 'cake1.png')
cake2 = Vision(path + 'cake2.png')
cake3 = Vision(path + 'cake3.png')


def eat_cake():
    if inventory.contains(cake3):
        inventory.click(cake3)
    elif inventory.contains(cake2):
        inventory.click(cake2)
    elif inventory.contains(cake1):
        inventory.click(cake1)
    else:
        print("No Food!")


def start_fletching():
    inventory.click(knife,1)
    time.sleep(random.normalvariate(0.2, 0.01))
    inventory.click(logs)

def fletch():
    if inventory.contains(logs):
        start_fletching()
        while inventory.contains(logs):
            if health.damage_taken() == True:
                if health.health() < 5:
                    eat_cake()
                start_fletching()

def woodcut():
    if to_brazier.end_of_path(within=2) == True:
        screen.click_region(root_region)
        time.sleep(random.normalvariate(4,0.2))
        while inventory.amount(logs) < 20:
            if health.health() < 5:
                eat_cake()
    else:
        print("No logs to fletch")

def unlit() -> bool:
    if brazier_status.contains(unlit_brazier,0.75):
        return True
    else:
        return False

def feed_brazier():
    to_brazier.walk(ind_len=-2)
    screen.click_region(brazier_region)
    while inventory.contains(kindling):
        if health.damage_taken() == True:
            if health.health() < 5:
                eat_cake()
            screen.click_region(brazier_region)
        if inventory.is_emptying() == False:
            screen.click_region(brazier_region)

def walk_to_start():
    to_door.walk()
    screen.click_region(enter_door_region)
    time.sleep(random.uniform(4, 0.2))
    to_brazier.walk(within=2)

def run():
    while True:
        walk_to_start()
        while ChatboxRegion().contains(next_round):
            time.sleep(0.1)
        screen.click_region(brazier_region)
        time.sleep(random.normalvariate(1.8,0.15))
        woodcut()
        fletch()
        feed_brazier()

run()