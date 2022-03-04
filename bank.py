from win32con import STATUS_ABANDONED_WAIT_0
from vision import Vision
from regions import BankRegion, ChatboxRegion, InventoryRegion, ScreenRegion
from player import Player
import time
import random

class Bank:

    # constant

    # properties
    item = None
    quantity = 0

    def __init__(self, bank_needle : str, stam : bool = False):

        self.screen = ScreenRegion()
        self.inventory = InventoryRegion()
        self.bank = BankRegion()
        self.chatbox = ChatboxRegion()

        self.stam = stam

        self.stamina_pot = Vision('Needle\\stam.png')
        self.bank_needle = Vision(bank_needle)
        self.bank_check = Vision('Needle\\inventory_guy.png')
        self.x = Vision('Needle\\x_bank.png')
        self.withdraw1 = Vision('Needle\\withdraw1.png')
        self.withdraw_all = Vision('Needle\\withdraw_all.png')
    
    def status(self):

        bank_interface = self.screen.contains(self.bank_check,0.9)
        return bank_interface

    def withdraw(self, item, threshold=0.6, quantity=0):

        if self.status() == False:
            self.findbank()
        
        if self.stam == True and Player().need_stam() == True:
            self.bank.click(self.withdraw1, 0.9)
            time.sleep(random.normalvariate(0.15,0.01))
            self.bank.click(self.stamina_pot, 1)
            time.sleep(random.normalvariate(0.15,0.01))
            self.close()
            time.sleep(random.normalvariate(0.15,0.01))
            self.inventory.click(self.stamina_pot, 1)
            self.findbank()
            time.sleep(random.normalvariate(0.15,0.01))
            self.inventory.click(self.stamina_pot, 1)
            self.screen.click(self.withdraw_all, 0.9)
            time.sleep(random.normalvariate(0.15,0.01))
            
        self.bank.click(item, threshold)


    def deposit(self, item, threshold=0.6, quantity=0):
        if self.status() == False:
            self.findbank()
        self.inventory.click(item, threshold)

    
    def close(self):
        self.screen.wait_for(self.x,0.76)
        self.screen.click(self.x,0.76)

    def findbank(self):
        print("BANKING")
        while True:
            if self.status() == True:
                break
            try:
                self.screen.click(self.bank_needle,1)
                self.screen.wait_for(self.bank_check,0.8) #TODO CHANGE TO BANK REGION?
                break
            except IndexError:
                print("DIDN'T FIND BANK")
        # screenshot = self.wincap.get_screenshot()
        # while vision.match(screenshot,threshold=0.8)[0] == False:
        #      screenshot = self.wincap.get_screenshot()
        
        # points = vision.get_click_points(vision.match(self.wincap.get_screenshot(),threshold=0.8)[1])
        # try:
        #     target = self.wincap.get_screen_position(points[0])
        #     pyautogui.click(x=target[0], y=target[1])
        #     time.sleep(random.uniform(1,1.96))
        # except IndexError:
        #     print('didnt find target!')
    
    # changed item_search to use the bank area instead of wincap
    # this was causing problems causing an inventory click instead of bank click for 
    # similar looking items
    # def item_search(self, item):

    #     # TODO apply left skewed distribution x and y values. 
    #     # x1 = random.uniform(334, 480)
    #     # y1 = random.uniform(300, 320)
    #     # x2 = x1 + random.uniform(-10,10)
    #     # y2 = random.uniform(260, 280)

    #     # pyautogui.mouseDown(x1,y1)
    #     # mouse_movement.bezier_move(x1,y1,x2,y2)
    #     # pyautogui.mouseUp()

    #     # screenshot wincap now is bank
    #     screenshot = self.bank.get_screenshot()
    #     if item.match(screenshot, threshold = 0.85)[0] == False:

    #         x1 = random.uniform(334,480)
    #         y1 = random.uniform(260,340)
    #         pyautogui.moveTo(x1, y1)

    #         while item.match(screenshot, threshold = 0.85)[0] == False:
    #             for s in range(1):
    #                 pyautogui.scroll(-1)
    #                 time.sleep(random.uniform(0.02,0.035))
    #             time.sleep(random.uniform(0.055,0.065))
    #             screenshot = self.wincap.get_screenshot()
    #         time.sleep(random.uniform(0.6,1.1))

    #     return item.match(self.wincap.get_screenshot(), threshold=0.85)[1]