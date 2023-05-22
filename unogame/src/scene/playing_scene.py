from typing import Any

import pygame
from pygame import Surface
from pygame.event import Event
from pygame.sprite import AbstractGroup
from pygame_gui.core import ObjectID

from classes.cards.wild_cards import WildChangeColorCard, WildGetFourCard
from classes.enums.colors import Colors
from classes.game.networking import Networking
from config.configuration import get_screen_width, get_screen_height, vw, vh, vp, KEYBOARD_MAP, get_action

from scene import Scene
from scene.main_screen import EventGroup
from states.playing_state import PlayingState
from utils import action_name, overlay_name
from utils.card_utility import card_image, random_cards
from utils.resource_path import resource_path
from widgets import FocusableUIButton
from utils.image_utility import load_image


class Cards(pygame.sprite.Sprite):
    CARD_END = pygame.event.custom_type()

    def moveToCenter(self):
        from config import configuration
        dest_x = configuration.get_screen_width() / 2
        dest_y = configuration.get_screen_height() / 2
        print(int(vw(1) * (dest_x - self.rect.x)))
        self.rect.x += int(vw(10) * (dest_x - self.rect.x))
        self.rect.y += int(vh(10) * (dest_y - self.rect.y))

    def __init__(self, user_id: int, x, y, networking: Networking, *groups: AbstractGroup,
                 max_width: int = vw(600), is_blank: bool = True, rotation: int = 0):
        super().__init__(*groups)
        self.networking = networking
        self.user_id = user_id
        self.max_width = max_width
        self.is_blank = is_blank
        self.image = pygame.transform.rotate(
            Surface(vp(self.max_width + 120, 180), pygame.SRCALPHA, 32), rotation)
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.card_set = load_image('images/cards.png')
        self._active_card_index = -1
        self.rotation = rotation
        self.wrong_sound = pygame.mixer.Sound(resource_path("assets/sound/wrong.mp3"))
        from config import configuration
        self.wrong_sound.set_volume(configuration.get_whole_sound_volume())
        self.throw_sound = pygame.mixer.Sound(resource_path("assets/sound/throw_card.mp3"))
        self.throw_sound.set_volume(configuration.get_whole_sound_volume())

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            print("Card Clicked!" + str(self._active_card_index))
            if self._active_card_index >= 0 and \
                    self.networking.is_our_move:
                if self.networking.throw_card(0, self._active_card_index):
                    pass
                pygame.time.set_timer(pygame.USEREVENT + 100, 100, 10)
                from config import configuration
                if configuration.is_sound_on():
                    self.throw_sound.play(1)
            else:
                from config import configuration
                if configuration.is_sound_on():
                    self.wrong_sound.play(1)
                # (because it is not your way)

    def update(self, *args: Any, **kwargs: Any):
        deck = self.networking.current_game.users[self.user_id].deck
        self.image.fill((0, 0, 0, 0))
        try:
            if not self.is_blank:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # this is the most elegant solution what i can think of (and very fast solution too)
                if self.rect.collidepoint(mouse_x, mouse_y):
                    # coordinates regarding our sprite
                    mouse_x -= self.rect.x
                    self._active_card_index = int(mouse_x // (self.max_width / len(deck.cards)))
                else:
                    self._active_card_index = -1
            for i, card in enumerate(deck.cards):
                image = pygame.transform.rotate(
                    card_image(self.card_set, card) if not self.is_blank else load_image(
                        'images/blank_card.png'), self.rotation)
                x, y = (self.max_width / len(deck.cards)) * i, 60 if not self.is_blank else 0
                if not self.is_blank and self._active_card_index == i:
                    y -= 60
                if self.rotation // 90 % 2 != 0:
                    x, y = y, x
                self.image.blit(image, (x, y))
            if not deck.cards:
                raise ValueError
        except (ZeroDivisionError, ValueError):
            # this exception will happen ONLY ONCE, when somebody has 0 cards
            # i know, that is strange solution, but trust me
            # this is just prototype, hehehe
            pygame.event.post(Event(self.CARD_END))


class GameCards(pygame.sprite.Sprite):
    def __init__(self, networking: Networking, x, y, *groups: AbstractGroup):
        super().__init__(*groups)
        self.networking = networking
        self.rect = pygame.rect.Rect(x, y, 120, 180)
        self.card_set = load_image('images/cards.png')
        self.image = self.card_set

    def update(self, *args: Any, **kwargs: Any) -> None:
        deck = self.networking.current_game.deck
        # TODO: draw multiple cards, with various rotation and another pretty things
        self.image = card_image(self.card_set, deck.cards[0])

class ColorChooser(pygame.sprite.Sprite):
    def __init__(self, x, y, networking: Networking, *groups: AbstractGroup):
        super().__init__(*groups)
        self.networking = networking
        self.rect = pygame.rect.Rect(x, y, 206, 206)
        self.image = pygame.surface.Surface((206, 206), pygame.SRCALPHA, 32)
        self._active_color = None
        self._colors = {
            (0, 0): (load_image('images/color_chooser/red.png'),
                     load_image('images/color_chooser/red_active.png')),
            (1, 0): (load_image('images/color_chooser/green.png'),
                     load_image('images/color_chooser/green_active.png')),
            (0, 1): (load_image('images/color_chooser/yellow.png'),
                     load_image('images/color_chooser/yellow_active.png')),
            (1, 1): (load_image('images/color_chooser/blue.png'),
                     load_image('images/color_chooser/blue_active.png')),
        }

    def handle_events(self, event: Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            card = None
            if self._active_color == (0, 0):
                card = random_cards(color=Colors.RED)[0]
            if self._active_color == (1, 0):
                card = random_cards(color=Colors.GREEN)[0]
            if self._active_color == (0, 1):
                card = random_cards(color=Colors.YELLOW)[0]
            if self._active_color == (1, 1):
                card = random_cards(color=Colors.BLUE)[0]
            self.networking.throw_card(0, card, ignore=True)
            #self.networking.throw_card(self.networking.user.id, card, ignore=True)
            # self.networking.current_game.next_player()
            # time.sleep(1)
            return



    def update(self, *args: Any, **kwargs: Any) -> None:
        self.image.fill((0, 0, 0, 0))
        for x in range(2):
            for y in range(2):
                rect = pygame.rect.Rect(self.rect.x + x * 103, self.rect.y + y * 103, 103, 103)
                if rect.collidepoint(pygame.mouse.get_pos()):
                    self.image.blit(self._colors[(x, y)][1], dest=(x * 103, y * 103))
                    self._active_color = (x, y)
                else:
                    self.image.blit(self._colors[(x, y)][0], dest=(x * 103, y * 103))



class CardGiver(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, networking: Networking, *groups: AbstractGroup):
        super().__init__(*groups)
        self.networking = networking
        self._active = load_image("playing_game_img/deck_active.png")
        # self._active = load_image('images/deck_active.png')
        self._non_active = load_image("playing_game_img/deck.png")
        self.image = self._active
        self.rect = self.image.get_rect()
        self.is_active = False
        self.rect.x = x
        self.rect.y = y

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_active:
                if self.networking.is_our_move:  # and self.networking.get_user_from_game() == 0:
                    self.networking.get_card()

    def update(self, *args: Any, **kwargs: Any) -> None:
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.image = self._active
            self.is_active = True
        else:
            self.is_active = False
            self.image = self._non_active


class UnoButton(pygame.sprite.Sprite):
    def __init__(self, x, y, networking, *groups: AbstractGroup):
        super().__init__(*groups)
        self.frames = []
        self.rect = pygame.Rect(0, 0, vw(127), vh(188))
        self.cur_frame = 0
        self._direction_left = False
        self.is_active = False
        self.networking = networking
        self.rect.x = x
        self.rect.y = y
        self.image = load_image('playing_game_img/btn_uno.png')
        self.ai_timer_event = pygame.USEREVENT + 4
        self.ai_time = 5
        self.timer_able = True

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_active:
                self.networking.say_uno()
        if event.type == pygame.USEREVENT + 4:
            pass
            # self.ai_time -= 1
            # if self.ai_time <= 0:
            #     self.ai_time = 5
            #     self.networking.get_card()
            #     self.timer_able = True

    def update(self):
        if not self.rect.collidepoint(pygame.mouse.get_pos()):
            self.is_active = False
            # if self.cur_frame == 99:
            #    self._direction_left = True
            # elif self.cur_frame == 0:
            #    self._direction_left = False
            # if self._direction_left:
            #    self.cur_frame -= 1
            # else:
            #    self.cur_frame += 1
            # self.image = self.frames[self.cur_frame // 20]
        else:
            self.is_active = True
            # self.image = self.frames[4]
            if self.timer_able:
                self.timer_able = False
                pygame.time.set_timer(self.ai_timer_event, 1000)


class PlayingScene(Scene):
    def initialize_elements(self):
        self.create_card_buttons()
        self.create_side_buttons()

    def __init__(self, screen, gui_manager, params=None):  # , image_loader: ImageLoader):
        super().__init__(screen, gui_manager, params)  # , image_loader)
        self.state = PlayingState()
        self.timer_event = pygame.USEREVENT + 1
        self.turn_time = 30
        self.TURN_TIME_EVENT_CODE = 99
        pygame.time.set_timer(self.TURN_TIME_EVENT_CODE, 1000)
        self._miscellaneous_group = EventGroup()
        self.player_counts = len(params)
        self.card_stack = load_image("playing_game_img/card_stack.png")
        self.btn_uno = load_image("playing_game_img/btn_uno.png")
        self.btn_view_cards = load_image("playing_game_img/btn_view_cards.png")
        self.btn_turn_off = load_image("playing_game_img/btn_turn_off.png")
        self.btn_pause = load_image("playing_game_img/btn_pause.png")
        self.my_cat = load_image("playing_game_img/my_cat.png")
        self.small_card = load_image("playing_game_img/small_card.png")
        self.card_set = load_image('images/cards.png')
        self.font = pygame.font.SysFont("comicsansms", 22, True, False)
        self.cat_images = [load_image("playing_game_img/cat1.png"),
                           load_image("playing_game_img/cat2.png"),
                           load_image("playing_game_img/cat3.png"),
                           load_image("playing_game_img/cat4.png"),
                           load_image("playing_game_img/cat5.png")]
        self.turn_image = load_image("playing_game_img/turn.png")

        self.opponent_players = params[1:]
        self.player = params[0]
        self.deck_num = 3

        self._all_cards = EventGroup()
        self._game_deck = pygame.sprite.Group()
        self.networking = Networking(params)
        self._game_cards = GameCards(self.networking, vw(640 - 60), vh(360 - 120),
                                     self._all_cards)

        self._card_giver = CardGiver(get_screen_width() / 2 - (127 + 75), vh(235), self.networking,
                                     self._miscellaneous_group)
        self._uno_button = UnoButton(get_screen_width() / 2 + 150, get_screen_height() / 2 - 60, self.networking)
        # self.card_image = image_loader.get_image(image_keys.IMG_CARD)
        self.resize_images()
        self.initialize_elements()
        self._color_chooser = ColorChooser(540, 260, self.networking, self._miscellaneous_group)
        self.last_user = self.networking.user
        self.draw_my_player()


    def draw_my_player(self):
        Cards(0, vw((1280 / 2) - 300), vh(600), self.networking,
              self._all_cards, is_blank=False)

    def draw_players(self, players):
        # todo pygame_gui로 players 만큼 그리기

        text_total_timer = self.font.render(str(self.turn_time), True, (0, 0, 0))
        text_total_timer_rect = text_total_timer.get_rect()
        text_total_timer_rect.x = 350
        text_total_timer_rect.y = 300
        self.screen.blit(text_total_timer, text_total_timer_rect)

        text_myname = self.font.render(self.player.name, True, (0, 0, 0))
        text_myrect = text_myname.get_rect()
        text_myrect.x = get_screen_width() / 2 - 80
        text_myrect.y = get_screen_height() - 160
        self.screen.blit(text_myname, text_myrect)

        if self.player == self.networking.get_user_from_game():
            text_turn = self.font.render("Meow! My Turn!", True, (255, 0, 0))
            text_turn_rect = text_turn.get_rect()
            text_turn_rect.x = vw((1280 / 2) - 300)
            text_turn_rect.y = vh(600)
            self.screen.blit(text_turn, text_turn_rect)
        for i in range(len(players)):

            x = 40 + i * 260
            y = 0
            if players[i] == self.networking.get_user_from_game():
                text_turn = self.font.render("Meow! My Turn!", True, (255, 0, 0))
                text_turn_rect = text_turn.get_rect()
                text_turn_rect.x = x
                text_turn_rect.y = y + 10
                self.screen.blit(text_turn, text_turn_rect)
            text_name = self.font.render(self.opponent_players[i].name, True, (0, 0, 0))
            text_rect = text_name.get_rect()
            text_rect.x = x
            text_rect.y = y + 200

            text_card_num = self.font.render(str(len(self.opponent_players[i].deck.cards)), True, (0, 0, 0))
            text_cardrect = text_card_num.get_rect()
            text_cardrect.x = x + 108
            text_cardrect.y = y + 123

            self.screen.blit(text_name, text_rect)
            self.screen.blit(self.cat_images[i], vp(x, y + 70))
            self.screen.blit(self.small_card, vp(x + 90, y + 100))
            self.screen.blit(text_card_num, text_cardrect)


    def resize_images(self):
        super().resize_images()
        self.card_stack = pygame.transform.scale(self.card_stack, vp(110, 176))
        self.btn_uno = pygame.transform.scale(self.btn_uno, vp(163, 115))
        self.btn_view_cards = pygame.transform.scale(self.btn_view_cards, vp(199, 107))
        self.btn_turn_off = pygame.transform.scale(self.btn_turn_off, vp(179, 110))
        self.btn_pause = pygame.transform.scale(self.btn_pause, vp(91, 129))
        self.my_cat = pygame.transform.scale(self.my_cat, vp(121, 141))

    def create_card_buttons(self):
        btn_pause = FocusableUIButton(
            relative_rect=pygame.Rect((vw(23), get_screen_height() - 143), vp(91, 129)),
            text="",
            manager=self.gui_manager,
            object_id=ObjectID(object_id=f"button_b_1", class_id="@playing_game_btn_pause")
        )
        btn_pause.drawable_shape.states['normal'].surface.blit(self.btn_pause, (0, 0))

        btn_pause.drawable_shape.active_state.has_fresh_surface = True

        self.focusable_buttons.extend([btn_pause])

    def create_side_buttons(self):
        btn_view_cards = FocusableUIButton(
            relative_rect=pygame.Rect((get_screen_width() - 200, get_screen_height() / 2 - 140), vp(199, 107)),
            text="",
            manager=self.gui_manager,
            object_id=ObjectID(object_id=f"button_b_1", class_id="@playing_game_btn_view_cards")
        )
        btn_turn_off = FocusableUIButton(
            relative_rect=pygame.Rect((get_screen_width() - 180, get_screen_height() / 2 - 20), vp(179, 110)),
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
        self._all_cards.handle_events(event)
        self._miscellaneous_group.handle_events(event)
        cur_user = self.networking.get_user_from_game()
        if cur_user != self.last_user:
            print("======Current User! "+cur_user.name+"======")
            self.last_user = cur_user
            self.turn_time = 30
        if cur_user.is_ai:
            if cur_user.throwable:
                pygame.time.set_timer(self.timer_event + 5, 3000, 1)
            cur_user.throwable = False
        if event.type == self.timer_event+5 and cur_user.is_ai:
            cur_user.do_action(networking=self.networking)
        if event.type == pygame.KEYDOWN:
            key_event = event.key
            action = get_action(key_event)
            if action == action_name.PAUSE:
                self.state.active_overlay(overlay_name.CONFIGURATION)
        if event.type == self.TURN_TIME_EVENT_CODE:
            self.turn_time -= 1
            if self.turn_time <= 0:
                self.turn_time = 30
                self.networking.get_card()



    def draw(self):
        if (isinstance(self.networking.current_game.deck.cards[0], WildChangeColorCard) or
            isinstance(self.networking.current_game.deck.cards[0], WildGetFourCard)) and \
                self.networking.is_our_move and not self.networking.get_user_from_game().is_ai:
            self._color_chooser.add(self._miscellaneous_group)
        else:
            self._color_chooser.remove(self._miscellaneous_group)
        self.screen.fill((141, 168, 104))
        self.draw_players(self.opponent_players)
        self._all_cards.draw(self.screen)
        self._all_cards.update()
        if not self.networking.get_user_from_game().deck.uno_said \
                and len(self.networking.get_user_from_game().deck.cards) == 2:
            self._uno_button.add(self._miscellaneous_group)
        else:
            self._uno_button.remove(self._miscellaneous_group)

        self._miscellaneous_group.draw(self.screen)
        self._miscellaneous_group.update()
        self.gui_manager.draw_ui(self.screen)
