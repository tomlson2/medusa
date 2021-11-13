import pyautogui
import random
import numpy as np
import time
from scipy import interpolate
import math
import random

def bezier_move(x1,y1,x2,y2):

    pyautogui.PAUSE = 0
    pyautogui.MINIMUM_SLEEP = 0
    pyautogui.MINIMUM_DURATION = 0

    cp = random.randint(5, 6)  # Number of control points. Must be at least 2.

    # Distribute control points between start and destination evenly.
    x = np.linspace(x1, x2, num=cp, dtype='int')
    y = np.linspace(y1, y2, num=cp, dtype='int')

    # Randomise inner points a bit (+-RND at most).
    RND = 10
    xr = [random.randint(-RND, RND) for k in range(cp)]
    yr = [random.randint(-RND, RND) for k in range(cp)]
    xr[0] = yr[0] = xr[-1] = yr[-1] = 0
    x += xr
    y += yr

    # Approximate using Bezier spline.
    degree = 3 if cp > 3 else cp - 1  # Degree of b-spline. 3 is recommended.
                                    # Must be less than number of control points.
    tck, u = interpolate.splprep([x, y], k=degree)
    # Move upto a certain number of points
    u = np.linspace(0, 1, num=2+int(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)/50.0))
    points = interpolate.splev(u, tck)

    # Move mouse.
    duration = random.uniform(0.35,0.4)
    timeout = duration / len(points[0])
    point_list=zip(*(i.astype(int) for i in points))
    for point in point_list:
        timeout = timeout*0.8
        pyautogui.moveTo(point)
        time.sleep(timeout)