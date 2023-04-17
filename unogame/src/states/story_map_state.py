from states import GameState
from utils import scene_name


class StoryMapState(GameState):
    def __init__(self):
        super().__init__()

    def start_single_play(self):
        self.move_scene(scene_name.PLAYING_GAME)
