import torch
from vision import Vision
import numpy as np
import cv2 as cv


class Model(Vision):

    def __init__(self, weight_path, label_idx = 0):
        print("Loading Model..")
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path=weight_path)
        self.label_idx = label_idx
        print("Model Loaded!")

    def print_results(self, im, threshold=0.5):
        im = cv.cvtColor(im, cv.COLOR_BGR2RGB)
        result = self.model([im])
        labels, coord = result.xyxyn[0][:, -1], result.xyxyn[0][:, :-1]

    def find(self, im, threshold=0.5):
        im = cv.cvtColor(im, cv.COLOR_BGR2RGB)
        result = self.model([im])
        labels, coord = result.xyxyn[0][:, -1], result.xyxyn[0][:, :-1]
        im_h, im_w, _ = im.shape
        coords_list = []
        n = len(labels)
        
        for i in range(n):
            if labels[i] == self.label_idx:
                row = coord[i]
                if row[4] >= threshold:
                    x1, y1, x2, y2 = int(row[0] * im_w), int(row[1] * im_h), int(row[2] * im_w), int(row[3] * im_h)
                    x = x1
                    y = y1
                    w = (x2 - x1)
                    h = (y2 - y1)
                    coords_list.append([x,y,w,h])

        
        rectangles = np.asarray(coords_list)

        return rectangles


class NPC(Model):
    def __init__(self, weight_path, label_idx=0):
        super().__init__(weight_path, label_idx)
        self.label_idx = label_idx