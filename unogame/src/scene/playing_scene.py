import pygame
from pygame_gui.core import ObjectID
from pygame_gui.elements import UIButton
from config.configuration import SCREEN_WIDTH, SCREEN_HEIGHT, vw, vh, vp, KEYBOARD_MAP

from assets import image_keys
from assets.image_loader import ImageLoader
from scene import Scene
from states.playing_state import PlayingState
from utils import action_name, overlay_name
from widgets import FocusableUIButton



class PlayingScene(Scene):
    def initialize_elements(self):
        self.create_card_buttons()
        self.create_side_buttons()

    def __init__(self, screen, gui_manager, params=None):  # , image_loader: ImageLoader):
        super().__init__(screen, gui_manager, params)  # , image_loader)
        self.state = PlayingState()
        print(params)

        self.card_stack = pygame.image.load("assets/playing_game_img/card_stack.png")
        self.btn_deck = pygame.image.load("assets/playing_game_img/deck.png")
        self.btn_uno = pygame.image.load("assets/playing_game_img/btn_uno.png")
        self.btn_view_cards = pygame.image.load("assets/playing_game_img/btn_view_cards.png")
        self.btn_turn_off = pygame.image.load("assets/playing_game_img/btn_turn_off.png")
        self.btn_pause = pygame.image.load("assets/playing_game_img/btn_pause.png")
        self.my_cat = pygame.image.load("assets/playing_game_img/my_cat.png")
        self.small_card = pygame.image.load("assets/playing_game_img/small_card.png")

        self.cat1 = pygame.image.load("assets/playing_game_img/cat1.png")
        self.cat2 = pygame.image.load("assets/playing_game_img/cat2.png")
        self.cat3 = pygame.image.load("assets/playing_game_img/cat3.png")
        self.cat4 = pygame.image.load("assets/playing_game_img/cat4.png")
        self.cat5 = pygame.image.load("assets/playing_game_img/cat5.png")

        self.opponent_players_text = ["player1", "player2", "player3", "player4", "player5"]
        self.opponent_players = [self.cat1, self.cat2, self.cat3, self.cat4, self.cat5]
        self.deck_num = 3

        # self.card_image = image_loader.get_image(image_keys.IMG_CARD)
        self.resize_images()
        self.initialize_elements()

    def resize_images(self):
        #self.card_image = pygame.transform.smoothscale(self.card_image, vp(110, 176))
        super().resize_images()
        self.card_stack = pygame.transform.scale(self.card_stack, vp(110, 176))
        self.btn_deck = pygame.transform.scale(self.btn_deck, vp(127, 188))
        self.btn_uno = pygame.transform.scale(self.btn_uno, vp(163, 115))
        self.btn_view_cards = pygame.transform.scale(self.btn_view_cards, vp(199, 107))
        self.btn_turn_off = pygame.transform.scale(self.btn_turn_off, vp(179, 110))
        self.btn_pause = pygame.transform.scale(self.btn_pause, vp(91, 129))
        self.my_cat = pygame.transform.scale(self.my_cat, vp(121, 141))
        self.cat1 = pygame.transform.scale(self.cat1, vp(80, 120))
        self.cat2 = pygame.transform.scale(self.cat2, vp(80, 120))
        self.cat3 = pygame.transform.scale(self.cat3, vp(80, 120))
        self.cat4 = pygame.transform.scale(self.cat4, vp(80, 120))
        self.cat5 = pygame.transform.scale(self.cat5, vp(80, 120))
        self.small_card = pygame.transform.scale(self.small_card, vp(50, 79))

    def create_card_buttons(self):
        btn_deck = FocusableUIButton(
            relative_rect=pygame.Rect((SCREEN_WIDTH/2 - (127+25), vh(241)), vp(127, 188)),
            text="",
            manager=self.gui_manager,
            object_id=ObjectID(object_id=f"button_b_1", class_id="@playing_game_deck")
        )
        btn_uno = FocusableUIButton(
            relative_rect=pygame.Rect((SCREEN_WIDTH/2 + 150, SCREEN_HEIGHT / 2 - 60), vp(163, 115)),
            text="",
            manager=self.gui_manager,
            object_id=ObjectID(object_id=f"button_b_1", class_id="@playing_game_btn_uno")
        )
        btn_pause = FocusableUIButton(
            relative_rect=pygame.Rect((vw(23), SCREEN_HEIGHT - 143), vp(91, 129)),
            text="",
            manager=self.gui_manager,
            object_id=ObjectID(object_id=f"button_b_1", class_id="@playing_game_btn_pause")
        )
        btn_deck.drawable_shape.states['normal'].surface.blit(self.btn_deck, (0, 0))
        btn_uno.drawable_shape.states['normal'].surface.blit(self.btn_uno, (0, 0))
        btn_pause.drawable_shape.states['normal'].surface.blit(self.btn_pause, (0, 0))

        btn_deck.drawable_shape.active_state.has_fresh_surface = True
        btn_uno.drawable_shape.active_state.has_fresh_surface = True
        btn_pause.drawable_shape.active_state.has_fresh_surface = True

        self.focusable_buttons.extend([btn_deck, btn_uno, btn_pause])

    def create_side_buttons(self):
        btn_view_cards = FocusableUIButton(
            relative_rect=pygame.Rect((SCREEN_WIDTH - 200, SCREEN_HEIGHT / 2 - 140), vp(199, 107)),
            text="",
            manager=self.gui_manager,
            object_id=ObjectID(object_id=f"button_b_1", class_id="@playing_game_btn_view_cards")
        )
        btn_turn_off = FocusableUIButton(
            relative_rect=pygame.Rect((SCREEN_WIDTH - 180, SCREEN_HEIGHT / 2 - 20), vp(179, 110)),
            text="",
            manager=self.gui_manager,
            object_id=ObjectID(object_id=f"button_b_1", class_id="@playing_game_btn_turn_off")
        )
        btn_view_cards.drawable_shape.states['normal'].surface.blit(self.btn_view_cards, (0, 0))
        btn_turn_off.drawable_shape.states['normal'].surface.blit(self.btn_turn_off, (0, 0))
        btn_view_cards.drawable_shape.active_state.has_fresh_surface = True
        btn_turn_off.drawable_shape.active_state.has_fresh_surface = True

        self.focusable_buttons.extend([btn_view_cards, btn_turn_off])

    def process_events(self, event):
        if event.type == pygame.KEYDOWN:
            key_event = event.key
            action = get_action(key_event)
            if action == action_name.PAUSE:
                self.state.active_overlay(overlay_name.CONFIGURATION)

    def draw(self):
        self.screen.fill((141, 168, 104))
        # Add your game drawing code here
        self.screen.blit(self.card_stack, vp(SCREEN_WIDTH / 2 + 25, 247))
        self.screen.blit(self.my_cat, vp(SCREEN_WIDTH / 2 - 80, SCREEN_HEIGHT - 238))
        self.screen.blit(self.small_card, vp(SCREEN_WIDTH / 2 + 40, SCREEN_HEIGHT - 180))

        for i in range(len(self.opponent_players)):
            x = 40 + i * 260
            y = 0
            self.screen.blit(self.opponent_players[i], vp(x, y + 70))
            self.screen.blit(self.small_card, vp(x + 90, y + 100))

        self.gui_manager.draw_ui(self.screen)
