from hsvfilter import HsvFilter
from windowcapture import WindowCapture
from vision import Vision
from ocr import Numbers


class Player:

    def __init__(self) -> None:
        self.run_orb = WindowCapture(area='run_orb')
        self.health_orb = WindowCapture(area='health_orb')
        self.prayer_orb = WindowCapture(area='prayer_orb')
        self.special_orb = WindowCapture(area='special_orb')
        self.vision = Vision('Needle\\banana.png')
        self.numbers = Numbers()
        self.filter = HsvFilter(vMin=136,sSub=255)

    def health(self):
        im = self.vision.apply_hsv_filter(self.health_orb.get_screenshot(),self.filter)
        health = self.numbers.number(im)
        return health

    def run(self):
        im = self.vision.apply_hsv_filter(self.run_orb.get_screenshot(),self.filter)
        run = self.numbers.number(im)
        return run

    def prayer(self):
        im = self.vision.apply_hsv_filter(self.prayer_orb.get_screenshot(),self.filter)
        prayer = self.numbers.number(im)
        return prayer
