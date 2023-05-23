import pygame
import pygame_gui
from pygame_gui.core import ObjectID

from assets import image_keys
from scene import Scene
from states import MultiRoleState
from widgets import FocusableUIButton

from config import get_screen_width, get_screen_height, vw, vh
from utils.image_utility import load_image

class MultiRoleScene(Scene):
    def __init__(self, screen, gui_manager, params=None, server=None):
        super().__init__(screen, gui_manager, params, server)
        self.state = MultiRoleState()

        self.lobby_image = load_image("lobby_img/lobby_bg.png")
        self.lobby_image = pygame.transform.scale(self.lobby_image, (get_screen_width(), get_screen_height()))

        self.create_role_buttons()

    def create_role_buttons(self):
        btn_role_server = FocusableUIButton(
            relative_rect=pygame.Rect(get_screen_width()/2 - vw(400), get_screen_height() / 2 - vh(150), vw(300), vh(300)),
            text="server",
            manager=self.gui_manager,
            object_id=ObjectID(object_id=f"button_b_1", class_id="@lobby_role_btns")
        )
        btn_role_client = FocusableUIButton(
            relative_rect=pygame.Rect(get_screen_width()/2 + vw(100), get_screen_height() / 2 - vh(150), vw(300), vh(300)),
            text="client",
            manager=self.gui_manager,
            object_id=ObjectID(object_id=f"button_b_1", class_id="@lobby_role_btns")
        )
        self.focusable_buttons.extend([btn_role_server, btn_role_client])

    def process_events(self, event):
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                print(event.ui_element)
                if event.ui_element == self.focusable_buttons[0]:
                    self.state.start_role_server()
                elif event.ui_element == self.focusable_buttons[1]:
                    self.state.start_role_client()

    def draw(self):
        self.screen.blit(self.lobby_image, (0, 0))

        self.gui_manager.draw_ui(self.screen)
