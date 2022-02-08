from windowcapture import ScreenRegion
import cv2 as cv
import numpy as np
import os

screen = ScreenRegion()
OBJECT_DETECTOR = cv.createBackgroundSubtractorMOG2(history=10, varThreshold=0.001)
parent_dir = "model_data/"


def find_if_close(cnt1,cnt2):
    row1,row2 = cnt1.shape[0],cnt2.shape[0]
    for i in range(row1):
        for j in range(row2):
            dist = np.linalg.norm(cnt1[i]-cnt2[j])
            if abs(dist) < 15 :
                return True
            elif i==row1-1 and j==row2-1:
                return False

def group_contours():
    firstl = True
    while True:
        if firstl == True:
            for i in range(70):
                im = screen.get_screenshot()
                mask = OBJECT_DETECTOR.apply(im)
        else:
            im = screen.get_screenshot()
            mask = OBJECT_DETECTOR.apply(im)
        contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        contours2 = []

        for cnt in contours:
            if cv.contourArea(cnt) > 150:
                contours2.append(cnt)
        LENGTH = len(contours2)
        print(LENGTH)
        status = np.zeros((LENGTH,1))

        for i,cnt1 in enumerate(contours2):
            x = i
            print(i)    
            if i != LENGTH-1:
                for j,cnt2 in enumerate(contours2[i+1:]):
                    x = x+1
                    dist = find_if_close(cnt1,cnt2)
                    if dist == True:
                        val = min(status[i],status[x])
                        status[x] = status[i] = val
                    else:
                        if status[x]==status[i]:
                            status[x] = i+1

        unified = []
        maximum = int(status.max())+1
        for i in range(maximum):
            pos = np.where(status==i)[0]
            if pos.size != 0:
                cont = np.vstack(contours2[i] for i in pos)
                hull = cv.convexHull(cont)
                unified.append(hull)

        cv.drawContours(im,unified,-1,(0,255,0),2)
        #cv.drawContours(thresh,unified,-1,255,-1)

        cv.imshow("1", im)

        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            break

def npc_labeling():
    DIR = input('Name: ')
    class_input = input('Names of classes seperated by space: ')
    data_types = class_input.split()
    path = os.path.join(parent_dir, DIR)
    os.mkdir(path)

    DIRS = ["images/train","images/val","labels/train","labels/val"]

    for d in DIRS:
        d_path = os.path.join(path, d)
        os.makedirs(d_path)

    OBJECT_DETECTOR = cv.createBackgroundSubtractorMOG2(history=70, varThreshold=0.005)
    image_number = 0
    fmt = '%d','%1.6f','%1.6f','%1.6f','%1.6f'
    first_loop = True
    
    while True:
        if first_loop == True:
            for i in range(70):
                im = screen.get_screenshot()
                mask = OBJECT_DETECTOR.apply(im)
                first_loop = False
        else:
            im = screen.get_screenshot()
            mask = OBJECT_DETECTOR.apply(im)
        im_h, im_w, _ = im.shape
        blur = cv.GaussianBlur(mask, (1, 1), cv.BORDER_DEFAULT)
        contours, _ = cv.findContours(blur, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        temp_im = im.copy()

        rectangles = []
        for cnt in contours:
            area = cv.contourArea(cnt)
            if area > 2500:
                x, y, w, h = cv.boundingRect(cnt)
                cv.rectangle(temp_im, (x, y), (x + w, y + h), (0, 255, 0), 2)
                rectangles.append((x, y, w, h))
        
        CLASS_X = 50
        INDEX_X = 20
        text_y = 30
        keys = []

        for idx, cl in enumerate(data_types):
            temp_im = cv.putText(temp_im, str(idx+1), (INDEX_X, text_y),cv.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
            temp_im = cv.putText(temp_im, cl, (CLASS_X,text_y),cv.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
            text_y += 30
    
        broken = False
        broken2 = False
        cows = []
        
        if len(rectangles) > 1:
            for rect in rectangles:
                temp_im = cv.rectangle(temp_im, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]),(255, 0, 0), 3)
                cv.imshow('test',temp_im)
                temp_im = cv.rectangle(temp_im, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]),(0, 255, 0), 3)
                key = cv.waitKey(0)

                if key == ord('1'):
                    label_list = label_format(rect, im_w, im_h, class_index=0)
                    cows.append(label_list)
                    print("added data point")
                if key == ord('2'):
                    broken = True
                    break
                if key == ord('q'):
                    cv.destroyAllWindows()
                    broken2 = True
                    break

            if broken2 == True:
                print("data collection terminated")
                break
            
            label_array = np.asarray(cows, dtype=np.float64)

            if len(cows) > 1 and broken == False:
                with open(f"{path}\\labels\\{image_number}.txt", "wb") as f:
                    np.savetxt(f, label_array, fmt=fmt)
                cv.imwrite(f"{path}\\images\\{image_number}.png", im)

            image_number += 1
        
def label_format(rect, im_w, im_h, class_index):
    x, y, w, h = rect
    center_x = (x + (w / 2))
    center_y = (y + (h / 2))
    rect_x = (center_x / im_w)
    print(rect_x, center_x)
    rect_y = (center_y / im_h)
    rect_w = (w / im_w)
    rect_h = (h / im_h)
    label_list = [float(class_index), rect_x, rect_y, rect_w, rect_h]
    return label_list

if __name__ == '__main__':
    npc_labeling()