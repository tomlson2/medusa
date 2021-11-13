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
        self.numbers.number(im)

    def run(self):
        im = self.vision.apply_hsv_filter(self.run_orb.get_screenshot(),self.filter)
        self.numbers.number(im)

    def prayer(self):
        im = self.vision.apply_hsv_filter(self.prayer_orb.get_screenshot(),self.filter)
        self.numbers.number(im)

player = Player()

player.health()
