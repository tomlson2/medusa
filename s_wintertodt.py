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

    def __init__(self) -> None:
        super().__init__(show_log=True)

    def eat_cake(self):
        self.log("Eating cake")
        if inventory.contains(cake3):
            inventory.click(cake3)
        elif inventory.contains(cake2):
            inventory.click(cake2)
        elif inventory.contains(cake1):
            inventory.click(cake1)
        else:
            self.log("No Food!")
        time.sleep(random.normalvariate(0.3,0.05))

    def start_fletching(self):
        self.log("Fletching")
        inventory.click(knife,1)
        time.sleep(random.normalvariate(0.2, 0.01))
        inventory.click(logs)

    def damage_interruption(self):
        if health.damage_taken() is True:
            self.log("Damage Taken")
            if health.get_hp() < 5:
                self.eat_cake()
            return True
    
    def not_increasing(self):
        if inventory.item_increasing(kindling) is False:
            return True
        else:
            return False

    def level_interruption(self):
        if ChatboxRegion().contains_dialogue():
            self.log("Level interruption")
            return True

    def not_emptying(self):
        if inventory.is_emptying() is False:
            self.log("Inventory not emptying")
            return True

    def fletch(self):
        if inventory.contains(logs):
            self.start_fletching()
            while inventory.contains(logs):
                if any([self.damage_interruption(), self.level_interruption(), self.not_increasing()]):
                    self.start_fletching()
                    time.sleep(0.5)

    def woodcut(self):
        if to_brazier.end_of_path(within=2) is False:
            to_brazier.walk(ind_len=-2)
        self.log("Clicking root region")
        screen.click_region(root_region)
        time.sleep(random.normalvariate(4,0.2))
        while inventory.amount(logs) < 20:
            if self.level_interruption():
                self.log("Clicking close root region")
                screen.click_region(close_root_region)
                time.sleep(random.normalvariate(0.3,0.05))
            if health.get_hp() < 7:
                self.eat_cake()
                screen.click_region(close_root_region)
                time.sleep(random.normalvariate(0.3,0.05))

    def unlit(self) -> bool:
        if brazier_status.contains(unlit_brazier,0.75):
            self.log("Brazier not lit")
            return True

    def feed_brazier(self):
        to_brazier.walk(ind_len=-2)
        self.log("Clicking brazier")
        screen.click_region(brazier_region)
        while inventory.contains(kindling):
            if health.get_hp() < 7:
                self.eat_cake()
                screen.click_region(brazier_region)
            if self.unlit():
                screen.click_region(brazier_region)
                time.sleep(random.normalvariate(2.4,0.1))
                screen.click_region(brazier_region)
            elif any([self.damage_interruption(), self.level_interruption(), self.not_emptying()]):
                screen.click_region(brazier_region)
                time.sleep(0.5)
    

    def walk_to_start(self):
        self.log("Walking to start")
        to_outside_door.walk(within=7)
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
            self.log("Waiting for minigame to begin.")
            while ChatboxRegion().contains(next_round):
                time.sleep(0.05)
            screen.click_region(brazier_region)
            time.sleep(random.normalvariate(1.8,0.15))
            self.minigame()
            to_inside_door.walk()
            while ChatboxRegion().contains(next_round) is False:
                time.sleep(1)
            time.sleep(1.5)
            screen.click_region(exit_door_region)
            time.sleep(random.normalvariate(4,0.2))
            to_bank.walk(ind_len=-2,within=2)
            screen.click(bank_chest)
            screen.wait_for(bank.bank_check, t=3)
            for _ in range(5):
                if screen.contains(bank.bank_check):
                    break
                else:
                    screen.click(bank_chest)
                    screen.wait_for(bank.bank_check)
            try:
                bank.deposit(supply_crate)
            except IndexError:
                self.log("Didn't have supply crate.")
            if InventoryRegion().amount(cake1, 0.8) < 3:
                bank.withdraw(cake1, quantity=3)
            self.print_time()

if __name__ == '__main__':
    script = Wintertodt()
    script.main()
