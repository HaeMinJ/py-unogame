from states import GameState

from utils import scene_name, overlay_name

class PlayingState(GameState):
    def __init__(self):
        super().__init__()
        self.game_over = False

    def end_game(self):
        pass

    def back_to_main_menu(self):
        pass

    def move_menu_scene(self):
        self.move_scene(scene_name.MAIN_MENU)

    def exit(self):
        pass
