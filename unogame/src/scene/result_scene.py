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

        self.winner_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((vw(get_screen_width() / 2 - 170), vh(get_screen_height() / 2)), (vw(300), vh(60))),
            text=str(params['winner'].name)+" is Winner!!",
            manager=self.gui_manager
        )

        self.go_menu_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((vw(get_screen_width() / 2 - 170), vh(get_screen_height() / 2 + 170)),
                                      (vw(300), vh(60))),
            text="go to menu",
            manager=self.gui_manager
        )

    def process_events(self, event):
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                print(event.ui_element)
                if event.ui_element == self.go_menu_button:
                    self.state.go_main_menu()

    def draw(self):
        self.screen.fill((141, 168, 68))
        self.screen.blit(self.logo_image, (vw(get_screen_width() / 2 - 130), vh(100)))
        self.gui_manager.draw_ui(self.screen)
