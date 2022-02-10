import time
import random
from vision import Vision
from windowcapture import ScreenRegion

lumb_tp = Vision('Needle\\magic\\teleporter\\lumb_tp.png')
fala_tp = Vision('Needle\\magic\\teleporter\\fala_tp.png')
home_tp = Vision('Needle\\magic\\teleporter\\home_tp.png')
cam_tp = Vision('Needle\\magic\\teleporter\\cam_tp.png')

screen = ScreenRegion()

tp_count = 0
start_time = time.time()

print('--\/\/\/\/starting teleporter\/\/\/\/--')
while True:
    screen.click(cam_tp, threshold=0.9)
    time.sleep(random.normalvariate(2.02, 0.09))
    tp_count += 1
    
    if tp_count % 100 == 0:
        print(f'xp gained: {tp_count * 55.5}')
        
        current_time = (time.time() - start_time)
        current_time_format = time.strftime("%H:%M:%S", time.gmtime(current_time))
        print(f"run time: {current_time_format}")
