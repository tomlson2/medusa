from turtle import Screen
from windowcapture import BankRegion, CustomRegion, PlayerRegion, ScreenRegion, ChatboxRegion, InventoryRegion
from vision import Vision
from model import Model
import time, random
from webwalking import WebWalking


'''
start in your house in build mode with 3 full watering cans, noted bagged plants, and unnoted (optional)
north full up
zoom 2 brightness 2
inventory open
'''

path = 'Needle\\bagged_planter\\'

full_watering_can = Vision(path + "full_wateringcan" + ".png")
empty_watering_can = Vision(path + "empty_wateringcan" + ".png")
bagged_plant = Vision(path + "bagged_plant" + ".png")
exchange_all = Vision(path + "exchange_all" + ".png")
noted_bagged_plants = Vision(path + "noted_bagged_plants" + ".png")
sink = Vision(path + "sink" + ".png")
build_mode_opt = Vision(path + "build_mode" + ".png")
unbuilt_plant = Vision(path + "unbuilt_plant.png")
build_plant_opt = Vision(path + "build_plant" + ".png")
fern_menu = Vision(path + "fern_menu.png")
remove_fern_opt = Vision(path + "remove_fern.png")
yes = Vision(path + "yes.png")
outside_portal = Vision(path + "outside_portal.png")
inside_portal = Vision(path + "inside_portal.png")
tap_here = Vision(path + "tap_here.png")

to_sink = WebWalking('walking_lists\\to_sink.pkl','map\\rimmington.png')
to_phials = WebWalking('walking_lists\\to_phials.pkl','map\\rimmington.png')
to_portal = WebWalking('walking_lists\\to_portal.pkl','map\\rimmington.png')

phials = Model('model_data\\weights\\phials.pt')

to_plant = ([(763,849,43,35)])
remove_fern_region = ([(887,666,32,33)])

inventory = InventoryRegion()
screen = ScreenRegion()
chatbox = ChatboxRegion()

while True:
    while inventory.contains(bagged_plant,0.8):
        screen.click(unbuilt_plant, right_click=True)
        screen.click(build_plant_opt, 1)
        screen.click(fern_menu)
        time.sleep(random.normalvariate(1.5, 0.1))
        screen.click_region(remove_fern_region, right_click=True)
        screen.click(remove_fern_opt)
        time.sleep(random.normalvariate(1.3, 0.03))
        while chatbox.contains(tap_here):
            chatbox.click(tap_here)
            time.sleep(random.normalvariate(0.8, 0.03))
        chatbox.click(yes)
        time.sleep(random.normalvariate(0.7, 0.03))
    screen.click(inside_portal)
    time.sleep(random.normalvariate(3.5, 0.3))
    to_sink.walk(within=2,ind_len=-2)
    time.sleep(random.normalvariate(0.7, 0.03))
    inventory.click(empty_watering_can,1)
    screen.click(sink,1)
    time.sleep(random.normalvariate(8, 0.4))
    to_phials.walk_once(150)
    time.sleep(random.normalvariate(6, 0.1))
    inventory.click(noted_bagged_plants,1)
    screen.click(phials,0.5)
    chatbox.wait_for(exchange_all, 0.8)
    chatbox.click(exchange_all, 1)
    to_portal.walk_once(130)
    time.sleep(random.normalvariate(4.2, 0.15))
    screen.click(outside_portal, right_click=True)
    screen.click(build_mode_opt)
    time.sleep(random.normalvariate(5.5, 0.2))
    screen.click_region(to_plant)
    time.sleep(random.normalvariate(1.2, 0.1))


