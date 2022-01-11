from win32con import STATUS_ABANDONED_WAIT_0
from vision import Vision
from interactions import Interactions
from windowcapture import WindowCapture
from player import Player
import time
import random

class Bank:

    # constant

    # properties
    item = None
    quantity = 0

    def __init__(self, bank_needle : str, stam : bool = False):

        self.screen = Interactions()
        self.inventory = Interactions(area='inventory')
        self.bank = Interactions(area='bank')
        self.chatbox = Interactions(area='chatbox')
        self.sidebar_r = Interactions(area='sidebar_r')
        self.wincap = WindowCapture('BlueStacks')

        self.stam = stam

        self.stamina_pot = Vision('Needle\\stam.png')
        self.bank_needle = Vision(bank_needle)
        self.bank_check = Vision('Needle\\inventory_guy.png')
        self.x = Vision('Needle\\x_bank.png')
    
    def status(self):

        bank_interface = self.screen.contains(self.bank_check,0.9)
        return bank_interface

    def withdraw(self, item, threshold=0.6, quantity=0):

        if self.status() == False:
            self.findbank()
        
        if self.stam == True and Player().need_stam() == True:
            self.bank.click(self.stamina_pot,right_click=True)
            time.sleep(random.normalvariate(0.4,0.05))
            self.bank.click(Vision('Needle\\withdraw-1.png'),1)
            time.sleep(random.normalvariate(0.4,0.05))
            self.close()
            time.sleep(random.normalvariate(0.4,0.05))
            self.inventory.click(self.stamina_pot)
            self.findbank()
            self.inventory.click(self.stamina_pot, 1)
            time.sleep(random.normalvariate(0.4,0.05))
            
        print('Withdrawing...')
        self.bank.click(item, threshold)


    def deposit(self, item, threshold=0.6, quantity=0):
        if self.status() == False:
            self.findbank()
        print('Depositing...')
        self.inventory.click(item, threshold)

    
    def close(self):
        print('Closing Bank...')
        self.screen.wait_for(self.x,0.76)
        self.screen.click(self.x,0.76)

    def findbank(self):
        print('Finding Bank...')
        while True:
            if self.status() == True:
                break
            try:
                self.screen.click(self.bank_needle,1)
                self.screen.wait_for(self.bank_check)
                break
            except IndexError:
                print('didnt find bank')

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