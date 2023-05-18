import pygame
import pygame_gui
from pygame_gui.core import ObjectID

from config.configuration import get_screen_width, get_screen_height, vw, vh, vp, KEYBOARD_MAP, get_action

from scene import Scene
from states import MultiIPState
from utils import action_name, overlay_name, scene_name
from utils.image_utility import load_image
from widgets import FocusableUIButton
from classes.auth.user import User

class MultiIPScene(Scene):
    def initialize_elements(self):
        self.create_below_buttons()

    def __init__(self, screen, gui_manager, params=None):
        super().__init__(screen, gui_manager, params)
        self.state = MultiIPState()

        self.lobby_image = load_image("lobby_img/lobby_bg.png")
        self.lobby_image = pygame.transform.scale(self.lobby_image, (get_screen_width(), get_screen_height()))

        self.player_bg = load_image("lobby_img/player_bg.png")
        self.player_bg = pygame.transform.scale(self.player_bg, vp(338, 400))

        self.btn_left = load_image("lobby_img/btn_left.png")
        self.btn_right = load_image("lobby_img/btn_right.png")
        self.btn_left = pygame.transform.scale(self.btn_left, vp(64.95, 57))
        self.btn_right = pygame.transform.scale(self.btn_right, vp(64.95, 57))

        self.move_scene_buttons = []

        self.text_input_ip = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(vp(523, 300), vp(235, 52)),
            manager=self.gui_manager,
        )

        self.game_IP = ""

        self.initialize_elements()

    def create_below_buttons(self):
        btn_left = FocusableUIButton(
            relative_rect=pygame.Rect(vw(50), get_screen_height() - vh(100), vw(64.95), vh(57)),
            text="",
            manager=self.gui_manager,
            object_id=ObjectID(object_id=f"button_b_1", class_id="@lobby_below_btns")
        )
        btn_right = FocusableUIButton(
            relative_rect=pygame.Rect((get_screen_width() - vw(100), get_screen_height() - vh(100)), vp(64.95, 57)),
            text="",
            manager=self.gui_manager,
            object_id=ObjectID(object_id=f"button_b_2", class_id="@lobby_below_btns")

        )
        btn_left.drawable_shape.states['normal'].surface.blit(self.btn_left, (0, 0))
        btn_right.drawable_shape.states['normal'].surface.blit(self.btn_right, (0, 0))
        btn_left.drawable_shape.active_state.has_fresh_surface = True
        btn_right.drawable_shape.active_state.has_fresh_surface = True
        self.focusable_buttons.extend([btn_left, btn_right])
        self.move_scene_buttons.extend([btn_left, btn_right])

    def process_events(self, event):
        if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
            if event.ui_element == self.text_input_ip:
                self.game_IP = self.text_input_ip.get_text()
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.move_scene_buttons[0]:
                    self.state.move_scene(scene_name.MULTI_ROLE_SCENE)
                if event.ui_element == self.move_scene_buttons[1]:
                    self.state.move_scene(scene_name.MULTI_ACCESS_SCENE)

    def draw(self):
        font = pygame.font.SysFont('arial', 30)
        text_title = font.render("Input Game IP", True, (255, 255, 255))
        text_enter = font.render("Press Enter Setting", True, (255, 255, 255))

        self.screen.blit(self.lobby_image, (0, 0))
        self.screen.blit(self.player_bg, vp(472, 109))

        self.gui_manager.draw_ui(self.screen)

        self.screen.blit(text_title, vp(540, 180))
        self.screen.blit(text_enter, vp(510, 400))

