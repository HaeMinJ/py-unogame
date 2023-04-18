import pygame
import pygame_gui
from pygame_gui.core import ObjectID

from config.configuration import get_screen_width, get_screen_height, vw, vh, vp, KEYBOARD_MAP, get_action

from scene import Scene
from states import LobbyState
from utils import action_name, overlay_name, scene_name
from utils.image_utility import load_image
from widgets import FocusableUIButton
from classes.auth.user import User


class LobbyScene(Scene):
    def initialize_elements(self):
        self.create_below_buttons()
        self.create_set_player_buttons()

    def __init__(self, screen, gui_manager, params=None):
        super().__init__(screen, gui_manager, params)
        self.state = LobbyState()
        self.current_focused_button = -1


        self.lobby_image = load_image("lobby_img/lobby_bg.png")
        self.btn_left = load_image("lobby_img/btn_left.png")
        self.btn_right = load_image("lobby_img/btn_right.png")
        self.player_bg = load_image("lobby_img/player_bg.png")
        self.other_player_bg = load_image("lobby_img/other_player_bg.png")
        self.btn_set_player = load_image("lobby_img/btn_set_player.png")
        self.player_profile = load_image("lobby_img/player_profile.png")

        self.player_bg_width = vw(512)
        self.player_bg_height = vh(90)
        self.player_bg_margin = vh(13)

        self.players = [User(1, "player1")]
        self.set_player_buttons = []
        self.move_scene_buttons = []

        self.resize_images()
        self.initialize_elements()

        self.text_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(vp(223, 171), vp(235, 52)),
            manager=self.gui_manager,
        )
        self.player_name = ""

    def resize_images(self):
        super().resize_images()
        self.lobby_image = pygame.transform.scale(self.lobby_image, (get_screen_width(), get_screen_height()))
        self.btn_left = pygame.transform.scale(self.btn_left, vp(64.95, 57))
        self.btn_right = pygame.transform.scale(self.btn_right, vp(64.95, 57))
        self.player_bg = pygame.transform.scale(self.player_bg, vp(338, 400))
        self.other_player_bg = pygame.transform.scale(self.other_player_bg, vp(512, 90))
        self.btn_set_player = pygame.transform.scale(self.btn_set_player, vp(160, 83))
        self.player_profile = pygame.transform.scale(self.player_profile, vp(70, 66))

    def create_below_buttons(self):
        btn_left = FocusableUIButton(
            relative_rect=pygame.Rect((vw(50), get_screen_height() - 100), vp(64.95, 57)),
            text="",
            manager=self.gui_manager,
            object_id=ObjectID(object_id=f"button_b_1", class_id="@lobby_below_btns")
        )
        btn_right = FocusableUIButton(
            relative_rect=pygame.Rect((get_screen_width() - 100, get_screen_height() - 100), vp(64.95, 57)),
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

    def create_set_player_buttons(self):
        btn_add_player = FocusableUIButton(
            relative_rect=pygame.Rect((vw(172), get_screen_height() - 200), vp(160, 83)),
            text="",
            manager=self.gui_manager,
            object_id=ObjectID(object_id=f"button_b_1", class_id="@lobby_add_btns")
        )
        btn_remove_player = FocusableUIButton(
            relative_rect=pygame.Rect((vw(350), get_screen_height() - 200), vp(160, 83)),
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

        if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
            if event.ui_element == self.text_input:
                self.player_name = self.text_input.get_text()
        if event.type == pygame.KEYDOWN:
            key_event = event.key
            action = get_action(key_event)
            if action == action_name.MOVE_UP or action == action_name.MOVE_LEFT:
                self.current_focused_button = (self.current_focused_button - 1) % len(self.focusable_buttons)
                self.gui_manager.set_focus_set(self.focusable_buttons[self.current_focused_button])
                print(self.gui_manager.get_focus_set(), self.current_focused_button)

            if action == action_name.MOVE_DOWN or action == action_name.MOVE_RIGHT:
                self.current_focused_button = (self.current_focused_button + 1) % len(self.focusable_buttons)
                self.gui_manager.set_focus_set(self.focusable_buttons[self.current_focused_button])
                print(self.gui_manager.get_focus_set(), self.current_focused_button)
                # todo: 버튼 포커싱에 맞게 움직이도록 하기.
            if action == action_name.PAUSE:
                self.state.toggle_configuration()
            if action == action_name.RETURN:
                ui_element = self.focusable_buttons[self.current_focused_button]
                if ui_element == self.set_player_buttons[0]:
                    if len(self.players) < 5:
                        self.players.append(User(len(self.players) + 1, f"player{len(self.players) + 1}", is_ai=True))
                elif ui_element == self.set_player_buttons[1]:
                    if len(self.players) > 1:
                        self.players.pop()
                elif ui_element == self.move_scene_buttons[0]:
                    self.state.move_scene(scene_name.MAIN_MENU)
                elif ui_element == self.move_scene_buttons[1]:
                    self.player_name = self.text_input.get_text()
                    self.players.insert(0, User(0, self.player_name, is_ai=False))
                    self.state.start_single_play(players=self.players)

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.set_player_buttons[0]:
                    if len(self.players) < 5:
                        self.players.append(User(len(self.players) + 1, f"player{len(self.players) + 1}", is_ai=True))
                if event.ui_element == self.set_player_buttons[1]:
                    if len(self.players) > 1:
                        self.players.pop()
                if event.ui_element == self.move_scene_buttons[1]:
                    self.player_name = self.text_input.get_text()
                    self.players.insert(0, User(0, self.player_name, is_ai=False))
                    self.state.start_single_play(players=self.players)
                if event.ui_element == self.move_scene_buttons[0]:
                    self.state.move_scene(scene_name.MAIN_MENU)

    def draw(self):
        font = pygame.font.SysFont('arial', 40)
        add_player_text = font.render('add', True, (0, 0, 0))  # 텍스트, 안티앨리어싱 여부, 텍스트 색상
        remove_player_text = font.render("remove", True, (0, 0, 0))

        self.screen.blit(self.lobby_image, (0, 0))
        self.screen.blit(self.player_bg, vp(172, 109))

        for i in range(len(self.players)):
            player_name = font.render(self.players[i].name, True, (255, 255, 255))
            x = get_screen_width() / 2 - vw(33)
            y = vh(107) + i * (self.player_bg_height + self.player_bg_margin)
            self.screen.blit(self.other_player_bg, vp(x, y))
            self.screen.blit(self.player_profile, vp((get_screen_width() / 2 + vw(82)),
                                                     vh(118) + i * (self.player_bg_height + self.player_bg_margin)))
            self.screen.blit(player_name, vp(vw(get_screen_width() / 2 + vw(180)), vh(y + vh(20))))

        self.gui_manager.draw_ui(self.screen)
        self.screen.blit(add_player_text, vp(vw(172 + 43), get_screen_height() - 200 + 18))
        self.screen.blit(remove_player_text, vp(vw(350 + 15), get_screen_height() - 200 + 18))
