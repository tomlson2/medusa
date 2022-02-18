from windowcapture import InventoryRegion, PlayerRegion, ScreenRegion, BankRegion
from webwalking import WebWalking
from vision import Vision
from numpy import array
import time, random

to_fire1 = WebWalking("walking_lists\\light_logs1.pkl",'map\\falador.png')
to_fire2 = WebWalking("walking_lists\\light_logs2.pkl",'map\\falador.png')
to_bank = WebWalking("walking_lists\\falador_east_bank.pkl",'map\\falador.png')

bank_region = array([(790,632,250,98)])

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
    start_time = time.time()
    burned = 0
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
            start_logs = inventory.amount(logs)
            while inventory.contains(logs):
                inventory.click(tinderbox)
                time.sleep(random.normalvariate(0.3, 0.02))
                inventory.click(logs)
                s = time.time()
                time.sleep(random.normalvariate(0.3, 0.02))
                while to_fire1.coords_change() == False:
                    if time.time() - s > 15:
                        stuck += 1
                        break
                    else:
                        time.sleep(0.1)
                print("Moved")
                if stuck > 2:
                    print("stuck! switching lines")
                    break
            path1 = not path1
            burned += start_logs
                
        else:
            to_bank.walk(within=2)
            print("Banking")
            screen.click_region(bank_region)
            try:
                bank.wait_for(logs)
                bank.click(logs)
            except IndexError:
                screen.click_region(bank_region)
                bank.wait_for(logs)
                bank.click(logs)
            time.sleep(random.normalvariate(1, 0.1))

        runtime = (time.time() - start_time)
        runtime_formatted = time.strftime("%H:%M:%S", time.gmtime(runtime))
        print(f"run time: {runtime_formatted} - logs burned: {burned} ({int(burned/runtime * 3600)}/hr)")

if __name__ == "__main__":
    run(willow)