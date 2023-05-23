import pygame
import pygame_gui
from pygame_gui.core import ObjectID
import socket

from classes.auth.ai_user import AIUser
from config.configuration import get_screen_width, get_screen_height, vw, vh, vp, KEYBOARD_MAP, get_action

from scene import Scene
from states import MultiRobbyState
from utils import action_name, overlay_name, scene_name
from utils.image_utility import load_image
from widgets import FocusableUIButton
from classes.auth.user import User


class MultiRobbyScene(Scene):
    def initialize_elements(self):
        self.create_below_buttons()

    def __init__(self, screen, gui_manager, params=None, server=None):
        super().__init__(screen, gui_manager, params, server)
        self.params = params
        self.server.current_game.append_user(User(0,"Me"))

        self.lobby_image = load_image("lobby_img/lobby_bg.png")
        self.lobby_image = pygame.transform.scale(self.lobby_image, (get_screen_width(), get_screen_height()))

        self.player_bg = load_image("lobby_img/player_bg.png")
        self.player_bg = pygame.transform.scale(self.player_bg, vp(338, 400))

        self.btn_left = load_image("lobby_img/btn_left.png")
        self.btn_right = load_image("lobby_img/btn_right.png")
        self.btn_left = pygame.transform.scale(self.btn_left, vp(64.95, 57))
        self.btn_right = pygame.transform.scale(self.btn_right, vp(64.95, 57))

        self.other_player_bg = load_image("lobby_img/other_player_bg.png")
        self.other_player_bg = pygame.transform.scale(self.other_player_bg, vp(512, 90))

        hostname = socket.gethostname()
        ## getting the IP address using socket.gethostbyname() method
        ip_address = socket.gethostbyname(hostname)
        self.my_ip_address = ip_address

        self.move_scene_buttons = []

        self.player_bg_width = vw(512)
        self.player_bg_height = vh(90)
        self.player_bg_margin = vh(13)
        self.other_players = self.server.current_game.users

        self.initialize_elements()
        self.state = MultiRobbyState()

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
        if self.server.user_list_changed:
            self.other_players = self.server.current_game.users
            self.server.user_list_changed = False
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.move_scene_buttons[0]:
                    self.state.move_scene(scene_name.MULTI_PASSWORD_SCENE)
                if event.ui_element == self.move_scene_buttons[1]:
                    self.state.move_scene(scene_name.PLAYING_SCENE, [User(0,"Me",is_ai=False), AIUser(1, "Minsu",is_ai=True) ])
                    pass

    def draw(self):
        font = pygame.font.SysFont('arial', 40)
        text_title = font.render("Game IP", True, (255, 255, 255))
        text_my_ip = font.render(self.my_ip_address, True, (100, 200, 105))
        text_password = font.render("Password", True, (255, 255, 255))
        text_input_password = font.render(self.params, True, (100, 200, 105))

        self.screen.blit(self.lobby_image, (0, 0))
        self.screen.blit(self.player_bg, vp(172, 109))

        for i in range(len(self.other_players)):
            player_name = font.render(self.other_players[i].name, True, (255, 255, 255))
            x = get_screen_width() / 2 - vw(33)
            y = vh(107) + i * (self.player_bg_height + self.player_bg_margin)
            self.screen.blit(self.other_player_bg, (x, y))
            self.screen.blit(player_name, (get_screen_width() / 2 + vw(160), y + vh(20)))

        self.gui_manager.draw_ui(self.screen)

        self.screen.blit(text_title, vp(260, 180))
        self.screen.blit(text_my_ip, vp(215, 250))
        self.screen.blit(text_password, vp(250, 360))
        self.screen.blit(text_input_password, vp(230, 430))

