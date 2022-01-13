from hsvfilter import HsvFilter
from windowcapture import WindowCapture
from interactions import Interactions
from vision import Vision
from ocr import Ocr


class Player:

    def __init__(self) -> None:
        self.run_boot = Interactions(area='run_boot')
        self.run_orb = WindowCapture(area='run_orb')
        self.health_orb = WindowCapture(area='health_orb')
        self.prayer_orb = WindowCapture(area='prayer_orb')
        self.special_orb = WindowCapture(area='special_orb')
        self.xp_bar = WindowCapture(area='xp_bar')
        self.vision = Vision('Needle\\banana.png')
        self.stam_boot = Vision('Needle\\stam_boot.png')
        self.coffer = WindowCapture(area='smithing')
        self.filter = HsvFilter(vMin=136,sSub=255)

        self.orbs = Ocr('samples/generalsamples.data', 'responses/generalresponses.data')
        self.xpb = Ocr('samples/xpsamps.data', 'responses/xpresponses.data')
        self.choose_option = Ocr('samples/bold12lowersamples.data', 'responses/bold12lowerresponses.data')

    def health(self):
        im = self.vision.apply_hsv_filter(self.health_orb.get_screenshot(),self.filter)
        health = self.orbs.number(im)
        return health

    def run(self):
        im = self.vision.apply_hsv_filter(self.run_orb.get_screenshot(),self.filter)
        run = self.orbs.number(im)
        return run

    def prayer(self):
        im = self.vision.apply_hsv_filter(self.prayer_orb.get_screenshot(),self.filter)
        prayer = self.orbs.number(im)
        return prayer
    
    def stats(self):
        im = self.vision.apply_hsv_filter(self.health_orb.get_screenshot(),self.filter)
        health = self.numbers.number(im)
        im = self.vision.apply_hsv_filter(self.run_orb.get_screenshot(),self.filter)
        run = self.numbers.number(im)
        im = self.vision.apply_hsv_filter(self.prayer_orb.get_screenshot(),self.filter)
        prayer = self.numbers.number(im)

        text = "health: " + str(health) + " run: " + str(run) + " prayer: " + str(prayer) + "."
        return text

    def xp(self):
        im = self.vision.apply_hsv_filter(self.xp_bar.get_screenshot(),self.filter)
        xp = self.xpb.number(im)
        return xp
    
    # def bank_number(self):
    #     im = self.vision.apply_hsv_filter(self.bank_num.get_screenshot(),self.filter)
    #     number = self.numbers.number(im)
    #     return number
    
    def need_stam(self):
        if self.run() > 70 or self.run_boot.contains(self.stam_boot,0.9) == True:
            return False
        else:
            print("NEED STAM")
            return True


