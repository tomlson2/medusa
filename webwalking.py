import cv2 as cv
import time
from vision import Vision
import win32gui, win32api, win32con
import random
import numpy as np
import win32gui, win32con
import pickle
from windowcapture import MinimapRegion, WindowCapture, RunOrb



class WebWalking(WindowCapture):
    """
    WebWalking object, pass path to pickle list and map png
    """
    def __init__(self, path: str, worldmap: str, orientation: str = 'North'):
        super().__init__()

        try:
            with open(path, 'rb') as pickle_load:
                self.path = pickle.load(pickle_load)
        except FileNotFoundError:
            self.path = ''
        
        self.worldmap = worldmap
        if orientation == 'North':
            self.rotate_code = None
        if orientation == 'South':
            self.rotate_code = cv.ROTATE_180
        if orientation == 'East':
            self.rotate_code = cv.ROTATE_90_COUNTERCLOCKWISE
        if orientation == 'West':
            self.rotate_code = cv.ROTATE_90_CLOCKWISE
    
    def walk_once(self, dist = 100):
        coordinates = self.get_coordinates()
        d = map(lambda t: ((t[0] - coordinates[0])**2 + (t[1] - coordinates[1])**2)**0.5, self.path)
        arr = np.array(list(d))
        ind = np.where(arr < dist)
        ind = ind[0].tolist()
        possible_points = self.path[ind[-6]:ind[-1]]
        rel_point = self.get_relative_point(coordinates, random.choice(possible_points))
        hWnd = win32gui.FindWindow(None, self.window_name)
        lParam = win32api.MAKELONG(1716+rel_point[0], 185+rel_point[1])
        hWnd1 = win32gui.FindWindowEx(hWnd, None, None, None)
        win32gui.SendMessage(hWnd1, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
        win32gui.SendMessage(hWnd1, win32con.WM_LBUTTONUP, None, lParam)
        time.sleep(0.25)
    
    def coords_change(self, threshold = 3):
        starting = self.get_coordinates()
        time.sleep(2)
        if self.get_coordinates == starting:
            return False
        else:
            return True

    def walk(self, within: int = 1, debugger = True, ind_len = -4):
        print("WALKING")
        opoint = self.path[0]
        click_wait = 0
        start = time.time()
        current = 0
        first = True
        arrived = False
        while True:
            while True:
                im = self.show_coords()
                for coords in self.path:
                    image = cv.drawMarker(im, coords, (0,0,255),markerType=cv.MARKER_SQUARE, markerSize=4)
                coordinates = self.get_coordinates()
                d = map(lambda t: ((t[0] - coordinates[0])**2 + (t[1] - coordinates[1])**2)**0.5, self.path)
                arr = np.array(list(d))
                #changed from 103 to 138, i dont know if breaks other scripts
                #TODO add points to list (ln44) where they are a certain distance away on minimap or 
                ind = np.where(arr < 160)
                ind = ind[0].tolist()
                possible_points = self.path[ind[ind_len]:ind[-1]]
                point = random.choice(possible_points)
                
                if debugger == True:
                    if coordinates in self.path:
                        color = (0,255,0)
                    else:
                        color = (0,0,255)

                    image = cv.putText(image,str(coordinates), (150,40),cv.FONT_HERSHEY_PLAIN,3,color,1)
                    image = cv.drawMarker(image,coordinates, (0,255,0),markerType=cv.MARKER_DIAMOND, markerSize=8,thickness=4)
                    cv.imshow('Map', image)

                    if cv.waitKey(1) == ord('q'):
                        cv.destroyAllWindows()
                        break
                
                x1,x2,y1,y2 = self.within_distance(within)

                if  (x1 <= coordinates[0] <= x2 and y1 <= coordinates[1] <= y2):
                    cv.destroyAllWindows()
                    time.sleep(random.normalvariate(0.3,0.05))
                    arrived = True
                    break

                rel_point = self.get_relative_point(coordinates, point)

                opoint = point

                if RunOrb().is_active():
                    click_wait = 4
                else:
                    click_wait = 7

                if first == True:
                    first = False
                    break
                if current - start < random.normalvariate(click_wait,0.1):
                        current = time.time()
                        pass
                else:
                    break
            if  arrived == True:
                break
            hWnd = win32gui.FindWindow(None, self.window_name)
            # TODO Click point within 2 pixels, not exact
            lParam = win32api.MAKELONG(1716+rel_point[0], 185+rel_point[1])
            hWnd1 = win32gui.FindWindowEx(hWnd, None, None, None)
            win32gui.SendMessage(hWnd1, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
            win32gui.SendMessage(hWnd1, win32con.WM_LBUTTONUP, None, lParam)
            start = time.time()
    

    def end_of_path(self, within : int = 1):
        coordinates = self.get_coordinates()
        x1,x2,y1,y2 = self.within_distance(within)

        if (x1 <= coordinates[0] <= x2 and y1 <= coordinates[1] <= y2):
            return True
        else:
            return False
    

    def show_coords(self):

        x = 10
        y = 20
        if self.rotate_code == None:
            im = cv.imread(self.worldmap)
        else:
            im = cv.rotate(cv.imread(self.worldmap), self.rotate_code)
        for coord in self.path:
            im = cv.putText(im, str(coord), ((x,y)),cv.FONT_HERSHEY_PLAIN,1,(255,255,255),1)
            y = y+20
        return im


    def get_path(self,name):
        path = []
        while True:
            if self.rotate_code == None:
                im = cv.imread(self.worldmap)
            else:
                im = cv.rotate(cv.imread(self.worldmap), self.rotate_code)
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


    def get_coordinates(self):
        self.minivision = Vision(MinimapRegion().get_screenshot())
        if self.rotate_code == None:
            rectangles = self.minivision.find(cv.imread(self.worldmap),1)
        else:
            rectangles = self.minivision.find(cv.rotate(cv.imread(self.worldmap),self.rotate_code),1)
        coordinates = self.minivision.get_center(rectangles)
        return coordinates


    def get_relative_point(self, coordinates, point):
        p = tuple(map(lambda i, j: i - j, point, coordinates))
        return list(p)
    

    def within_distance(self, within : int):
            pixels = within * 3

            x1 = self.path[-1][0] - pixels
            x2 = self.path[-1][0] + pixels
            y1 = self.path[-1][1] - pixels
            y2 = self.path[-1][1] + pixels

            return x1,x2,y1,y2
            
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

if __name__ == '__main__':
    WebWalking('','map\\motherlode2.png',orientation='West').get_path("to_rocks")
