from windowcapture import InventoryRegion, PlayerRegion, ScreenRegion, BankRegion
from webwalking import WebWalking
from vision import Vision
import time, random

to_fire1 = WebWalking("walking_lists\\light_logs1.pkl",'map\\falador.png')
to_fire2 = WebWalking("walking_lists\\light_logs2.pkl",'map\\falador.png')
to_bank = WebWalking("walking_lists\\falador_east_bank.pkl",'map\\falador.png')

inventory = InventoryRegion()
player = PlayerRegion()

tinderbox = Vision('Needle\\firemaking\\tinderbox.png')
logs = Vision('Needle\\firemaking\\logs.png')

while inventory.contains(logs):
    inventory.click(tinderbox)
    time.sleep(random.normalvariate(0.3, 0.02))
    inventory.click(logs)
    while player.is_animating(history=25, threshold=15, loops=15):
        time.sleep(0.1)