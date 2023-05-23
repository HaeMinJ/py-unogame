import string

from states import GameState
from utils import scene_name


class AchievementState(GameState):
    def __init__(self):
        super().__init__()

    def back_to_main_menu(self):
        self.move_scene(scene_name.MAIN_MENU)

    def get_screen_size(self, achievement=None):
        return (achievement.get_screen_width(), achievement.get_screen_height())
    def set_screen_size(self, width:int, height:int, achievement=None):
        achievement.set_screen_size(width,height)
        self.save_to_file()

    def get_color_blind(self, achievement=None):
        return achievement.BLIND_MODE
    def set_color_blind(self, blind_mode:string, achievement=None):
        achievement.BLIND_MODE = blind_mode
        self.save_to_file()

    def save_to_file(self, achievement=None):
        achievement.save_config_to_file()

    def load_from_file(self, achievement=None):
        achievement.load_config_from_file()