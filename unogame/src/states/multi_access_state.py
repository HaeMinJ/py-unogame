import pygame

from multiplay.multi_networking import MultiNetworking
from states import GameState
from utils import scene_name


class MultiAccessState(GameState):
    def __init__(self):
        super().__init__()
        self.timer_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.timer_event, 3000)

    def start(self, event):
        if event.type == self.timer_event:
            self.move_scene(scene_name.MAIN_MENU)

    def connect_server(self, SERVER_IP, PASSWORD):
        networking = MultiNetworking(SERVER_IP)
        networking.access_lobby(PASSWORD)