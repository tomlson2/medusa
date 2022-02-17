from windowcapture import InventoryRegion, PlayerRegion, ScreenRegion, BankRegion
from webwalking import WebWalking
from vision import Vision
from numpy import array
import time, random

to_fire1 = WebWalking("walking_lists\\light_logs1.pkl",'map\\falador.png')
to_fire2 = WebWalking("walking_lists\\light_logs2.pkl",'map\\falador.png')
to_bank = WebWalking("walking_lists\\falador_east_bank.pkl",'map\\falador.png')

bank_region = array([(690,632,331,98)])

inventory = InventoryRegion()
screen = ScreenRegion()
player = PlayerRegion()
bank = BankRegion()

tinderbox = Vision('Needle\\firemaking\\tinderbox.png')
normal = Vision('Needle\\firemaking\\logs.png')
willow = Vision("Needle\\firemaking\\willow_logs.png")


def firemake(logs):
    if inventory.contains(logs) and inventory.contains(tinderbox):
        return True
    else:
        return False


def run(logs):
    path1 = True
    while True:
        stuck = 0
        if firemake(logs=logs) == True:
            if path1 == True:
                print("Going to north row")
                to_fire1.walk(within=2)
            else:
                print("Going to south row")
                to_fire2.walk(within=2)
            while inventory.contains(logs):
                inventory.click(tinderbox)
                time.sleep(random.normalvariate(0.3, 0.02))
                inventory.click(logs)
                s = time.time()
                time.sleep(random.normalvariate(0.3, 0.02))
                while to_fire1.coords_change() == False:
                    if time.time() - s > 5:
                        stuck += 1
                        break
                    else:
                        time.sleep(0.1)
                print("Moved")
                if stuck > 3:
                    print("stuck! switching lines")
                    # negate bool to switch path
                    path1 = not path1
                    break
                path1 = not path1
                
        else:
            to_bank.walk(within=2)
            print("Banking")
            screen.click_region(bank_region)
            time.sleep(random.normalvariate(1.8,0.1))
            bank.click(logs)
            time.sleep(random.normalvariate(1, 0.1))

if __name__ == "__main__":
    run(willow)