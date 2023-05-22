import pygame

from states import GameState
from utils import scene_name


class ResultState(GameState):
    def __init__(self):
        super().__init__()
        self.timer_event = pygame.USEREVENT + 1000
        pygame.time.set_timer(self.timer_event, 3000)

    def start(self, event):
        if event.type == self.timer_event:
            self.move_scene(scene_name.MAIN_MENU)

    def go_main_menu(self):
        self.move_scene(scene_name.MAIN_MENU)
