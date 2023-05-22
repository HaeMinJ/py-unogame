import pygame
import pygame_gui
from pygame_gui.core import ObjectID
from config.configuration import get_screen_width, get_screen_height, vw, vh, vp, KEYBOARD_MAP, get_action

from scene import Scene
from states.story_map_state import StoryMapState
from utils import action_name, overlay_name, scene_name
from widgets import FocusableUIButton
from utils.image_utility import load_image
from classes.auth.user import User

class StoryMapScene(Scene):
    def initialize_elements(self):
        self.create_stage_buttons()
        self.create_play_btn()

    def __init__(self, screen, gui_manager, params=None):
        super().__init__(screen, gui_manager)
        self.state = StoryMapState()
        self.current_focused_button = -1

        # 스토리 지역 클릭시 렌더링 되는 판넬 생성
        self.stage_1_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(vw(268), vh(51), vw(340), vh(346)),
            manager=self.gui_manager,
            starting_layer_height=2,
            object_id=ObjectID(object_id="overlay_panel", class_id="@overlay_panels")
        )
        self.stage_2_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(vw(331), vh(224), vw(340), vh(346)),
            manager=self.gui_manager,
            starting_layer_height=2,
            object_id=ObjectID(object_id="overlay_panel", class_id="@overlay_panels")
        )
        self.stage_3_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(vw(542), vh(301), vw(340), vh(346)),
            manager=self.gui_manager,
            starting_layer_height=2,
            object_id=ObjectID(object_id="overlay_panel", class_id="@overlay_panels")
        )
        self.stage_4_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(vw(853), vh(80), vw(340), vh(346)),
            manager=self.gui_manager,
            starting_layer_height=2,
            object_id=ObjectID(object_id="overlay_panel", class_id="@overlay_panels")
        )

        self.stage_1_panel_bg = load_image("story_map_img/stage_1.png")
        self.stage_1_panel.drawable_shape.states['normal'].surface.blit(self.stage_1_panel_bg, (0, 0))
        self.stage_1_panel.drawable_shape.active_state.has_fresh_surface = True
        self.stage_2_panel_bg = load_image("story_map_img/stage_2.png")
        self.stage_2_panel.drawable_shape.states['normal'].surface.blit(self.stage_2_panel_bg, (0, 0))
        self.stage_2_panel.drawable_shape.active_state.has_fresh_surface = True
        self.stage_3_panel_bg = load_image("story_map_img/stage_3.png")
        self.stage_3_panel.drawable_shape.states['normal'].surface.blit(self.stage_3_panel_bg, (0, 0))
        self.stage_3_panel.drawable_shape.active_state.has_fresh_surface = True
        self.stage_4_panel_bg = load_image("story_map_img/stage_4.png")
        self.stage_4_panel.drawable_shape.states['normal'].surface.blit(self.stage_4_panel_bg, (0, 0))
        self.stage_4_panel.drawable_shape.active_state.has_fresh_surface = True

        self.stage_1_panel.visible = False
        self.stage_2_panel.visible = False
        self.stage_3_panel.visible = False
        self.stage_4_panel.visible = False

        self.story_map_bg = load_image("story_map_img/story_map_bg.png")

        self.stage_1_bg = load_image("story_map_img/stage_1_bg.png")
        self.stage_2_bg = load_image("story_map_img/stage_2_bg.png")
        self.stage_3_bg = load_image("story_map_img/stage_3_bg.png")
        self.stage_4_bg = load_image("story_map_img/stage_4_bg.png")
        self.lock = load_image("story_map_img/lock.png")
        self.btn_start_game = load_image("story_map_img/btn_start_game.png")

        from config import configuration
        self.current_stage = configuration.CURRENT_STAGE
        self.stage_buttons =[]
        self.play_buttons =[]

        self.resize_images()
        self.initialize_elements()

    def resize_images(self):
        super().resize_images()
        self.story_map_bg = pygame.transform.scale(self.story_map_bg, (get_screen_width(), get_screen_height()))
        self.stage_1_bg = pygame.transform.scale(self.stage_1_bg, vp(262, 309))
        self.stage_2_bg = pygame.transform.scale(self.stage_2_bg, vp(217, 239))
        self.stage_3_bg = pygame.transform.scale(self.stage_3_bg, vp(245, 156))
        self.stage_4_bg = pygame.transform.scale(self.stage_4_bg, vp(306, 437))
        self.lock = pygame.transform.scale(self.lock, vp(345, 345))
        self.btn_start_game = pygame.transform.scale(self.btn_start_game, vp(134, 42))

    def create_stage_buttons(self):
        btn_stage_1 = FocusableUIButton(
            relative_rect=pygame.Rect(vw(0), vh(51), vw(262), vh(309)),
            text="stage1",
            manager=self.gui_manager,
            object_id=ObjectID(object_id=f"button_b_1", class_id="@stage_btn")
        )
        btn_stage_2 = FocusableUIButton(
            relative_rect=pygame.Rect(vw(256), get_screen_height() - vh(380), vw(217), vh(239)),
            text="stage2",
            manager=self.gui_manager,
            object_id=ObjectID(object_id=f"button_b_2", class_id="@stage_btn")
        )
        btn_stage_3 = FocusableUIButton(
            relative_rect=pygame.Rect(vw(635), get_screen_height() - vh(175), vw(245), vh(156)),
            text="stage3",
            manager=self.gui_manager,
            object_id=ObjectID(object_id=f"button_b_3", class_id="@stage_btn")
        )
        btn_stage_4 = FocusableUIButton(
            relative_rect=pygame.Rect(vw(939), get_screen_height() - vh(557), vw(306), vh(437)),
            text="stage4",
            manager=self.gui_manager,
            object_id=ObjectID(object_id=f"button_b_4", class_id="@stage_btn")
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

    def create_play_btn(self):
        btn_start_game_1 = FocusableUIButton(
            relative_rect=pygame.Rect(vp(388, 311), vp(134, 42)),
            text="start",
            manager=self.gui_manager,
            starting_height=3,
            object_id=ObjectID(object_id=f"button_b_1", class_id="@start_btn")
        )
        btn_start_game_2 = FocusableUIButton(
            relative_rect=pygame.Rect(vp(440, 500), vp(134, 42)),
            text="start",
            manager=self.gui_manager,
            starting_height=3,
            object_id=ObjectID(object_id=f"button_b_2", class_id="@start_btn")
        )
        btn_start_game_3 = FocusableUIButton(
            relative_rect=pygame.Rect(vp(660, 580), vp(134, 42)),
            text="start",
            manager=self.gui_manager,
            starting_height=3,
            object_id=ObjectID(object_id=f"button_b_3", class_id="@start_btn")
        )
        btn_start_game_4 = FocusableUIButton(
            relative_rect=pygame.Rect(vp(970, 350), vp(134, 42)),
            text="start",
            manager=self.gui_manager,
            starting_height=3,
            object_id=ObjectID(object_id=f"button_b_4", class_id="@start_btn")
        )
        btn_start_game_1.drawable_shape.states['normal'].surface.blit(self.btn_start_game, (0, 0))
        btn_start_game_1.drawable_shape.active_state.has_fresh_surface = True
        btn_start_game_2.drawable_shape.states['normal'].surface.blit(self.btn_start_game, (0, 0))
        btn_start_game_2.drawable_shape.active_state.has_fresh_surface = True
        btn_start_game_3.drawable_shape.states['normal'].surface.blit(self.btn_start_game, (0, 0))
        btn_start_game_3.drawable_shape.active_state.has_fresh_surface = True
        btn_start_game_4.drawable_shape.states['normal'].surface.blit(self.btn_start_game, (0, 0))
        btn_start_game_4.drawable_shape.active_state.has_fresh_surface = True
        self.focusable_buttons.extend([btn_start_game_1,btn_start_game_2,btn_start_game_3,btn_start_game_4])
        self.play_buttons.extend([btn_start_game_1,btn_start_game_2,btn_start_game_3,btn_start_game_4])
        btn_start_game_1.visible = False
        btn_start_game_2.visible = False
        btn_start_game_3.visible = False
        btn_start_game_4.visible = False
    def process_events(self, event):

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
                if ui_element == self.stage_buttons[0]:
                    self.stage_2_panel.visible = False
                    self.play_buttons[1].visible = False
                    self.stage_3_panel.visible = False
                    self.play_buttons[2].visible = False
                    self.stage_4_panel.visible = False
                    self.play_buttons[3].visible = False
                    self.stage_1_panel.visible = True
                    self.play_buttons[0].visible = True
                elif ui_element == self.stage_buttons[1]:
                    if self.current_stage >= 1:
                        self.stage_1_panel.visible = False
                        self.play_buttons[0].visible = False
                        self.stage_3_panel.visible = False
                        self.play_buttons[2].visible = False
                        self.stage_4_panel.visible = False
                        self.play_buttons[3].visible = False
                        self.stage_2_panel.visible = True
                        self.play_buttons[1].visible = True
                elif ui_element == self.stage_buttons[2]:
                    if self.current_stage >= 2:
                        self.stage_2_panel.visible = False
                        self.play_buttons[1].visible = False
                        self.stage_1_panel.visible = False
                        self.play_buttons[0].visible = False
                        self.stage_4_panel.visible = False
                        self.play_buttons[3].visible = False
                        self.stage_3_panel.visible = True
                        self.play_buttons[2].visible = True
                elif ui_element == self.stage_buttons[3]:
                    if self.current_stage >= 3:
                        self.stage_2_panel.visible = False
                        self.play_buttons[1].visible = False
                        self.stage_3_panel.visible = False
                        self.play_buttons[2].visible = False
                        self.stage_1_panel.visible = False
                        self.play_buttons[0].visible = False
                        self.stage_4_panel.visible = True
                        self.play_buttons[3].visible = True

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.stage_buttons[0]:
                    self.stage_2_panel.visible = False
                    self.play_buttons[1].visible = False
                    self.stage_3_panel.visible = False
                    self.play_buttons[2].visible = False
                    self.stage_4_panel.visible = False
                    self.play_buttons[3].visible = False
                    self.stage_1_panel.visible = True
                    self.play_buttons[0].visible = True

                if event.ui_element == self.stage_buttons[1]:
                    if self.current_stage >= 1:
                        self.stage_1_panel.visible = False
                        self.play_buttons[0].visible = False
                        self.stage_3_panel.visible = False
                        self.play_buttons[2].visible = False
                        self.stage_4_panel.visible = False
                        self.play_buttons[3].visible = False
                        self.stage_2_panel.visible = True
                        self.play_buttons[1].visible = True

                if event.ui_element == self.stage_buttons[2]:
                    if self.current_stage >= 2:
                        self.stage_2_panel.visible = False
                        self.play_buttons[1].visible = False
                        self.stage_1_panel.visible = False
                        self.play_buttons[0].visible = False
                        self.stage_4_panel.visible = False
                        self.play_buttons[3].visible = False
                        self.stage_3_panel.visible = True
                        self.play_buttons[2].visible = True

                if event.ui_element == self.stage_buttons[3]:
                    if self.current_stage >= 3:
                        self.stage_2_panel.visible = False
                        self.play_buttons[1].visible = False
                        self.stage_3_panel.visible = False
                        self.play_buttons[2].visible = False
                        self.stage_1_panel.visible = False
                        self.play_buttons[0].visible = False
                        self.stage_4_panel.visible = True
                        self.play_buttons[3].visible = True

    def draw(self):
        self.screen.blit(self.story_map_bg, vp(0, 0))
        self.gui_manager.draw_ui(self.screen)
        # if self.stage_1_text_visible:
        #     self.screen.blit(self.stage_1_text, vp(331, 224))
        # if self.stage_2_text_visible:
        #     self.screen.blit(self.stage_2_text, vp(400, 400))
        # if self.stage_3_text_visible:
        #     self.screen.blit(self.stage_3_text, vp(600, 450))
        # if self.stage_4_text_visible:
        #     self.screen.blit(self.stage_4_text, vp(900, 224))

        for i in range(len(self.stage_buttons)):
            if i > self.current_stage:
                self.screen.blit(self.lock, (self.stage_buttons[i].rect.x - vw(50), self.stage_buttons[i].rect.y - vh(80)))







