# Screen dimensions
import copy

from utils import blind_mode_name
import pygame
import json

from utils import action_name
import unittest

BLIND_MODE = blind_mode_name.DEFAULT
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
CURRENT_STAGE = 0
WHOLE_SOUND_VOLUME = 30
BACKGROUND_SOUND_VOLUME = 30
EFFECT_SOUND_VOLUME = 30
SOUND_ON = True

def set_whole_sound_volume(v:int):
    global WHOLE_SOUND_VOLUME
    WHOLE_SOUND_VOLUME = v
def set_background_sound_volume(v:int):
    global BACKGROUND_SOUND_VOLUME
    BACKGROUND_SOUND_VOLUME = v
def set_effect_sound_volume(v:int):
    global EFFECT_SOUND_VOLUME
    EFFECT_SOUND_VOLUME = v

def get_whole_sound_volume():
    return WHOLE_SOUND_VOLUME
def get_background_sound_volume():
    return BACKGROUND_SOUND_VOLUME
def get_effect_sound_volume():
    return EFFECT_SOUND_VOLUME
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
        "WHOLE_SOUND_VOLUME" : WHOLE_SOUND_VOLUME,
        "BACKGROUND_SOUND_VOLUME" : BACKGROUND_SOUND_VOLUME,
        "EFFECT_SOUND_VOLUME" : EFFECT_SOUND_VOLUME,
        "SOUND_ON":SOUND_ON
    }
    with open("config.json", "w") as f:
        json.dump(configurations, f)
    return configurations


async def load_config_from_file():
    filename="config.json"
    configurations = {
        "BLIND_MODE": BLIND_MODE,
        "SCREEN_HEIGHT": SCREEN_HEIGHT,
        "SCREEN_WIDTH": SCREEN_WIDTH,
        "keybinding": KEYBOARD_MAP,
        "CURRENT_STAGE": CURRENT_STAGE,
        "WHOLE_SOUND_VOLUME": WHOLE_SOUND_VOLUME,
        "BACKGROUND_SOUND_VOLUME": BACKGROUND_SOUND_VOLUME,
        "EFFECT_SOUND_VOLUME": EFFECT_SOUND_VOLUME,
        "SOUND_ON": SOUND_ON
    }
    try:
        with open(filename, "a") as f:
            configurations = json.load(f)
            convert_to_current_config(configurations)
            convert_keybinding(configurations["keybinding"])
            pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    except FileNotFoundError:
        print(f"The file '{filename}' does not exist. Creating a new file.")
        with open(filename, 'w') as file:
            # The file is created
            # Add your file operations here, e.g., writing to the file
            file.write("This is a new line.\n")
    except IOError as e:
        print(f"An error occurred while opening/creating the file: {e}")

    return configurations

def convert_to_current_config(configurations):
    global BLIND_MODE
    global SCREEN_WIDTH
    global SCREEN_HEIGHT
    global CURRENT_STAGE
    global WHOLE_SOUND_VOLUME
    global BACKGROUND_SOUND_VOLUME
    global EFFECT_SOUND_VOLUME
    global SOUND_ON
    try:
        BLIND_MODE=configurations["BLIND_MODE"]
        SCREEN_WIDTH=configurations["SCREEN_WIDTH"]
        SCREEN_HEIGHT=configurations["SCREEN_HEIGHT"]
        CURRENT_STAGE=configurations["CURRENT_STAGE"]
        SOUND_ON=configurations["SOUND_ON"]
        WHOLE_SOUND_VOLUME = configurations["WHOLE_SOUND_VOLUME"]
        BACKGROUND_SOUND_VOLUME = configurations["BACKGROUND_SOUND_VOLUME"]
        EFFECT_SOUND_VOLUME = configurations["EFFECT_SOUND_VOLUME"]

    except(KeyError):
        print("No Initial config valid.")


def convert_keybinding(keybindings):
    global KEYBOARD_MAP
    keybindings={int(key): action for key, action in keybindings.items()}
    KEYBOARD_MAP=keybindings
    print(keybindings)
    return keybindings
