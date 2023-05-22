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
from widgets import ScrollableUIButton, FocusableUIButton
from scene import Scene
from config import configuration


class ConfigurationOverlayScene(OverlayScene):

    def __init__(self, screen, overlay_manager):
        super().__init__(screen, overlay_manager)

        self.tab_button_clicked = False

        self.close_btn_image = load_image("btn_close_overlay.png")
        self.close_btn_image = pygame.transform.smoothscale(self.close_btn_image, vp(60, 60))
        self.state = ConfigurationState()

        # 배경 이미지 생성
        self.panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(vw(149), (get_screen_height() - vh(633)) / 2, vw(984), vh(633)),
            manager=self.overlay_manager,
            starting_layer_height=2,
            object_id=ObjectID(object_id="overlay_panel", class_id="@overlay_panels")
        )
        # 화면 설정 배경
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
        # 키설정 배경
        self.up_key_setting_bg = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(vw(186), (get_screen_height() - vh(100)) / 2, vw(421), vh(60)),
            manager=self.overlay_manager,
            starting_layer_height=2,
            object_id=ObjectID(object_id="overlay_panel", class_id="@overlay_panels")
        )
        self.down_key_setting_bg = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(vw(186 + 450), (get_screen_height() - vh(100)) / 2, vw(421), vh(60)),
            manager=self.overlay_manager,
            starting_layer_height=2,
            object_id=ObjectID(object_id="overlay_panel", class_id="@overlay_panels")
        )
        self.right_key_setting_bg = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(vw(186), (get_screen_height() - vh(250)) / 2, vw(421), vh(60)),
            manager=self.overlay_manager,
            starting_layer_height=2,
            object_id=ObjectID(object_id="overlay_panel", class_id="@overlay_panels")
        )
        self.left_key_setting_bg = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(vw(186 + 450), (get_screen_height() - vh(250)) / 2, vw(421), vh(60)),
            manager=self.overlay_manager,
            starting_layer_height=2,
            object_id=ObjectID(object_id="overlay_panel", class_id="@overlay_panels")
        )
        # 사운드 설정 배경
        self.whole_sound_setting_bg = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(vw(186), (get_screen_height() - vh(250)) / 2, vw(886), vh(60)),
            manager=self.overlay_manager,
            starting_layer_height=2,
            object_id=ObjectID(object_id="overlay_panel", class_id="@overlay_panels")
        )
        self.background_sound_setting_bg = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(vw(186), (get_screen_height() - vh(100)) / 2, vw(886), vh(60)),
            manager=self.overlay_manager,
            starting_layer_height=2,
            object_id=ObjectID(object_id="overlay_panel", class_id="@overlay_panels")
        )
        self.effect_sound_setting_bg = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(vw(186), (get_screen_height() / 2 + vh(25)) , vw(886), vh(60)),
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

        # 탭 버튼 이미지
        self.btn_display_setting = load_image("tab_display.png")
        self.btn_display_setting = pygame.transform.smoothscale(self.btn_display_setting, vp(107, 52))
        self.btn_key_setting = load_image("tab_key.png")
        self.btn_key_setting = pygame.transform.smoothscale(self.btn_key_setting, vp(107, 52))
        self.btn_sound_setting = load_image("tab_sound.png")
        self.btn_sound_setting = pygame.transform.smoothscale(self.btn_sound_setting, vp(107, 52))

        self.input_key = []
        self.input_sound = []
        self.blind_buttons = []
        self.size_buttons = []
        self.tab_buttons = []
        self.current_width = 1280
        self.current_height = 720
        self.current_blind = "default"

        self.panel.drawable_shape.states['normal'].surface.blit(self.overlay_bg_image, (0, 0))
        self.panel.drawable_shape.active_state.has_fresh_surface = True

        # 화면 설정 배경 이미지
        self.small_config_bg = load_image("small_config_bg.png")
        self.small_config_bg = pygame.transform.smoothscale(self.small_config_bg, vp(886, 60))
        self.large_config_bg = load_image("large_config_bg.png")
        self.large_config_bg = pygame.transform.smoothscale(self.large_config_bg, vp(886, 155))
        self.large_config_panel.drawable_shape.states['normal'].surface.blit(self.large_config_bg, (0, 0))
        self.small_config_panel.drawable_shape.states['normal'].surface.blit(self.small_config_bg, (0, 0))
        self.large_config_panel.drawable_shape.active_state.has_fresh_surface = True
        self.small_config_panel.drawable_shape.active_state.has_fresh_surface = True
        self.create_blind_buttons()
        self.create_size_buttons()

        # 키 설정 이미지
        self.up_key_setting = load_image("up_key_setting.png")
        self.down_key_setting = load_image("down_key_setting.png")
        self.left_key_setting = load_image("left_key_setting.png")
        self.right_key_setting = load_image("right_key_setting.png")
        self.up_key_setting = pygame.transform.smoothscale(self.up_key_setting, vp(421, 60))
        self.down_key_setting = pygame.transform.smoothscale(self.down_key_setting, vp(421, 60))
        self.left_key_setting = pygame.transform.smoothscale(self.left_key_setting, vp(421, 60))
        self.right_key_setting = pygame.transform.smoothscale(self.right_key_setting, vp(421, 60))

        self.up_key_setting_bg.drawable_shape.states['normal'].surface.blit(self.up_key_setting, (0, 0))
        self.down_key_setting_bg.drawable_shape.states['normal'].surface.blit(self.down_key_setting, (0, 0))
        self.left_key_setting_bg.drawable_shape.states['normal'].surface.blit(self.left_key_setting, (0, 0))
        self.right_key_setting_bg.drawable_shape.states['normal'].surface.blit(self.right_key_setting, (0, 0))
        self.up_key_setting_bg.drawable_shape.active_state.has_fresh_surface = True
        self.down_key_setting_bg.drawable_shape.active_state.has_fresh_surface = True
        self.left_key_setting_bg.drawable_shape.active_state.has_fresh_surface = True
        self.right_key_setting_bg.drawable_shape.active_state.has_fresh_surface = True
        self.up_key_setting_bg.visible = False
        self.down_key_setting_bg.visible = False
        self.left_key_setting_bg.visible = False
        self.right_key_setting_bg.visible = False

        self.create_elements()
        self.create_tab_buttons()
        self.create_input_key()
        self.create_input_sound()


        # 초기 키 설정 화면 안보이도록
        for i in range(len(self.input_key)):
            self.input_key[i].visible = False
        # 초기 사운드 설정 화면 안보이도록
        for i in range(len(self.input_sound)):
            self.input_sound[i].visible = False

        # 사운드 설정 이미지
        self.whole_sound_setting = load_image("whole_sound_setting_bg.png")
        self.background_sound_setting = load_image("background_sound_setting_bg.png")
        self.effect_sound_setting = load_image("effect_sound_setting_bg.png")
        self.whole_sound_setting = pygame.transform.smoothscale(self.whole_sound_setting, vp(886, 60))
        self.background_sound_setting = pygame.transform.smoothscale(self.background_sound_setting, vp(886, 60))
        self.effect_sound_setting = pygame.transform.smoothscale(self.effect_sound_setting, vp(886, 60))

        self.whole_sound_setting_bg.drawable_shape.states['normal'].surface.blit(self.whole_sound_setting, (0, 0))
        self.background_sound_setting_bg.drawable_shape.states['normal'].surface.blit(self.background_sound_setting, (0, 0))
        self.effect_sound_setting_bg.drawable_shape.states['normal'].surface.blit(self.effect_sound_setting, (0, 0))
        self.whole_sound_setting_bg.drawable_shape.active_state.has_fresh_surface = True
        self.background_sound_setting_bg.drawable_shape.active_state.has_fresh_surface = True
        self.effect_sound_setting_bg.drawable_shape.active_state.has_fresh_surface = True
        self.whole_sound_setting_bg.visible = False
        self.background_sound_setting_bg.visible = False
        self.effect_sound_setting_bg.visible = False

        # 사운드 설정 값
        self.whole_sound=""
        self.background_sound=""
        self.effect_sound=""

        # 키 세팅 값
        self.key_setting = ""
        self.up_key = ""
        self.down_key = ""
        self.left_key = ""
        self.right_key = ""

    def create_input_key(self):
        self.up_key_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(vp(300, 275), vp(50, 50)),
            container=self.panel,
            manager=self.overlay_manager
        )
        self.down_key_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(vp(750, 275), vp(50, 50)),
            container=self.panel,
            manager=self.overlay_manager
        )
        self.left_key_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(vp(750, 200), vp(50, 50)),
            container=self.panel,
            manager=self.overlay_manager
        )
        self.right_key_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(vp(300, 200), vp(50, 50)),
            container=self.panel,
            manager=self.overlay_manager
        )
        self.input_key.extend([self.up_key_input, self.down_key_input, self.left_key_input, self.right_key_input])

    def create_input_sound(self):
        self.whole_sound_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(vp(500, 200), vp(100, 50)),
            container=self.panel,
            manager=self.overlay_manager
        )
        self.background_sound_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(vp(500, 275), vp(100, 50)),
            container=self.panel,
            manager=self.overlay_manager
        )
        self.effect_sound_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(vp(500, 350), vp(100, 50)),
            container=self.panel,
            manager=self.overlay_manager
        )
        self.input_sound.extend([self.whole_sound_input, self.background_sound_input, self.effect_sound_input])

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

        self.close_button.drawable_shape.states['normal'].surface.blit(self.close_btn_image, (0, 0))
        self.initialize_settings_button.drawable_shape.states['normal'].surface.blit(self.initialize_settings_btn, (0, 0))

        self.close_button.drawable_shape.active_state.has_fresh_surface = True
        self.initialize_settings_button.drawable_shape.active_state.has_fresh_surface = True

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
            text="protanopia",
            container=self.panel,
            manager=self.overlay_manager
        )
        self.blind_mode_tritanopia = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(vp(552, 339), vp(109, 28)),
            text="tritanopia",
            container=self.panel,
            manager=self.overlay_manager
        )
        self.blind_mode_deuteranopia = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(vp(734, 339), vp(147, 28)),
            text="deuteranopia",
            container=self.panel,
            manager=self.overlay_manager
        )
        self.blind_buttons.extend([self.blind_mode_normal_vision,self.blind_mode_protanopia,self.blind_mode_tritanopia,self.blind_mode_deuteranopia])

    def create_tab_buttons(self):
        btn_display_setting = FocusableUIButton(
            relative_rect=pygame.Rect(vp(50, 70), vp(107, 52)),
            text="",
            container=self.panel,
            manager=self.overlay_manager
        )
        btn_key_setting = FocusableUIButton(
            relative_rect=pygame.Rect(vp(50 + 120, 70), vp(107, 52)),
            text="",
            container=self.panel,
            manager=self.overlay_manager
        )
        btn_sound_setting = FocusableUIButton(
            relative_rect=pygame.Rect(vp(170 + 120, 70), vp(107, 52)),
            text="",
            container=self.panel,
            manager=self.overlay_manager
        )
        btn_display_setting.drawable_shape.states['normal'].surface.blit(self.btn_display_setting, (0, 0))
        btn_display_setting.drawable_shape.active_state.has_fresh_surface = True
        btn_key_setting.drawable_shape.states['normal'].surface.blit(self.btn_key_setting, (0, 0))
        btn_key_setting.drawable_shape.active_state.has_fresh_surface = True
        btn_sound_setting.drawable_shape.states['normal'].surface.blit(self.btn_sound_setting, (0, 0))
        btn_sound_setting.drawable_shape.active_state.has_fresh_surface = True

        self.tab_buttons.extend([btn_display_setting, btn_key_setting, btn_sound_setting])
        self.focusable_buttons.extend([btn_display_setting, btn_key_setting, btn_sound_setting])

    def fire_tab_button_0_event(self):
        self.large_config_panel.visible = True
        self.small_config_panel.visible = True
        for i in range(len(self.blind_buttons)):
            self.blind_buttons[i].visible = True
        for i in range(len(self.size_buttons)):
            self.size_buttons[i].visible = True
            self.blind_buttons[i].visible = True
        for i in range(len(self.input_key)):
            self.input_key[i].visible = False

        self.up_key_setting_bg.visible = False
        self.down_key_setting_bg.visible = False
        self.left_key_setting_bg.visible = False
        self.right_key_setting_bg.visible = False

        for i in range(len(self.input_sound)):
            self.input_sound[i].visible = False
        self.whole_sound_setting_bg.visible = False
        self.background_sound_setting_bg.visible = False
        self.effect_sound_setting_bg.visible = False

    def fire_tab_button_1_event(self):
        self.large_config_panel.visible = False
        self.small_config_panel.visible = False
        for i in range(len(self.blind_buttons)):
            self.blind_buttons[i].visible = False
        for i in range(len(self.size_buttons)):
            self.size_buttons[i].visible = False

        for i in range(len(self.input_key)):
            self.input_key[i].visible = True
        self.up_key_setting_bg.visible = True
        self.down_key_setting_bg.visible = True
        self.left_key_setting_bg.visible = True
        self.right_key_setting_bg.visible = True

        for i in range(len(self.input_sound)):
            self.input_sound[i].visible = False
        self.whole_sound_setting_bg.visible = False
        self.background_sound_setting_bg.visible = False
        self.effect_sound_setting_bg.visible = False

    def fire_tab_button_2_event(self):
        self.large_config_panel.visible = False
        self.small_config_panel.visible = False
        for i in range(len(self.blind_buttons)):
            self.blind_buttons[i].visible = False
        for i in range(len(self.size_buttons)):
            self.size_buttons[i].visible = False
        for i in range(len(self.input_key)):
            self.input_key[i].visible = False
        self.up_key_setting_bg.visible = False
        self.down_key_setting_bg.visible = False
        self.left_key_setting_bg.visible = False
        self.right_key_setting_bg.visible = False

        for i in range(len(self.input_sound)):
            self.input_sound[i].visible = True
        self.whole_sound_setting_bg.visible = True
        self.background_sound_setting_bg.visible = True
        self.effect_sound_setting_bg.visible = True

    def process_events(self, event):
        # super().process_events(event)
        # 엔터 입력시 값 입력
        if event.type == pygame.KEYDOWN:
            key_event = event.key
            action = get_action(key_event)
            if action != action_name.RETURN:
                self.key_setting = key_event
            if action == action_name.PAUSE:
                self.set_inactive()

        if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
            if event.ui_element == self.up_key_input:
                self.up_key = self.key_setting
                self.state.set_up_key(self.up_key, self.down_key, self.left_key, self.right_key)
            if event.ui_element == self.down_key_input:
                self.down_key = self.key_setting
                self.state.set_up_key(self.up_key, self.down_key, self.left_key, self.right_key)
            if event.ui_element == self.left_key_input:
                self.left_key = self.key_setting
                self.state.set_up_key(self.up_key, self.down_key, self.left_key, self.right_key)
            if event.ui_element == self.right_key_input:
                self.right_key = self.key_setting
                self.state.set_up_key(self.up_key, self.down_key, self.left_key, self.right_key)

            if event.ui_element == self.whole_sound_input:
                self.whole_sound = int(self.whole_sound_input.get_text())
                self.state.set_whole_sound_volume(self.whole_sound)
                self.state.set_background_sound_volume((int(configuration.get_background_sound_volume()) + self.whole_sound)/2)
                self.state.set_effect_sound_volume((int(configuration.get_effect_sound_volume()) + self.whole_sound)/2)
            if event.ui_element == self.background_sound_input:
                self.background_sound = int(self.background_sound_input.get_text())
                if int(configuration.get_whole_sound_volume()) > int(self.background_sound):
                    self.state.set_background_sound_volume(self.background_sound)
                else:
                    self.state.set_background_sound_volume(self.background_sound)
                    self.state.set_whole_sound_volume(self.background_sound)
            if event.ui_element == self.effect_sound_input:
                self.effect_sound = int(self.effect_sound_input.get_text())
                if int(configuration.get_whole_sound_volume()) > int(self.effect_sound):
                    self.state.set_effect_sound_volume((self.effect_sound))
                else:
                    self.state.set_effect_sound_volume(self.effect_sound)
                    self.state.set_whole_sound_volume(self.effect_sound)



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
                if not self.tab_button_clicked:
                    if event.ui_element == self.tab_buttons[0]:
                        self.fire_tab_button_0_event()

                    if event.ui_element == self.tab_buttons[1]:
                        self.fire_tab_button_1_event()

                    if event.ui_element == self.tab_buttons[2]:
                        self.fire_tab_button_2_event()

                if event.ui_element == self.initialize_settings_button:
                    self.current_width = 1280
                    self.current_height = 720
                    self.current_blind = "default"
                    self.state.set_screen_size(self.current_width, self.current_height)
                    self.state.set_color_blind(self.current_blind)
                    self.set_inactive()

    def draw(self):
        super().draw()

