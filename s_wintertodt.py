from webwalking import WebWalking
from windowcapture import ScreenRegion, BankRegion, InventoryRegion
from vision import Vision

path = 'Needle\\wintertodt\\'

screen = ScreenRegion()
bank_region = BankRegion()
inventory = InventoryRegion()

to_door = WebWalking()
to_brazier = WebWalking()

logs = Vision(path + 'logs.png')