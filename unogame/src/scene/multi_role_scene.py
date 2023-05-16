import pygame
import pygame_gui

from assets import image_keys
from scene import Scene
from states import LandingState

from config import get_screen_width, get_screen_height, vw, vh
from utils.image_utility import load_image

class MultiRoleScene(Scene):
    def __init__(self, screen, gui_manager, params=None):
        super().__init__(screen, gui_manager, params)
        self.state = LandingState()
        self.logo_image = load_image("logo.png")
        self.single_play_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((vw(40), vh(30)), (vw(8), vh(25))),
            text="Landing",
            manager=self.gui_manager
        )

    def process_events(self, event):
        self.state.start(event)

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.logo_image, (150, 100))
        self.gui_manager.draw_ui(self.screen)
