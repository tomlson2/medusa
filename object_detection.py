import torch
import cv2 as cv
import pandas
from time import time



model = torch.hub.load('ultralytics/yolov5', 'custom', 'model_data\\master_farmer_best.pt')
# while True:
#     image = 'image.png'
#     img = cv.cvtColor(image, cv.COLOR_BGR2RGB)
#     #cv.imwrite('mf.png', image)
#     results = model(img)
#     labels, cord = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]
#     w, h = img.shape[1], img.shape[0]
#     print(cord)
#     n = len(labels)
#     x_shape, y_shape = img.shape[1], img.shape[0]
#     for i in range(n):
#         row = cord[i]
#         if row[4] >= 0.2:
#             x1, y1, x2, y2 = int(row[0]*x_shape), int(row[1]*y_shape), int(row[2]*x_shape), int(row[3]*y_shape)
#             # bgr = (0, 255, 0)
#             # cv2.rectangle(img, (x1, y1), (x2, y2), bgr, 2)
#             # cv2.putText(img, self.class_to_label(labels[i]), (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.9, bgr, 2)
#             width = x2 - x1
#             height = y2 - y1
#             cv.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
#     cv.imshow('xd', img)
#     if cv.waitKey(1) == ord('q'):
#         cv.destroyAllWindows()
#         break
