import unittest

import bcrypt
import pygame
from utils.password_utility import hash_password, check_password
from utils.text_utility import center_rect, text_on_center, truncate
from utils.card_utility import random_cards
from classes.cards.card import Card
from classes.cards.special_cards import SkipCard

from states import GameState
from utils import scene_name, overlay_name

class TestUtils(unittest.TestCase):

    def test_random_cards(self):
        #amount=3 and color=None case
        cards = random_cards(amount=3)
        self.assertEqual(len(cards), 3)
        self.assertIsInstance(cards[0], SkipCard)


    #hash_password가 bytes 객체 반환하는지
    def test_hash_password(self):
        password = "my_password"
        hashed_password = hash_password(password)
        self.assertIsInstance(hashed_password, bytes)

    #check_password가 hashed password 올바르게 검사하는지
    def test_check_password(self):
        password = "my_password"
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        self.assertTrue(check_password(password, hashed_password))
        incorrect_password = "wrong_password"
        self.assertFalse(check_password(incorrect_password, hashed_password))


    def test_center_rect(self):
        rect = pygame.Rect(0, 0, 100, 50)
        center_rect(self.surface, rect)
        self.assertEqual(rect.centerx, self.surface.get_width() // 2)

    def test_text_on_center(self):
        text = "Hello, world!"
        y = self.surface.get_height() // 2
        text_on_center(self.surface, self.font, text, y)
        text_rect = self.font.get_rect(text)
        self.assertEqual(text_rect.centerx, self.surface.get_width() // 2)
        self.assertEqual(text_rect.centery, y)

    def test_truncate(self):
        long_text = "This is a very long string"
        max_len = 10
        truncated_text = truncate(long_text, max_len)
        self.assertEqual(truncated_text, "This is a...")
        short_text = "Hello"
        truncated_text = truncate(short_text, max_len)
        self.assertEqual(truncated_text, short_text)


class TestStates(unittest.TestCase):
    def setUp(self):
        self.game_state = GameState()
        self.landing_state = LandingState()
        self.lobby_state = LobbyState()
        self.menu_state = MenuState()

    #Game state
    def test_move_scene(self):
        next_scene = scene_name.PLAYING_SCENE
        next_params = { '1', '2' }
        self.game_state.move_scene(next_scene, next_params)

        self.assertTrue(self.game_state.scene_changed)
        self.assertEqual(self.game_state.next_scene_name, next_scene)
        self.assertEqual(self.game_state.next_params, next_params)

    def test_active_overlay(self):
        overlay_scene = overlay_name.CONFIGURATION
        self.game_state.active_overlay(overlay_scene)

        self.assertTrue(self.game_state.overlay_active_changed)
        self.assertTrue(self.game_state.overlay_active)
        self.assertEqual(self.game_state.overlay_scene_name, overlay_scene)

    def test_inactive_overlay(self):
        overlay_scene = overlay_name.CONFIGURATION
        self.game_state.inactive_overlay(overlay_scene)

        self.assertTrue(self.game_state.overlay_active_changed)
        self.assertFalse(self.game_state.overlay_active)
        self.assertEqual(self.game_state.overlay_scene_name, overlay_scene)

    #Landing state
    def test_start(self):
        event = pygame.event.Event(self.landing_state.timer_event)
        self.landing_state.start(event)

        self.assertTrue(self.landing_state.scene_changed)
        self.assertEqual(
            self.landing_state.next_scene_name, scene_name.MAIN_MENU)

    #Lobby state
    def test_start_single_play(self):
        players = ['1', '2']
        self.lobby_state.start_single_play(players)
        self.assertEqual(
            self.lobby_state.next_scene_name, scene_name.PLAYING_SCENE)
        self.assertEqual(self.lobby_state.next_params, players)

    def test_open_configuration(self):
        self.lobby_state.open_configuration()
        self.assertEqual(
            self.lobby_state.overlay_scene_name, overlay_name.CONFIGURATION)

    #Menu state
    def test_open_story_play(self):
        self.menu_state.open_story_play()
        self.assertEqual(
            self.menu_state.next_scene_name, scene_name.STORY_MAP_SCENE)


class TestConfigurationSetting(unittest.TestCase):

    def test_save_load(self):
        self.assertEqual(save_config_to_file(), load_config_from_file())


    def test_load_color_blind(self):
        global BLIND_MODE
        a=copy.deepcopy(BLIND_MODE)
        BLIND_MODE="deutranopia"
        save_config_to_file()
        load_config_from_file()
        print(a, BLIND_MODE)
        self.assertNotEqual(a, BLIND_MODE)

    def test_load_keybindings(self):
        global KEYBOARD_MAP
        a = copy.deepcopy(KEYBOARD_MAP)
        save_config_to_file()
        self.assertDictEqual(a, convert_keybinding(load_config_from_file()['keybinding']))



if __name__ == '__main__':
    unittest.main()