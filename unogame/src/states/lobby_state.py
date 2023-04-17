from states import GameState
from utils import scene_name


class LobbyState(GameState):
    def __init__(self):
        super().__init__()

    def start_single_play(self, players):
        self.move_scene(scene_name.PLAYING_GAME, players)