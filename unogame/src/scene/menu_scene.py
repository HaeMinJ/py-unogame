import pygame
import pygame_gui
from pygame_gui.core import ObjectID

from assets import image_keys
from assets.image_loader import ImageLoader
from config import SCREEN_WIDTH, SCREEN_HEIGHT, vw, vh, vp, get_action
from states import MenuState
from utils import action_name
from widgets import ScrollableUIButton, FocusableUIButton
from .scene import Scene
from utils.image_utility import load_image


class MenuScene(Scene):
    def initialize_elements(self):
        self.create_scrollable_buttons()
        self.create_below_buttons()

    def __init__(self, screen, gui_manager, params=None):
        super().__init__(screen, gui_manager, params)

        self.sound_toggle_button = None
        self.state = MenuState()
        self.current_focused_button = -1

        self.main_image = load_image("main_bg.png")
        self.logo_image = load_image("logo.png")
        self.btn_image = load_image("menu_btn.png")
        self.btn_exit = load_image("btn_exit.png")
        self.btn_ranking = load_image("btn_ranking.png")
        self.btn_setting = load_image("btn_setting.png")

        self.scrollable_area_rect = pygame.Rect(vw(0), vh(124), SCREEN_WIDTH, vh(403))
        self.scrollable_button_width = vw(289)
        self.scrollable_button_height = vh(403)
        self.scrollable_button_margin = vw(52)
        self.scrollable_container = pygame_gui.elements.UIScrollingContainer(
            relative_rect=self.scrollable_area_rect,
            manager=self.gui_manager
        )

        self.scroll_buttons_text = ["Single Play", "Configuration", "Exit", "Test2", "Test3"]

        self.scrollable_buttons = []
        self.scroll_offset_x = 0
        self.target_scroll_offset_x = 0
        self.scroll_speed = 0.2

        self.resize_images()
        self.initialize_elements()

    def resize_images(self):
        super().resize_images()
        self.main_image = pygame.transform.scale(self.main_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.logo_image = pygame.transform.smoothscale(self.logo_image, vp(100, 100))
        self.btn_image = pygame.transform.smoothscale(self.btn_image, vp(289, 403))
        self.btn_exit = pygame.transform.smoothscale(self.btn_exit, vp(115, 115))
        self.btn_ranking = pygame.transform.smoothscale(self.btn_ranking, vp(115, 115))
        self.btn_setting = pygame.transform.smoothscale(self.btn_setting, vp(115, 115))

    def create_scrollable_buttons(self):
        for i in range(len(self.scroll_buttons_text)):
            x = i * self.scrollable_button_width + (i + 1) * self.scrollable_button_margin
            y = 0
            button_rect = pygame.Rect(x, y, self.scrollable_button_width, self.scrollable_button_height)
            btn = ScrollableUIButton(
                relative_rect=button_rect,
                text=self.scroll_buttons_text[i],
                manager=self.gui_manager,
                container=self.scrollable_container,
                object_id=ObjectID(object_id=f"button_{i + 1}", class_id="@main_menu_btns")
            )
            btn.drawable_shape.states['normal'].surface.blit(self.btn_image, (0, 0))
            btn.drawable_shape.active_state.has_fresh_surface = True
            self.scrollable_buttons.append(btn)
            self.focusable_buttons.append(btn)

    def create_below_buttons(self):
        btn_setting = FocusableUIButton(
            relative_rect=pygame.Rect(((SCREEN_WIDTH - vw(115)) / 2 - vw(86 + 115), SCREEN_HEIGHT - vh(152)),
                                      vp(115, 115)),
            text="",
            manager=self.gui_manager,
            object_id=ObjectID(object_id=f"button_b_1", class_id="@main_menu_below_btns")
        )
        btn_ranking = FocusableUIButton(
            relative_rect=pygame.Rect(((SCREEN_WIDTH - vw(115)) / 2, SCREEN_HEIGHT - vh(152)), vp(115, 115)),
            text="",
            manager=self.gui_manager,
            object_id=ObjectID(object_id=f"button_b_2", class_id="@main_menu_below_btns")

        )
        btn_exit = FocusableUIButton(
            relative_rect=pygame.Rect(((SCREEN_WIDTH - vw(115)) / 2 + vw(86 + 115), SCREEN_HEIGHT - vh(152)),
                                      vp(115, 115)),
            text="",
            manager=self.gui_manager,
            object_id=ObjectID(object_id=f"button_b_3", class_id="@main_menu_below_btns")
        )
        btn_setting.drawable_shape.states['normal'].surface.blit(self.btn_setting, (0, 0))
        btn_ranking.drawable_shape.states['normal'].surface.blit(self.btn_ranking, (0, 0))
        btn_exit.drawable_shape.states['normal'].surface.blit(self.btn_exit, (0, 0))
        btn_setting.drawable_shape.active_state.has_fresh_surface = True
        btn_ranking.drawable_shape.active_state.has_fresh_surface = True
        btn_exit.drawable_shape.active_state.has_fresh_surface = True
        self.focusable_buttons.extend([btn_setting, btn_ranking, btn_exit])

    def process_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4 or event.button == 1:  # Mouse wheel up
                self.target_scroll_offset_x += vw(60)
            elif event.button == 5 or event.button == 3:  # Mouse wheel down
                self.target_scroll_offset_x -= vw(60)
            self.target_scroll_offset_x = min(self.target_scroll_offset_x, vw(15))
            max_scroll = (len(self.scrollable_buttons) - 3.5) * (
                    self.scrollable_button_width + self.scrollable_button_margin) + self.scrollable_button_margin * 2
            self.target_scroll_offset_x = max(self.target_scroll_offset_x, -max_scroll)
            self.scroll_offset_x += (self.target_scroll_offset_x - self.scroll_offset_x) * self.scroll_speed

            for button in self.scrollable_buttons:
                button.set_position((button.starting_rect.x + self.scroll_offset_x, button.rect.y))

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
                if ui_element == self.scrollable_buttons[0]:
                    self.state.start_single_play()
                elif ui_element == self.scrollable_buttons[1]:
                    self.state.open_configuration()
                elif ui_element == self.scrollable_buttons[2]:
                    self.state.exit()

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                print(event.ui_element)
                if event.ui_element == self.scrollable_buttons[0]:
                    self.state.start_single_play()
                elif event.ui_element == self.scrollable_buttons[1]:
                    self.state.open_configuration()
                elif event.ui_element == self.scrollable_buttons[2]:
                    self.state.exit()

    def draw(self):
        self.screen.blit(self.main_image, (0, 0))
        self.screen.blit(self.logo_image, ((SCREEN_WIDTH - vw(100)) / 2, vh(15)))
        self.gui_manager.draw_ui(self.screen)
