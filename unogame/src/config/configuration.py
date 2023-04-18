# Screen dimensions
import copy

from utils import blind_mode_name
import pygame
import json

from utils import action_name
import unittest

BLIND_MODE = blind_mode_name.DEUTERANOPIA
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
CURRENT_STAGE = 0
SOUND_VOLUME = 30
SOUND_ON = True

def set_sound_volume(v:int):
    global SOUND_VOLUME
    SOUND_VOLUME = v
def get_sound_volume():
    return SOUND_VOLUME
def set_sound_on():
    global SOUND_ON
    SOUND_ON = True
def set_sound_off():
    global SOUND_ON
    SOUND_ON = False
def is_sound_on():
    return SOUND_ON

def get_screen_width():
    return SCREEN_WIDTH

def get_screen_height():
    return SCREEN_HEIGHT

def set_screen_size(width, height):
    global SCREEN_HEIGHT
    global SCREEN_WIDTH
    SCREEN_WIDTH = width
    SCREEN_HEIGHT = height
    pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))


KEYBOARD_MAP = {
    pygame.K_UP: action_name.MOVE_UP,
    pygame.K_DOWN: action_name.MOVE_DOWN,
    pygame.K_LEFT: action_name.MOVE_LEFT,
    pygame.K_RIGHT: action_name.MOVE_RIGHT,
    pygame.K_SPACE: action_name.FIRE,
    pygame.K_ESCAPE: action_name.PAUSE,
    pygame.K_RETURN: action_name.RETURN
    # Add more key-action mappings here
}

def vw(width):
    return (width * SCREEN_WIDTH) / 1280

def vh(height):
    return (height * SCREEN_HEIGHT) / 720


def vp(width, height):
    return vw(width), vh(height)

def get_action(key):
    try:
        return KEYBOARD_MAP[key]
    except KeyError:
        return None

def save_config_to_file():
    keybindings = {key: action for key, action in KEYBOARD_MAP.items()}
    configurations = {
        "BLIND_MODE" : BLIND_MODE,
        "SCREEN_HEIGHT" : SCREEN_HEIGHT,
        "SCREEN_WIDTH" : SCREEN_WIDTH,
        "keybinding" : keybindings,
        "CURRENT_STAGE": CURRENT_STAGE,
        "SOUND_VOLUME":SOUND_VOLUME,
        "SOUND_ON":SOUND_ON
    }
    with open("config.json", "w") as f:
        json.dump(configurations, f)
    return configurations


async def load_config_from_file():
    with open("config.json", "r") as f:
        configurations = json.load(f)
        print(configurations)
    convert_to_current_config(configurations)
    convert_keybinding(configurations["keybinding"])
    pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    return configurations

def convert_to_current_config(configurations):
    global BLIND_MODE
    global SCREEN_WIDTH
    global SCREEN_HEIGHT
    global CURRENT_STAGE
    global SOUND_VOLUME
    global SOUND_ON
    try:
        BLIND_MODE=configurations["BLIND_MODE"]
        SCREEN_WIDTH=configurations["SCREEN_WIDTH"]
        SCREEN_HEIGHT=configurations["SCREEN_HEIGHT"]
        CURRENT_STAGE=configurations["CURRENT_STAGE"]
        SOUND_ON=configurations["SOUND_ON"]
        SOUND_VOLUME=configurations["SOUND_VOLUME"]
    except(KeyError):
        print("No Initial config valid.")


def convert_keybinding(keybindings):
    global KEYBOARD_MAP
    keybindings={int(key): action for key, action in keybindings.items()}
    KEYBOARD_MAP=keybindings
    print(keybindings)
    return keybindings



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
