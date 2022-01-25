import os
import pandas as pd
import pandas as pd
from osrsbox import items_api
import base64
import os
from PIL import Image
import sys
import cv2 as cv
import numpy as np

def get_item_png():

    items = items_api.load()

    for item in items:
        icon = item.icon
        name = item.wiki_name
        print(name)
        bytes = icon.encode('utf-8')
        try:
            path = "needles//"+name+".png"
            if os.path.isfile(path):
                pass
            else:
                with open(path, 'wb') as file_to_save:
                    decoded_image_data = base64.decodebytes(bytes)
                    file_to_save.write(decoded_image_data)
                blur("needles//"+name+".png",name)
        except TypeError:
            pass
        except FileNotFoundError:
            pass
        except OSError:
            pass
        except cv.error as e:
            pass

def reduce_quality(path, file_name):
    image = Image.open(os.path.join(path, file_name))
    image.save("output_"+file_name, "PNG",)

def blur():
    imgs = os.listdir("needles//")
    for img in imgs:
        try:
            im = cv.imread("needles//"+img)
            bimg = cv.blur(im, ksize=(2,2))
            cv.imwrite("b_needles//"+img,bimg)
        except cv.error as e:
            pass
        print(len(os.listdir("b_needles//")))

def crop_black(path):
    try:
        img = cv.imread(path)
        gimg = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        _,thresh = cv.threshold(gimg,1,255,cv.THRESH_BINARY)
        c,h = cv.findContours(thresh,cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        cnt = c[0]
        x,y,w,h = cv.boundingRect(cnt)
        crop = img[y:y+h,x:x+w]
        #crop[np.where((crop==[0,0,0]).all(axis=2))] = [255,255,255]
        cv.imwrite(path,crop)
    except cv.error as e:
        pass

def pad(path,h,w):
    im = cv.imread(path)
    x,y,c = im.shape
    bw = w-y
    bh = h-x
    resized_im = cv.copyMakeBorder(im, bh, bh, bw, bw, borderType=cv.BORDER_CONSTANT)
    cv.imwrite(path+"//padded",resized_im)

def add_margin(pil_img, top, right, bottom, left, color):
    width, height = pil_img.size
    new_width = width + right + left
    new_height = height + top + bottom
    result = Image.new(pil_img.mode, (new_width, new_height), color)
    result.paste(pil_img, (left, top))
    return result

im = Image.open('map/motherlode.png')
imnew = add_margin(im,100, 100, 100, 100, color=(85,73,41))
imnew.save('map/motherlode2.png')
