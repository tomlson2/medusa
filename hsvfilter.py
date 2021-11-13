
# custom data structure to hold the state of an HSV filter
class HsvFilter:

    def __init__(self, hMin=0, sMin=0, vMin=0, hMax=179, sMax=255, vMax=255, 
                    sAdd=0, sSub=0, vAdd=0, vSub=0):
        self.hMin = hMin
        self.sMin = sMin
        self.vMin = vMin
        self.hMax = hMax
        self.sMax = sMax
        self.vMax = vMax
        self.sAdd = sAdd
        self.sSub = sSub
        self.vAdd = vAdd
        self.vSub = vSub
