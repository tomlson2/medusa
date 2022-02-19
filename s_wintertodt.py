from tracemalloc import start
from webwalking import WebWalking
from windowcapture import ChatboxRegion, CustomRegion, HealthOrb, ScreenRegion, BankRegion, InventoryRegion
from player import Player
from vision import Vision
import threading
from numpy import array
import time, random
from scripting import Script

path = 'Needle\\wintertodt\\'


screen = ScreenRegion()
bank = BankRegion()
inventory = InventoryRegion()
brazier_status = CustomRegion(69, 68, 136, 311)

close_root_region = array([(918,628,43,44)])
root_region = array([(890,1003,40,50)])
exit_door_region = array([(835,532,261,135)])
enter_door_region = array([(766,198,379,178)])
brazier_region = array([(927,406,73,51)])

player = Player()

health = HealthOrb()

to_outside_door = WebWalking('walking_lists\\wintertodt_door.pkl', 'map\\wintertodt.png')
to_bank = WebWalking('walking_lists\\wintertodt_door.pkl', 'map\\wintertodt.png', reverse=True)
to_brazier = WebWalking('walking_lists\\wintertodt_brazier.pkl', 'map\\wintertodt.png')
to_inside_door = WebWalking('walking_lists\\wintertodt_brazier.pkl', 'map\\wintertodt.png', reverse=True)

next_round = Vision(path + 'returning.png')
kindling = Vision(path + 'kindling.png')
logs = Vision(path + 'logs.png')
knife = Vision(path + 'knife.png')
bank_chest = Vision(path + 'bank_chest.png')
unlit_brazier = Vision(path + 'unlit_brazier.png')
cake1 = Vision(path + 'cake1.png')
cake2 = Vision(path + 'cake2.png')
cake3 = Vision(path + 'cake3.png')
supply_crate = Vision(path + 'supply_crate.png')



class Wintertodt(Script):

    def __init__(self, breaking = True) -> None:
        super().__init__()
        self.breaking = breaking

    def eat_cake(self):
        if inventory.contains(cake3):
            inventory.click(cake3)
        elif inventory.contains(cake2):
            inventory.click(cake2)
        elif inventory.contains(cake1):
            inventory.click(cake1)
        else:
            print("No Food!")
        time.sleep(random.normalvariate(0.3,0.05))

    def start_fletching(self):
        inventory.click(knife,1)
        time.sleep(random.normalvariate(0.2, 0.01))
        inventory.click(logs)

    def damage_interruption(self):
        if health.damage_taken() == True:
            if health.get_hp() < 5:
                self.eat_cake()
            return True

    def level_interruption(self):
        if ChatboxRegion().contains_dialogue():
            return True

    def not_emptying(self):
        if inventory.is_emptying() == False:
            return True

    def fletch(self):
        if inventory.contains(logs):
            self.start_fletching()
            while inventory.contains(logs):
                if self.damage_interruption() == True:
                    self.start_fletching()
                elif self.level_interruption() == True:
                    self.start_fletching()

    def woodcut(self):
        if to_brazier.end_of_path(within=2) == False:
            to_brazier.walk(ind_len=-2)
        screen.click_region(root_region)
        time.sleep(random.normalvariate(4,0.2))
        while inventory.amount(logs) < 20:
            if self.level_interruption():
                screen.click_region(close_root_region)
            if health.get_hp() < 7:
                self.eat_cake()
                screen.click_region(close_root_region)

    def unlit(self) -> bool:
        if brazier_status.contains(unlit_brazier,0.75):
            return True

    def feed_brazier(self):
        to_brazier.walk(ind_len=-2)
        screen.click_region(brazier_region)
        while inventory.contains(kindling):
            if health.get_hp() < 7:
                self.eat_cake()
                screen.click_region(brazier_region)
            if self.unlit():
                screen.click_region(brazier_region)
                time.sleep(random.normalvariate(0.7,0.1))
                screen.click_region(brazier_region)
            elif self.damage_interruption():
                screen.click_region(brazier_region)
            elif self.level_interruption():
                screen.click_region(brazier_region)
            elif self.not_emptying():
                screen.click_region(brazier_region)
    

    def walk_to_start(self):
        to_outside_door.walk(within=4)
        screen.click_region(enter_door_region)
        time.sleep(random.normalvariate(4, 0.2))
        to_brazier.walk(within=2)

    def minigame(self):
        self.woodcut()
        self.fletch()
        self.feed_brazier()

    def main(self):
        while True:
            self.walk_to_start()
            while ChatboxRegion().contains(next_round):
                time.sleep(0.05)
            screen.click_region(brazier_region)
            time.sleep(random.normalvariate(1.8,0.15))
            self.minigame()
            to_inside_door.walk()
            while ChatboxRegion().contains(next_round) == False:
                time.sleep(1)
            screen.click_region(exit_door_region)
            time.sleep(random.normalvariate(4,0.2))
            to_bank.walk(ind_len=-2,within=2)
            deadloop = 0
            while bank.wait_interface() == False:
                screen.click(bank_chest)
                deadloop += 1
                if deadloop > 3:
                    break
            if bank.status() == False:
                break
            else:
                bank.deposit(supply_crate)
            if InventoryRegion().amount(cake1) < 3:
                bank.withdraw(cake1, quantity=2)
            print(f'runtime: {self.get_runtime()}')

if __name__ == '__main__':
   Wintertodt().main()