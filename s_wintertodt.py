from webwalking import WebWalking
from windowcapture import ScreenRegion, BankRegion, InventoryRegion
from vision import Vision

path = 'Needle\\wintertodt\\'

screen = ScreenRegion()
bank_region = BankRegion()
inventory = InventoryRegion()

to_door = WebWalking('walking_lists\\wintertodt_door.pkl', 'maps\\wintertodt.png')
to_brazier = WebWalking('walking_lists\\wintertodt_brazier.pkl', 'maps\\wintertodt.png')

logs = Vision(path + 'logs.png')

to_brazier.walk()