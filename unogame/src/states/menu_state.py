import pygame

from states import GameState
from utils import scene_name, overlay_name


class MenuState(GameState):
    def __init__(self):
        super().__init__()
        self.changed = False

    def start_single_play(self):
        self.move_scene(scene_name.LOBBY_SCENE)

    def open_configuration(self):
        self.active_overlay(overlay_name.CONFIGURATION)

    def toggle_configuration(self):
        if self.overlay_active:
            self.inactive_overlay(overlay_name.CONFIGURATION)
        else:
            self.active_overlay(overlay_name.CONFIGURATION)

    def open_story_play(self):
        self.move_scene(scene_name.STORY_MAP_SCENE)

    def exit(self):
        pygame.quit()
