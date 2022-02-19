import time
import random
from vision import Vision
from windowcapture import ScreenRegion


path = 'Needle\\scripting\\'
screen = ScreenRegion()
class Script:
    
    def __init__(self) -> None:

        print("starting script")

        # set time vars
        self.script_time = time.time()
        self.session_time = time.time()
        self.breaking = True
        self.break_time = self.set_break_time()
        self.break_duration = self.set_break_duration()

        # load vision objects
        self.inventory_closed = Vision(path + 'inventory_pane.png')
        self.logout_pane = Vision(path + 'logout_pane.png')
        self.tap_here_to_logout = Vision(path + 'tap_here_to_logout.png')
        self.play_now = Vision(path + 'play_now.png')
        self.tap_here_to_play = Vision(path + 'tap_here_to_play.png')
        self.world_map = Vision(path + 'world_map.png')

    def get_runtime(self):
        runtime = time.time() - self.script_time
        runtime_fmt = time.strftime("%H:%M:%S", time.gmtime(runtime))
        return runtime_fmt
    
    def get_session_time(self):
        session_runtime = time.time() - self.session_time
        return session_runtime
    
    def set_break_time(self):
        break_time = random.randrange(300, 400) * 36
        self.break_time = break_time
        return break_time

    def set_break_duration(self):
        break_duration = random.randrange(80, 240) * 6
        self.break_duration = break_duration
        return break_duration

    def set_session_time(self):
        self.session_time = time.time()
    
    def get_time_to_break(self):
        ttb = self.break_time - self.get_session_time()
        ttb_fmt = time.strftime("%H:%M:%S", time.gmtime(ttb))
        return ttb_fmt

    def ingame_status(self):
        if screen.contains(self.world_map):
            return True
        else:
            return False

    def break_handler(self):
        if self.breaking == True and self.get_session_time() > self.break_time:
            time.sleep(self.break_duration)
            if self.login() == True:
                print("Break completed")
                self.set_break_duration()
                self.set_break_range()
                self.set_session_time()
            else:
                print("Failed to log in")
    
    def print_time(self):
        print(f'runtime: {self.get_runtime()} time to break: {self.get_time_to_break()}')
            
        
    def login(self) -> bool:
        screen.click(self.play_now)
        screen.wait_for(self.tap_here_to_play)
        screen.click(self.tap_here_to_play)
        screen.wait_for(self.world_map)
        return True

    def logout(self) -> None:
        pass

        


