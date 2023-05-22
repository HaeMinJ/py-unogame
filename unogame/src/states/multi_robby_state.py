
from multiplay.server import Server
from states import GameState
from utils import scene_name


class MultiRobbyState(GameState):
    def __init__(self):
        super().__init__()




    def start(self, event):
        if event.type == self.timer_event:
            self.move_scene(scene_name.MAIN_MENU)
