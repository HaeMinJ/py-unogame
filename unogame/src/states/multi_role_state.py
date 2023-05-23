import pygame

from states import GameState
from utils import scene_name


class MultiRoleState(GameState):
    def __init__(self):
        super().__init__()
        self.timer_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.timer_event, 3000)

    def start_role_server(self):
        self.move_scene(scene_name.MULTI_PASSWORD_SCENE)

    def start_role_client(self):
        self.move_scene(scene_name.MULTI_ACCESS_SCENE)


