import asyncio

import pygame
import sys
from pygame.locals import *

import pygame_gui

from utils.scene_manager import SceneManager
from config import get_screen_width, get_screen_height, vw, vh, configuration
from assets.image_loader import ImageLoader

# Initialize pygame and create a window
pygame.init()
screen = pygame.display.set_mode((get_screen_width(), get_screen_height()))
loop = asyncio.get_event_loop()
loop.run_until_complete(configuration.load_config_from_file())
loop.close()
pygame.display.set_caption("UnoCatMe")
INIT_SCREEN_WIDTH = get_screen_width()

# Set up the GUI manager
gui_manager = pygame_gui.UIManager((configuration.SCREEN_WIDTH, configuration.SCREEN_HEIGHT), "theme.json")
gui_manager.set_visual_debug_mode(True)

overlay_manager = pygame_gui.UIManager((configuration.SCREEN_WIDTH, configuration.SCREEN_HEIGHT), "theme.json")
overlay_manager.set_visual_debug_mode(True)

# Set up clock for controlling the frame rate
clock = pygame.time.Clock()

#image_loader = ImageLoader()
# Create a SceneManager instance
scene_manager = SceneManager(screen, gui_manager, overlay_manager)
while True:
    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        scene_manager.process_events(event)
        if event.type == pygame.VIDEORESIZE:
            print("Resized!")
        if INIT_SCREEN_WIDTH != get_screen_width():
            del scene_manager
            INIT_SCREEN_WIDTH = get_screen_width()
            screen = pygame.display.set_mode((get_screen_width(), get_screen_height()))
            gui_manager.set_window_resolution((get_screen_width(),get_screen_height()))
            overlay_manager.set_window_resolution((get_screen_width(),get_screen_height()))
            # gui_manager = pygame_gui.UIManager((get_screen_width(), get_screen_height()), "theme.json")
            #
            # overlay_manager = pygame_gui.UIManager((get_screen_width(), get_screen_height()),
            #                                        "theme.json")

            scene_manager = SceneManager(screen, gui_manager, overlay_manager)

    gui_manager.update(time_delta)
    overlay_manager.update(time_delta)
    scene_manager.update()

    scene_manager.draw()
    pygame.display.flip()

#pygame.quit()