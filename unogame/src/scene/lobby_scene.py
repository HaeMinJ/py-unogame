import pygame
import pygame_gui
from pygame_gui.core import ObjectID

from config.configuration import SCREEN_WIDTH, SCREEN_HEIGHT, vw, vh, vp, KEYBOARD_MAP

from scene import Scene
from states.lobby_state import LobbyState
from utils import action_name, overlay_name
from widgets import FocusableUIButton
from classes.auth.user import User



class LobbyScene(Scene):
    def initialize_elements(self):
        self.create_below_buttons()
        self.create_set_player_buttons()

    def __init__(self, screen, gui_manager):
        super().__init__(screen, gui_manager)
        self.state = LobbyState()

        self.lobby_image = pygame.image.load("assets/lobby_img/lobby_bg.png")
        self.btn_left = pygame.image.load("assets/lobby_img/btn_left.png")
        self.btn_right = pygame.image.load("assets/lobby_img/btn_right.png")
        self.player_bg = pygame.image.load("assets/lobby_img/player_bg.png")
        self.other_player_bg = pygame.image.load("assets/lobby_img/other_player_bg.png")
        self.btn_set_player = pygame.image.load("assets/lobby_img/btn_set_player.png")

        self.player_bg_width = vw(512)
        self.player_bg_height = vh(90)
        self.player_bg_margin = vh(13)

        self.players = [User(0, "player1")]
        self.set_player_buttons =[]

        self.resize_images()
        self.initialize_elements()

    def resize_images(self):
        super().resize_images()
        self.lobby_image = pygame.transform.scale(self.lobby_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.btn_left = pygame.transform.scale(self.btn_left, vp(64.95, 57))
        self.btn_right = pygame.transform.scale(self.btn_right, vp(64.95, 57))
        self.player_bg = pygame.transform.scale(self.player_bg, vp(338, 400))
        self.other_player_bg = pygame.transform.scale(self.other_player_bg, vp(512, 90))
        self.btn_set_player = pygame.transform.scale(self.btn_set_player, vp(160, 83))

    def create_below_buttons(self):
        btn_left = FocusableUIButton(
            relative_rect=pygame.Rect((vw(50), SCREEN_HEIGHT - 100), vp(64.95, 57)),
            text="",
            manager=self.gui_manager,
            object_id=ObjectID(object_id=f"button_b_1", class_id="@lobby_below_btns")
        )
        btn_right = FocusableUIButton(
            relative_rect=pygame.Rect((SCREEN_WIDTH-100, SCREEN_HEIGHT - 100), vp(64.95, 57)),
            text="",
            manager=self.gui_manager,
            object_id=ObjectID(object_id=f"button_b_2", class_id="@lobby_below_btns")

        )
        btn_left.drawable_shape.states['normal'].surface.blit(self.btn_left, (0, 0))
        btn_right.drawable_shape.states['normal'].surface.blit(self.btn_right, (0, 0))
        btn_left.drawable_shape.active_state.has_fresh_surface = True
        btn_right.drawable_shape.active_state.has_fresh_surface = True
        self.focusable_buttons.extend([btn_left, btn_right])

    def create_set_player_buttons(self):
        btn_add_player = FocusableUIButton(
            relative_rect=pygame.Rect((vw(172), SCREEN_HEIGHT - 200), vp(160, 83)),
            text="",
            manager=self.gui_manager,
            object_id=ObjectID(object_id=f"button_b_1", class_id="@lobby_add_btns")
        )
        btn_remove_player = FocusableUIButton(
            relative_rect=pygame.Rect((vw(350), SCREEN_HEIGHT - 200), vp(160, 83)),
            text="",
            manager=self.gui_manager,
            object_id=ObjectID(object_id=f"button_b_1", class_id="@lobby_remove_btns")
        )
        btn_add_player.drawable_shape.states['normal'].surface.blit(self.btn_set_player, (0, 0))
        btn_remove_player.drawable_shape.states['normal'].surface.blit(self.btn_set_player, (0, 0))
        btn_add_player.drawable_shape.active_state.has_fresh_surface = True
        btn_remove_player.drawable_shape.active_state.has_fresh_surface = True
        self.focusable_buttons.extend([btn_add_player, btn_remove_player])
        self.set_player_buttons.extend([btn_add_player, btn_remove_player])

    def process_events(self, event):
        if event.type == pygame.KEYDOWN:
            key_event = event.key
            action = get_action(key_event)
            if action == action_name.RETURN:
                self.state.start_single_play()
            if action == action_name.PAUSE:
                self.state.active_overlay(overlay_name.CONFIGURATION)
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.set_player_buttons[0]:
                    if len(self.players) < 5:
                        self.players.append(User(len(self.players), f"플레이어{len(self.players)}"))
                if event.ui_element == self.set_player_buttons[1]:
                    if len(self.players) > 1:
                        self.players.pop()

    def draw(self):
        font = pygame.font.SysFont('arial', 40)
        add_player_text = font.render('add', True, (0, 0, 0))  # 텍스트, 안티앨리어싱 여부, 텍스트 색상
        remove_player_text = font.render("remove", True, (0, 0, 0))

        self.screen.blit(self.lobby_image, (0, 0))
        self.screen.blit(self.player_bg, vp(172, 109))

        for i in range(len(self.players)):
            x = SCREEN_WIDTH / 2 - vw(33)
            y = 107 + i * (self.player_bg_height + self.player_bg_margin)
            self.screen.blit(self.other_player_bg, vp(x, y))

        self.gui_manager.draw_ui(self.screen)
        self.screen.blit(add_player_text, (vw(172 + 43), SCREEN_HEIGHT - 200 + 18))
        self.screen.blit(remove_player_text, (vw(350 + 15), SCREEN_HEIGHT - 200 + 18))
