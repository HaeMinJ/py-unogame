import pygame
import pygame_gui
from pygame_gui.core import ObjectID

from assets import image_keys
from assets.image_loader import ImageLoader
from config import vp, vw, vh, get_screen_width, get_screen_height, get_action
from states.achievement_state import AchievementState
from utils import action_name
from utils.image_utility import load_image
from widgets.overlay import OverlayScene
from widgets import ScrollableUIButton, FocusableUIButton
from scene import Scene

class AchievementOverlayScene(OverlayScene):

    def __init__(self, screen, overlay_manager):
        super().__init__(screen, overlay_manager)
        print("Achievement Overlay Init!")

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
            relative_rect=pygame.Rect(vw(186), (get_screen_height() - vh(250)) / 2, vw(886), vh(68)),
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
        self.story_check_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(vw(186), (get_screen_height() - vh(100)) / 2, vw(886), vh(155)),
            manager=self.overlay_manager,
            starting_layer_height=2,
            object_id=ObjectID(object_id="overlay_panel", class_id="@overlay_panels")
        )
        self.multi_victory_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(vw(186), (get_screen_height() - vh(100)) / 2, vw(886), vh(155)),
            manager=self.overlay_manager,
            starting_layer_height=2,
            object_id=ObjectID(object_id="overlay_panel", class_id="@overlay_panels")
        )
        # self.btn_date_overlay_panel = pygame_gui.elements.UIPanel(
        #     relative_rect=pygame.Rect(vw(186), (get_screen_height() - vh(100)) / 2, vw(886), vh(155)),
        #     manager=self.overlay_manager,
        #     starting_layer_height=2,
        #     object_id=ObjectID(object_id="overlay_panel", class_id="@overlay_panels")
        # )
        # self.btn_clear_overlay_panel = pygame_gui.elements.UIPanel(
        #     relative_rect=pygame.Rect(vw(186), (get_screen_height() - vh(100)) / 2, vw(886), vh(155)),
        #     manager=self.overlay_manager,
        #     starting_layer_height=2,
        #     object_id=ObjectID(object_id="overlay_panel", class_id="@overlay_panels")
        # )

        self.overlay_bg_image = load_image("achieve_overlay_bg.png")
        self.overlay_bg_image = pygame.transform.smoothscale(self.overlay_bg_image, vp(984, 633))

        self.panel.drawable_shape.states['normal'].surface.blit(self.overlay_bg_image, (0, 0))
        self.panel.drawable_shape.active_state.has_fresh_surface = True

        self.war_victory_bg = load_image("war_victory_bg.png")
        self.war_victory_bg = pygame.transform.smoothscale(self.war_victory_bg, vp(688, 41))
        self.area_victory_bg = load_image("area_victory_bg.png")
        self.area_victory_bg = pygame.transform.smoothscale(self.area_victory_bg, vp(688, 41))
        self.war_victory_panel.drawable_shape.states['normal'].surface.blit(self.war_victory_bg, (0, 0))
        self.area_victory_panel.drawable_shape.states['normal'].surface.blit(self.area_victory_bg, (0, 0))



        # self.turn_victory1 = load_image("turn_victory1.png")
        # self.turn_victory1 = pygame.transform.smoothscale(self.war_victory, vp(688, 41))
        # self.technic_ban = load_image("technic_ban.png")
        # self.technic_ban = pygame.transform.smoothscale(self.technic_ban, vp(688, 41))
        # self.UNO = load_image("UNO.png")
        # self.UNO = pygame.transform.smoothscale(self.UNO, vp(688, 41))
        # self.winning_streak = load_image("winning_streak.png")
        # self.winning_streak = pygame.transform.smoothscale(self.winning_streak, vp(688, 41))
        # self.story_check = load_image("story_check.png")
        # self.story_check = pygame.transform.smoothscale(self.story_check, vp(688, 41))
        # self.multi_victory = load_image("multi_victory.png")
        # self.multi_victory = pygame.transform.smoothscale(self.multi_victory, vp(688, 41))
        #
        #
        # self.panel.drawable_shape.states['normal'].surface.blit(self.overlay_bg_image, (0, 0))
        # self.panel.drawable_shape.active_state.has_fresh_surface = True
        #
        # self.date_achieve_bg = load_image("date_achieve_bg.png")
        # self.clear_achieve_bg = load_image("clear_achieve_bg.png")
        # self.date_achieve_bg = pygame.transform.smoothscale(self.date_achieve_bg, vp(84, 40))
        # self.clear_achieve_bg = pygame.transform.smoothscale(self.clear_achieve_bg, vp(84, 40))




        self.create_elements()
    def create_elements(self):
        self.close_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((vw(984 - 60 - 55), vh(55)), (vp(60, 60))),
            text='',
            manager=self.overlay_manager,
            container=self.panel,
            object_id=ObjectID(object_id="close_button", class_id="@main_menu_btns")
        )

        self.close_button.drawable_shape.states['normal'].surface.blit(self.close_btn_image, (0, 0))

        self.close_button.drawable_shape.active_state.has_fresh_surface = True


def process_events(self, event):
        super().process_events(event)
        if event.type == pygame.KEYDOWN:
            key_event = event.key
            action = get_action(key_event)
            if action == action_name.PAUSE:
                self.set_inactive()