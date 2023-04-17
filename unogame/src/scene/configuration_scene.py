import pygame
import pygame_gui
from pygame_gui.core import ObjectID

from assets import image_keys
from assets.image_loader import ImageLoader
from config import vp, vw, vh, SCREEN_WIDTH, SCREEN_HEIGHT, get_action
from states import ConfigurationState
from utils import action_name
from widgets.overlay import OverlayScene


class ConfigurationOverlayScene(OverlayScene):

    def __init__(self, screen, overlay_manager):
        super().__init__(screen, overlay_manager)
        #self.close_btn_image = ImageLoader.get_image(image_loader, image_keys.IMG_BTN_CLOSE_OVERLAY)
#        self.close_btn_image = pygame.transform.smoothscale(self.close_btn_image, vp(60, 60))
        self.state = ConfigurationState()
        self.panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(vw(149), (SCREEN_HEIGHT - vh(633)) / 2, vw(984), vh(633)),
            manager=self.overlay_manager,
            starting_layer_height=2,
            object_id=ObjectID(object_id="overlay_panel", class_id="@overlay_panels")
        )
#        self.overlay_bg_image = pygame.transform.smoothscale(self.overlay_bg_image, vp(984, 633))
 #       self.panel.drawable_shape.states['normal'].surface.blit(self.overlay_bg_image, (0, 0))
        self.panel.drawable_shape.active_state.has_fresh_surface = True
        self.create_elements()
        self.create_ui_elements()

    def create_elements(self):
        self.close_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((vw(984 - 60 - 55), vh(55)), (vp(60, 60))),
            text='',
            manager=self.overlay_manager,
            container=self.panel,
            object_id=ObjectID(object_id="close_button", class_id="@main_menu_btns")
        )
#        self.close_button.drawable_shape.states['normal'].surface.blit(self.close_btn_image, (0, 0))
        self.close_button.drawable_shape.active_state.has_fresh_surface = True


    def create_ui_elements(self):
        self.color_blind_mode_checkbox = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((350, 200), (150, 40)),
            text="Color Blind Mode",
            container=self.panel,
            manager=self.overlay_manager
        )
        self.back_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((350, 250), (100, 40)),
            text="Back",
            container=self.panel,
            manager=self.overlay_manager
        )

    def process_events(self, event):
        super().process_events(event)
        if event.type == pygame.KEYDOWN:
            key_event = event.key
            action = get_action(key_event)
            if action == action_name.PAUSE:
                self.set_inactive()

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.back_button:
                    self.state.back_to_main_menu()
                if event.ui_element.get_object_ids() == self.close_button.get_object_ids():
                    self.set_inactive()
    def draw(self):
        super().draw()
