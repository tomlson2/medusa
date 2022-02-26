from hsvfilter import HsvFilter
from windowcapture import Interactions
from regions import XpRegion, HealthOrb, RunOrb
from vision import Vision
from ocr import Ocr


class Player(Interactions):

    def __init__(self) -> None:
        super().__init__()
        self.vision = Vision('Needle\\banana.png')
        self.filter = HsvFilter(vMin=136,sSub=255)

        self.orbs = Ocr('samples/generalsamples.data', 'responses/generalresponses.data')

    def health(self):
        health = HealthOrb().get_hp()
        return health

    def run_energy(self):
        energy = RunOrb().get_energy()
        return energy

    def prayer(self):
        im = self.apply_hsv_filter(self.get_screenshot(),self.filter)
        prayer = self.orbs.number(im)
        return prayer
    
    # def stats(self):
    #     im = self.apply_hsv_filter(self.get_screenshot(),self.filter)
    #     health = self.numbers.number(im)
    #     im = self.apply_hsv_filter(self.get_screenshot(),self.filter)
    #     run = self.numbers.number(im)
    #     im = self.apply_hsv_filter(self.get_screenshot(),self.filter)
    #     prayer = self.numbers.number(im)

    #     text = "health: " + str(health) + " run: " + str(run) + " prayer: " + str(prayer) + "."
    #     return text

    def xp(self):
        xp = XpRegion().get_xp()
        return xp
        
    
    # def bank_number(self):
    #     im = self.vision.apply_hsv_filter(self.bank_num.get_screenshot(),self.filter)
    #     number = self.numbers.number(im)
    #     return number
    
    def need_stam(self):
        if self.run() > 65:
            pass
        else:
            print("NEED STAM")
            return True


