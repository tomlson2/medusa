from turtle import Screen
from windowcapture import ScreenRegion, InventoryRegion, ChatboxRegion
from vision import Vision
from scripting import Script
from webwalking import WebWalking
import time

'''
Start in lumbridge castle with axe equipped and empty inventory
Max zoom
2 brightness 
'''

walk = WebWalking('walking_lists\\regular_trees.pkl','map\\lumbridge.png')
s_leaves = Vision('Needle\\regular_trees\\south_leaves.png')
n_leaves = Vision('Needle\\regular_trees\\north_leaves.png')
logs = Vision('Needle\\regular_trees\\logs.png')
screen = ScreenRegion()
inventory = InventoryRegion()
chatbox = ChatboxRegion()

class RegularTrees(Script):
    
    def __init__(self, breaking=True, show_log=False) -> None:
        super().__init__(breaking, show_log)

    def walk_to_start(self):
        walk.walk(within=4)
    
    def cut_tree(self, needle):
        if screen.contains(needle):
                screen.click(needle)
                time.sleep(1)
                while screen.contains(needle):
                    time.sleep(0.25)
                if inventory.is_full():
                    inventory.drop_click_vert(logs, 24)

    def main(self):
        self.walk_to_start()
        while True:
            if chatbox.contains_dialogue():
                chatbox.tap_handler()
            self.cut_tree(s_leaves)
            self.cut_tree(n_leaves)
            self.print_time()
            


script = RegularTrees()
script.main()