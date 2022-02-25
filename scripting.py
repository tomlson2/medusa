import time
import random
from vision import Vision
from windowcapture import ScreenRegion
import logging

path = 'Needle\\scripting\\'
screen = ScreenRegion()
class Script(object):
    
    def __init__(self, breaking=True, show_log=False) -> None:

        print(f'Starting {__class__.__subclasses__()[0].__name__}')

        # set time vars
        self.script_time = time.time()
        self.session_time = time.time()
        self.breaking = breaking
        self.show_log = show_log
        self.break_time = self.set_break_time()
        self.break_duration = self.set_break_duration()

        # set logger
        logging.basicConfig(format='DEBUGGER: %(message)s')
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        self.logger = logger


        # load vision objects
        self.inventory_closed = Vision(path + 'inventory_pane.png')
        self.logout_pane = Vision(path + 'logout_pane.png')
        self.tap_here_to_logout = Vision(path + 'tap_here_to_logout.png')
        self.play_now = Vision(path + 'play_now.png')
        self.tap_here_to_play = Vision(path + 'tap_here_to_play.png')
        self.world_map = Vision(path + 'world_map.png')

        self.xp = 0
        self.gp = 0

    def set_xp(self, amount):
        self.xp += amount

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
    
    def log(self, message: str):
        if self.show_log is True:
            self.logger.info(message)

    def break_handler(self):
        if self.breaking is True and self.get_session_time() > self.break_time:
            time.sleep(self.break_duration)
            if self.login() is True:
                print("Break completed")
                self.set_break_duration()
                self.set_break_time()
                self.set_session_time()
            else:
                print("Failed to log in")
    
    def print_time(self):
        if self.show_log is False:
            line_end = '\r'
        else:
            line_end = '\n'
        print(f'runtime: {self.get_runtime()} time to break: {self.get_time_to_break()}', end=line_end)
            
        
    def login(self) -> bool:
        screen.click(self.play_now)
        screen.wait_for(self.tap_here_to_play)
        screen.click(self.tap_here_to_play)
        screen.wait_for(self.world_map)
        return True

    def logout(self) -> None:
        pass

        


