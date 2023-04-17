import pygame
import pygame_gui

from assets import image_keys
from scene import Scene
from states import LandingState

from config import SCREEN_WIDTH, SCREEN_HEIGHT, vw, vh

class LandingScene(Scene):
    def __init__(self, screen, gui_manager):
        super().__init__(screen, gui_manager)
        self.state = LandingState()
        #self.logo_image = image_loader.get_image(image_keys.IMG_LOGO)
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
