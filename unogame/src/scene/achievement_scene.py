import pygame
import pygame_gui
from pygame_gui.core import ObjectID

from assets import image_keys
from assets.image_loader import ImageLoader
from config import vp, vw, vh, get_screen_width, get_screen_height, get_action
from states import AchievementState
from utils import action_name
from utils.image_utility import load_image
from widgets.overlay import OverlayScene
from widgets import ScrollableUIButton, FocusableUIButton
from scene import Scene

class AchievementOverlayScene(OverlayScene):

    def __init__(self, screen, overlay_manager):
        super().__init__(screen, overlay_manager)

        self.tab_button_clicked = False

        self.close_btn_image = load_image("btn_close_overlay.png")
        self.close_btn_image = pygame.transform.smoothscale(self.close_btn_image, vp(60, 60))
        self.state = AchievementState()
        self.panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(vw(149), (get_screen_height() - vh(633)) / 2, vw(984), vh(633)),
            manager=self.overlay_manager,
            starting_layer_height=2,
            object_id=ObjectID(object_id="overlay_panel", class_id="@overlay_panels")
        )
        self.war_victory_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(vw(186), (get_screen_height() - vh(100)) / 2, vw(886), vh(155)),
            manager=self.overlay_manager,
            starting_layer_height=2,
            object_id=ObjectID(object_id="overlay_panel", class_id="@overlay_panels")
        )
        self.area_victory_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(vw(186), (get_screen_height() - vh(100)) / 2, vw(886), vh(155)),
            manager=self.overlay_manager,
            starting_layer_height=2,
            object_id=ObjectID(object_id="overlay_panel", class_id="@overlay_panels")
        )
        self.turn_victory1_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(vw(186), (get_screen_height() - vh(100)) / 2, vw(886), vh(155)),
            manager=self.overlay_manager,
            starting_layer_height=2,
            object_id=ObjectID(object_id="overlay_panel", class_id="@overlay_panels")
        )
        self.technic_ban_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(vw(186), (get_screen_height() - vh(100)) / 2, vw(886), vh(155)),
            manager=self.overlay_manager,
            starting_layer_height=2,
            object_id=ObjectID(object_id="overlay_panel", class_id="@overlay_panels")
        )
        self.UNO_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(vw(186), (get_screen_height() - vh(100)) / 2, vw(886), vh(155)),
            manager=self.overlay_manager,
            starting_layer_height=2,
            object_id=ObjectID(object_id="overlay_panel", class_id="@overlay_panels")
        )
        self.winning_streak_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(vw(186), (get_screen_height() - vh(100)) / 2, vw(886), vh(155)),
            manager=self.overlay_manager,
            starting_layer_height=2,
            object_id=ObjectID(object_id="overlay_panel", class_id="@overlay_panels")
        )
        self.UNO_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(vw(186), (get_screen_height() - vh(100)) / 2, vw(886), vh(155)),
            manager=self.overlay_manager,
            starting_layer_height=2,
            object_id=ObjectID(object_id="overlay_panel", class_id="@overlay_panels")
        )
        self.story_check_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(vw(186), (get_screen_height() - vh(100)) / 2, vw(886), vh(155)),
            manager=self.overlay_manager,
            starting_layer_height=2,
            object_id=ObjectID(object_id="overlay_panel", class_id="@overlay_panels")
        )
        self.turn_victory2_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(vw(186), (get_screen_height() - vh(100)) / 2, vw(886), vh(155)),
            manager=self.overlay_manager,
            starting_layer_height=2,
            object_id=ObjectID(object_id="overlay_panel", class_id="@overlay_panels")
        )
        self.date_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(vw(186), (get_screen_height() - vh(100)) / 2, vw(886), vh(155)),
            manager=self.overlay_manager,
            starting_layer_height=2,
            object_id=ObjectID(object_id="overlay_panel", class_id="@overlay_panels")
        )
        self.clear_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(vw(186), (get_screen_height() - vh(100)) / 2, vw(886), vh(155)),
            manager=self.overlay_manager,
            starting_layer_height=2,
            object_id=ObjectID(object_id="overlay_panel", class_id="@overlay_panels")
        )

        self.overlay_bg_image = load_image("config_overlay_bg.png")
        self.overlay_bg_image = pygame.transform.smoothscale(self.overlay_bg_image, vp(984, 633))

        self.date_btn_image = load_image("btn_date_overlay.png")
        self.date_btn_image = pygame.transform.smoothscale(self.date_btn, vp(210, 60))

        self.clear_btn_image = load_image("btn_clear_overlay.png")
        self.clear_btn_image = pygame.transform.smoothscale(self.clear_btn, vp(210, 60))
