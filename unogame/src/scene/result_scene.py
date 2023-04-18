import pygame
import pygame_gui

from assets import image_keys
from scene import Scene
from states import LandingState

from config import get_screen_width, get_screen_height, vw, vh, vp
from states.result_state import ResultState
from utils.image_utility import load_image


class ResultScene(Scene):
    def __init__(self, screen, gui_manager, params=None):
        super().__init__(screen, gui_manager, params)
        self.state = ResultState()
        self.logo_image = load_image("logo.png")
        self.single_play_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((vw(get_screen_width() / 2), vh(get_screen_height() / 2)), (vw(200), vh(40))),
            text=str(params['winner'].name)+" Win!!",
            manager=self.gui_manager
        )

    def process_events(self, event):
        self.state.start(event)

    def draw(self):
        self.screen.fill((141, 168, 68))
        self.screen.blit(self.logo_image, vp(150, 100))
        self.gui_manager.draw_ui(self.screen)
