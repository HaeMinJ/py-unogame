import pygame
import pygame_gui
from pygame_gui.core import ObjectID

from config.configuration import get_screen_width, get_screen_height, vw, vh, vp, KEYBOARD_MAP, get_action

from scene import Scene
from states import MultiAccessState
from utils import action_name, overlay_name, scene_name
from utils.image_utility import load_image
from widgets import FocusableUIButton
from classes.auth.user import User

class MultiAccessScene(Scene):
    def initialize_elements(self):
        self.create_below_buttons()
        self.create_access_buttons()

    def __init__(self, screen, gui_manager, params=None, server=None):
        super().__init__(screen, gui_manager, params, server)
        self.state = MultiAccessState()

        self.lobby_image = load_image("lobby_img/lobby_bg.png")
        self.lobby_image = pygame.transform.scale(self.lobby_image, (get_screen_width(), get_screen_height()))

        self.player_bg = load_image("lobby_img/player_bg.png")
        self.player_bg = pygame.transform.scale(self.player_bg, vp(338, 400))

        self.input_password_bg = load_image("lobby_img/player_bg.png")
        self.input_password_bg = pygame.transform.scale(self.input_password_bg, vp(338, 400))

        self.btn_left = load_image("lobby_img/btn_left.png")
        self.btn_right = load_image("lobby_img/btn_right.png")
        self.btn_left = pygame.transform.scale(self.btn_left, vp(64.95, 57))
        self.btn_right = pygame.transform.scale(self.btn_right, vp(64.95, 57))

        self.btn_set_player = load_image("lobby_img/btn_set_player.png")
        self.btn_set_player = pygame.transform.scale(self.btn_set_player, vp(160, 83))

        self.move_scene_buttons = []

        self.text_input_ip = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(vp(223, 250), vp(235, 52)),
            manager=self.gui_manager,
        )
        self.text_input_password = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(vp(690, 300), vp(235, 52)),
            manager=self.gui_manager,
        )
        self.text_input_password.visible = False

        self.game_ip = "123.123.123"
        self.input_ip = ""
        self.game_password = "123123"
        self.input_password = ""

        self.is_password_access = False
        self.is_lobby_access = False

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

    def create_access_buttons(self):
        btn_ip_access = FocusableUIButton(
            relative_rect=pygame.Rect(vw(260), vh(400), vw(160), vh(83)),
            text="",
            manager=self.gui_manager,
            object_id=ObjectID(object_id=f"button_b_1", class_id="@lobby_add_btns")
        )
        btn_ip_access.drawable_shape.states['normal'].surface.blit(self.btn_set_player, (0, 0))
        btn_ip_access.drawable_shape.active_state.has_fresh_surface = True
        self.focusable_buttons.append(btn_ip_access)

    def process_events(self, event):
        if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
            if event.ui_element == self.text_input_ip:
                self.input_ip = self.text_input_ip.get_text()
            if event.ui_element == self.text_input_password:
                self.input_password = self.text_input_password.get_text()
                if self.input_password == self.game_password:
                    print("Access Success!")
                    self.is_lobby_access = True
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.focusable_buttons[2]:
                    self.state.connect_server(self.input_ip,"asdf1234")
                    if self.input_ip == self.game_ip:
                        self.is_password_access = True
                    if self.is_password_access == True:
                        self.text_input_password.visible = True
                if event.ui_element == self.move_scene_buttons[0]:
                    self.state.move_scene(scene_name.MULTI_ROLE_SCENE)
                if event.ui_element == self.move_scene_buttons[1]:
                    pass


    def draw(self):
        font = pygame.font.SysFont('arial', 30)
        text_title = font.render("Input Game IP", True, (255, 255, 255))
        text_enter = font.render("ACCESS", True, (0, 0, 0))

        text_password_title = font.render("Input Password", True, (255, 255, 255))
        text_enter_second = font.render("Press Enter Setting", True, (255, 255, 255))

        self.screen.blit(self.lobby_image, (0, 0))
        self.screen.blit(self.player_bg, vp(172, 109))

        self.screen.blit(self.input_password_bg, vp(get_screen_width() / 2, 109))

        self.gui_manager.draw_ui(self.screen)

        self.screen.blit(text_title, vp(240, 180))
        self.screen.blit(text_enter, vp(280, 420))
        self.screen.blit(text_enter_second, vp(210, 330))


        self.screen.blit(text_password_title,  vp(700, 180))
        self.screen.blit(text_enter_second, vp(680, 400))


