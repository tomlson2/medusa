from webwalking import WebWalking
from vision import Vision
from player import Player
from interactions import Interactions

inventory = Interactions(area='inventory')
screen = Interactions()
bank = Interactions(area='bank')

player = Player()

coal_bag = Vision('Needle\\coal_bag.png')
coal = Vision('Needle\\coal.png')
adamant_ore = Vision('Needle\\adamant_ore.png')

# TODO: Right clicking, improved web walking speed, bank ocr, stamina check, anticheat, edge detection

