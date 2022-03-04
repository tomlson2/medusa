from webwalking import WebWalking
from regions import ShopRegion, ScreenRegion, ChatboxRegion
from model import Model
from vision import Vision
import time

screen = ScreenRegion()
cb = ChatboxRegion()
shop = ShopRegion()

npc_model1 = Model(weight_path='model_data\\weights\\tourist1.pt')

walk1 = WebWalking('walking_lists\\123.pkl', 'map\\desert1.png')

shantay_pass = Vision("Needle\\tourist_trap\\shantay_pass.png")

def shanty():
    npc_model1.label_idx = 0
    screen.click(npc_model1, threshold = 0.45)
    for _ in range(5):
        if cb.contains_dialogue():
            break
        else:
            time.sleep(1)
    cb.option_handler([2])
    cb.tap_handler()
    time.sleep(1)

def buy_items():
    shop.purchase(6, 1)
    shop.purchase(7, 1)
    shop.purchase(8, 1)
    shop.purchase(18, 1)
    shop.purchase(0, 5)
    shop.purchase(9, 5)
    shop.purchase(10, 50)

walk1.walk_once()
screen.click(shantay_pass, 1)

