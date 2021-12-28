import win32api
import keyboard
import time

made = False

while True:
    if keyboard.is_pressed("q"):
        if made == True:
            x2, y2 = win32api.GetCursorPos()
            time.sleep(0.5)
        else:
            x,y = win32api.GetCursorPos()
            made = True
            time.sleep(0.5)
    if keyboard.is_pressed("z"):
        w = x2-x
        h = y2-y
        print("self.w = "+str(w)+"\nself.h = "+str(h)+"\nself.x = "+str(x)+"\nself.y = "+str(y))
        break