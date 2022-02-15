import win32api
import keyboard
import time

made = False

# qqzqqzqqzqqzqqzqqzqqzqqzqqzqqzqqzqqzqqzqqzqqzqqzqqxzqqzqqz

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
        print("self.w = "+str(w)+"\n            self.h = "+str(h)+"\n            self.x = "+str(x)+"\n            self.y = "+str(y)+"\n\n"+str(x)+","+str(y)+","+str(w)+","+str(h))
        print(f'real y = {y - 32}')
        break