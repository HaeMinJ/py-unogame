import pygame
import pygame_gui
from pygame_gui.core import ObjectID

from assets import image_keys
from assets.image_loader import ImageLoader
from config import vp, vw, vh, get_screen_width, get_screen_height, get_action
from states import ConfigurationState
from utils import action_name
from utils.image_utility import load_image
from widgets.overlay import OverlayScene
from scene import Scene


class ConfigurationOverlayScene(OverlayScene):

    def __init__(self, screen, overlay_manager):
        super().__init__(screen, overlay_manager)

        self.close_btn_image = load_image("btn_close_overlay.png")
        self.close_btn_image = pygame.transform.smoothscale(self.close_btn_image, vp(60, 60))
        self.state = ConfigurationState()
        self.panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(vw(149), (get_screen_height() - vh(633)) / 2, vw(984), vh(633)),
            manager=self.overlay_manager,
            starting_layer_height=2,
            object_id=ObjectID(object_id="overlay_panel", class_id="@overlay_panels")
        )
        self.large_config_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(vw(186), (get_screen_height() - vh(100)) / 2, vw(886), vh(155)),
            manager=self.overlay_manager,
            starting_layer_height=2,
            object_id=ObjectID(object_id="overlay_panel", class_id="@overlay_panels")
        )
        self.small_config_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(vw(186), (get_screen_height() - vh(250)) / 2, vw(886), vh(60)),
            manager=self.overlay_manager,
            starting_layer_height=2,
            object_id=ObjectID(object_id="overlay_panel", class_id="@overlay_panels")
        )
        self.overlay_bg_image = load_image("config_overlay_bg.png")
        self.overlay_bg_image = pygame.transform.smoothscale(self.overlay_bg_image, vp(984, 633))

        self.initialize_settings_btn = load_image("btn_initialize_settings_overlay.png")
        self.initialize_settings_btn = pygame.transform.smoothscale(self.initialize_settings_btn, vp(210, 60))
        self.apply_btn = load_image("btn_apply_overlay.png")
        self.apply_btn = pygame.transform.smoothscale(self.apply_btn, vp(138, 60))

        self.small_config_bg = load_image("small_config_bg.png")
        self.small_config_bg = pygame.transform.smoothscale(self.small_config_bg, vp(886, 60))

        self.large_config_bg = load_image("large_config_bg.png")
        self.large_config_bg = pygame.transform.smoothscale(self.large_config_bg, vp(886, 155))

        self.blind_buttons = []
        self.size_buttons = []
        self.current_width = 1280
        self.current_height = 720
        self.current_blind = "normal_vision"

        self.panel.drawable_shape.states['normal'].surface.blit(self.overlay_bg_image, (0, 0))
        self.panel.drawable_shape.active_state.has_fresh_surface = True
        self.large_config_panel.drawable_shape.states['normal'].surface.blit(self.large_config_bg, (0, 0))
        self.large_config_panel.drawable_shape.active_state.has_fresh_surface = True
        self.small_config_panel.drawable_shape.states['normal'].surface.blit(self.small_config_bg, (0, 0))
        self.small_config_panel.drawable_shape.active_state.has_fresh_surface = True
        self.create_elements()
        self.create_blind_buttons()
        self.create_size_buttons()

    def create_elements(self):
        self.close_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((vw(984 - 60 - 55), vh(55)), (vp(60, 60))),
            text='',
            manager=self.overlay_manager,
            container=self.panel,
            object_id=ObjectID(object_id="close_button", class_id="@main_menu_btns")
        )
        self.initialize_settings_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((vw(32), vh(515)), (vp(210, 60))),
            text='',
            manager=self.overlay_manager,
            container=self.panel,
            object_id=ObjectID(object_id="close_button", class_id="@main_menu_btns")
        )
        # self.apply_button = pygame_gui.elements.UIButton(
        #     relative_rect=pygame.Rect((vw(788), vh(515)), (vp(138, 60))),
        #     text='',
        #     manager=self.overlay_manager,
        #     container=self.panel,
        #     object_id=ObjectID(object_id="close_button", class_id="@main_menu_btns")
        # )
        self.close_button.drawable_shape.states['normal'].surface.blit(self.close_btn_image, (0, 0))
        self.initialize_settings_button.drawable_shape.states['normal'].surface.blit(self.initialize_settings_btn, (0, 0))
        # self.apply_button.drawable_shape.states['normal'].surface.blit(self.apply_btn, (0, 0))

        self.close_button.drawable_shape.active_state.has_fresh_surface = True
        self.initialize_settings_button.drawable_shape.active_state.has_fresh_surface = True
        # self.apply_button.drawable_shape.active_state.has_fresh_surface = True

    def create_size_buttons(self):
        self.small_size = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(vp(750, 200), vp(115, 26)),
            text="640 X 360",
            container=self.panel,
            manager=self.overlay_manager
        )
        self.medium_size = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(vp(555, 200), vp(114, 28)),
            text="960 X 540",
            container=self.panel,
            manager=self.overlay_manager
        )
        self.large_size = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(vp(360, 200), vp(123, 28)),
            text="1280 X 720",
            container=self.panel,
            manager=self.overlay_manager
        )
        self.size_buttons.extend([self.small_size, self.medium_size, self.large_size])
    def create_blind_buttons(self):
        self.blind_mode_normal_vision = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(vp(356, 286), vp(163, 26)),
            text="default",
            container=self.panel,
            manager=self.overlay_manager
        )
        self.blind_mode_protanopia = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(vp(364, 339), vp(118, 28)),
            text="Protanopia",
            container=self.panel,
            manager=self.overlay_manager
        )
        self.blind_mode_tritanopia = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(vp(552, 339), vp(109, 28)),
            text="Tritanopia",
            container=self.panel,
            manager=self.overlay_manager
        )
        self.blind_mode_deuteranopia = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(vp(734, 339), vp(147, 28)),
            text="Deuteranopia",
            container=self.panel,
            manager=self.overlay_manager
        )
        self.blind_buttons.extend([self.blind_mode_normal_vision,self.blind_mode_protanopia,self.blind_mode_tritanopia,self.blind_mode_deuteranopia])

    def process_events(self, event):
        super().process_events(event)
        if event.type == pygame.KEYDOWN:
            key_event = event.key
            action = get_action(key_event)
            if action == action_name.PAUSE:
                self.set_inactive()


        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                for i in range(len(self.blind_buttons)):
                    if event.ui_element == self.blind_buttons[i]:
                        self.current_blind = self.blind_buttons[i].text
                        self.state.set_color_blind(self.current_blind)
                        self.set_inactive()
                for i in range(len(self.size_buttons)):
                    if event.ui_element == self.size_buttons[i]:
                        self.current_width = 640 + i * 320
                        self.current_height = 360 + i * 180
                        self.state.set_screen_size(self.current_width, self.current_height)
                        self.set_inactive()

                # if event.ui_element == self.apply_button:
                #     self.state.set_color_blind(self.current_blind)
                #     self.state.set_screen_size(self.current_width, self.current_height)
                #     self.set_inactive()
                if event.ui_element == self.initialize_settings_button:
                    self.current_width = 1280
                    self.current_height = 720
                    self.current_blind = "default"
                    self.state.set_screen_size(self.current_width, self.current_height)
                    self.state.set_color_blind(self.current_blind)
                    self.set_inactive()


    def draw(self):
        super().draw()

