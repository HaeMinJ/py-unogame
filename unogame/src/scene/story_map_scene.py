import pygame
import pygame_gui
from pygame_gui.core import ObjectID
from config.configuration import SCREEN_WIDTH, SCREEN_HEIGHT, vw, vh, vp, KEYBOARD_MAP

from scene import Scene
from states.story_map_state import StoryMapState
from utils import action_name, overlay_name
from widgets import FocusableUIButton
from utils.image_utility import load_image
from classes.auth.user import User
class StoryMapScene(Scene):
    def initialize_elements(self):
        self.create_stage_buttons()

    def __init__(self, screen, gui_manager, params=None):
        super().__init__(screen, gui_manager)
        self.state = StoryMapState()

        self.story_map_bg = load_image("story_map_img/story_map_bg.png")
        self.stage_1 = load_image("story_map_img/stage_1.png")
        self.stage_2 = load_image("story_map_img/stage_2.png")
        self.stage_3 = load_image("story_map_img/stage_3.png")
        self.stage_4 = load_image("story_map_img/stage_4.png")
        self.stage_1_bg = load_image("story_map_img/stage_1_bg.png")
        self.stage_2_bg = load_image("story_map_img/stage_2_bg.png")
        self.stage_3_bg = load_image("story_map_img/stage_3_bg.png")
        self.stage_4_bg = load_image("story_map_img/stage_4_bg.png")
        self.lock = load_image("story_map_img/lock.png")

        self.current_stage = 0
        self.stage_buttons =[]

        self.resize_images()
        self.initialize_elements()

    def resize_images(self):
        super().resize_images()
        self.story_map_bg = pygame.transform.scale(self.story_map_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.stage_1 = pygame.transform.scale(self.stage_1, vp(340, 346))
        self.stage_2 = pygame.transform.scale(self.stage_2, vp(340, 346))
        self.stage_3 = pygame.transform.scale(self.stage_3, vp(340, 346))
        self.stage_4 = pygame.transform.scale(self.stage_4, vp(340, 346))
        self.stage_1_bg = pygame.transform.scale(self.stage_1_bg, vp(262, 309))
        self.stage_2_bg = pygame.transform.scale(self.stage_2_bg, vp(217, 239))
        self.stage_3_bg = pygame.transform.scale(self.stage_3_bg, vp(245, 156))
        self.stage_4_bg = pygame.transform.scale(self.stage_4_bg, vp(306, 437))
        self.lock = pygame.transform.scale(self.lock, vp(345, 345))

    def create_stage_buttons(self):
        btn_stage_1 = FocusableUIButton(
            relative_rect=pygame.Rect((vw(0), vh(51)), vp(262, 309)),
            text="stage1",
            manager=self.gui_manager,
            object_id=ObjectID(object_id=f"button_b_1", class_id="@stage_btn")
        )
        btn_stage_2 = FocusableUIButton(
            relative_rect=pygame.Rect((vw(256), SCREEN_HEIGHT - 380), vp(217, 239)),
            text="stage2",
            manager=self.gui_manager,
            object_id=ObjectID(object_id=f"button_b_1", class_id="@stage_btn")
        )
        btn_stage_3 = FocusableUIButton(
            relative_rect=pygame.Rect((vw(635), SCREEN_HEIGHT - 175), vp(245, 156)),
            text="stage3",
            manager=self.gui_manager,
            object_id=ObjectID(object_id=f"button_b_1", class_id="@stage_btn")
        )
        btn_stage_4 = FocusableUIButton(
            relative_rect=pygame.Rect((vw(939), SCREEN_HEIGHT - 557), vp(306, 437)),
            text="stage4",
            manager=self.gui_manager,
            object_id=ObjectID(object_id=f"button_b_1", class_id="@stage_btn")
        )
        btn_stage_1.drawable_shape.states['normal'].surface.blit(self.stage_1_bg, (0, 0))
        btn_stage_2.drawable_shape.states['normal'].surface.blit(self.stage_2_bg, (0, 0))
        btn_stage_3.drawable_shape.states['normal'].surface.blit(self.stage_3_bg, (0, 0))
        btn_stage_4.drawable_shape.states['normal'].surface.blit(self.stage_4_bg, (0, 0))

        btn_stage_1.drawable_shape.active_state.has_fresh_surface = True
        btn_stage_2.drawable_shape.active_state.has_fresh_surface = True
        btn_stage_3.drawable_shape.active_state.has_fresh_surface = True
        btn_stage_4.drawable_shape.active_state.has_fresh_surface = True

        self.focusable_buttons.extend([btn_stage_1, btn_stage_2, btn_stage_3, btn_stage_4])
        self.stage_buttons.extend([btn_stage_1, btn_stage_2, btn_stage_3, btn_stage_4])

    def process_events(self, event):
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.stage_buttons[0]:
                    self.screen.blit(self.stage_1, (vw(268), vh(51)))
                    pygame.display.flip()
                    pygame.time.delay(3000)
                if event.ui_element == self.stage_buttons[1]:
                    if self.current_stage >= 1:
                        self.screen.blit(self.stage_2, (vw(331), vh(224)))
                        pygame.display.flip()
                        pygame.time.delay(3000)
                if event.ui_element == self.stage_buttons[2]:
                    if self.current_stage >= 2:
                        self.screen.blit(self.stage_3, (vw(542), vh(301)))
                        pygame.display.flip()
                        pygame.time.delay(3000)
                if event.ui_element == self.stage_buttons[3]:
                    if self.current_stage >= 3:
                        self.screen.blit(self.stage_4, (vw(853), vh(80)))
                        pygame.display.flip()
                        pygame.time.delay(3000)

    def draw(self):
        self.screen.blit(self.story_map_bg, vp(0, 0))
        self.gui_manager.draw_ui(self.screen)

        for i in range(len(self.stage_buttons)):
            if i > self.current_stage:
                self.screen.blit(self.lock, vp(self.stage_buttons[i].rect.x - vw(50), self.stage_buttons[i].rect.y - vh(80)))







