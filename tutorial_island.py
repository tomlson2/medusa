from vision import Vision
from interactions import Interactions


inventory = Interactions(area='inventory')
screen = Interactions()


inventory.amount(Vision('Needle\\need.png'))

# username = str(uuid4())[:8]Ble

# hWnd = win32gui.FindWindow(None, "BlueStacks")
# hWnd1 = win32gui.FindWindowEx(hWnd, None, None, None)
# for char in username:
#     win32api.PostMessage(hWnd1, win32con.WM_CHAR, ord(char), 0)
#     print(char)
#     time.sleep(1)



