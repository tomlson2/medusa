import cv2 as cv
import time
from windowcapture import WindowCapture
from vision import Vision
import win32gui, win32api, win32con
import random
import numpy as np
import win32gui, win32con
import pickle


class WebWalking():
    """
    WebWalking object, pass path to pickle list and map png
    """
    def __init__(self, path: str, worldmap: str):
        
        try:
            with open(path, 'rb') as pickle_load:
                self.path = pickle.load(pickle_load)
        except FileNotFoundError:
            self.path = ''

        self.minimap = WindowCapture(area='minimap')
        self.worldmap = worldmap
    
    def walk(self):
        opoint = self.path[0]
        start = time.time()
        current = time.time() + 5
        
        while True:
            coordinates = self.get_coordinates()
            d = map(lambda t: ((t[0] - coordinates[0])**2 + (t[1] - coordinates[1])**2)**0.5, self.path)
            arr = np.array(list(d))
            ind = np.where(arr < 100)
            ind = ind[0].tolist()
            possible_points = self.path[ind[-7]:ind[-1]]
            point = random.choice(possible_points)

            if coordinates == self.path[-1]:
                print('finished walk!')
                break

            rel_point = self.get_relative_point(coordinates, point)

            opoint = point

            if current - start > 4:
                hWnd = win32gui.FindWindow(None, "BlueStacks")
                lParam = win32api.MAKELONG(1720+rel_point[0], 185+rel_point[1])
                hWnd1 = win32gui.FindWindowEx(hWnd, None, None, None)
                win32gui.SendMessage(hWnd1, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
                win32gui.SendMessage(hWnd1, win32con.WM_LBUTTONUP, None, lParam)
                start = time.time()
            
            current = time.time()

    def get_coordinates(self):
        self.minivision = Vision(self.minimap.get_screenshot())
        rectangles = self.minivision.find(cv.imread(self.worldmap),1)
        coordinates = self.minivision.get_center(rectangles)
        return coordinates

    def get_relative_point(self, coordinates, point):
        p = tuple(map(lambda i, j: i - j, point, coordinates))
        return list(p)

    def get_path(self,name):
        path = []
        while True:
            im = cv.imread(self.worldmap)
            coordinates = self.get_coordinates()
            for coords in path:
                cv.drawMarker(im, coords, (255,255,255),markerType=cv.MARKER_SQUARE, markerSize=2)
            cv.drawMarker(im,coordinates, (255,255,0),markerType=cv.MARKER_SQUARE, markerSize=5)
            cv.putText(im,str(coordinates),tuple(np.subtract(coordinates,(70, 20))),cv.FONT_HERSHEY_COMPLEX,1,(255,255,0),2)
            cv.imshow("loc",im)
            #cv.imshow(self.minimap)
            if coordinates not in path:
                path.append(coordinates)
                print(len(path))
            if cv.waitKey(1) == ord('q'):
                with open('walking_lists/'+name+".pkl", 'wb') as pickle_file:
                    pickle.dump(path, pickle_file, protocol=pickle.HIGHEST_PROTOCOL) 
                cv.destroyAllWindows()
                break
        return coordinates

    @staticmethod
    def map_images():
        map = WindowCapture(area='map')
        hWnd = win32gui.FindWindow(None, "BlueStacks")
        lParam = win32api.MAKELONG(500, 400)
        hWnd1= win32gui.FindWindowEx(hWnd, None, None, None)

        i = 1

        while True:
            cv.imwrite("map//"+str(i)+".png",map.get_screenshot())
            for lp1 in range(4):
                for lp in range(random.randrange(300,500)):
                    win32gui.SendMessage(hWnd1, win32con.WM_MOUSEWHEEL, None, lParam)    
                time.sleep(0.2)
            i += 1

    @staticmethod
    def map_stitching():
        image_paths = ["map//one.png","map//two.png"]
        images = []
        for image in image_paths:
            img = cv.imread(image)
            images.append(img)

        imageStitcher = cv.Stitcher.create()
        error, stitched_img = imageStitcher.stitch(images)


        cv.imwrite("map//stitched_output.png",stitched_img)

        if(error==cv.STITCHER_OK):
            print("created")
            cv.imshow("1",stitched_img)
            cv.waitKey(1)
        else:
            print("error")

