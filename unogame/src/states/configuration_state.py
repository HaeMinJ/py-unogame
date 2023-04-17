import string

from states import GameState
from utils import scene_name
from config import configuration


class ConfigurationState(GameState):
    def __init__(self):
        super().__init__()

    def back_to_main_menu(self):
        self.move_scene(scene_name.MAIN_MENU)

    def get_screen_size(self):
        return (configuration.SCREEN_WIDTH, configuration.SCREEN_HEIGHT)
    def set_screen_size(self, width:int, height:int):
        configuration.SCREEN_HEIGHT = height
        configuration.SCREEN_WIDTH = width

    def get_color_blind(self):
        return configuration.BLIND_MODE
    def set_color_blind(self, blind_mode:string):
        configuration.BLIND_MODE = blind_mode

    def save_to_file(self):
        configuration.save_config_to_file()

    def load_from_file(self):
        configuration.load_config_from_file()

