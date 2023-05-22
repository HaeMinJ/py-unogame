import os
import pygame

from config import configuration
from utils.resource_path import resource_path


def load_image(name: str, colorkey: int = None, directory: str = f'assets/{configuration.get_color_mode()}'):
    fullname = resource_path(os.path.join(directory, name))
    if not os.path.isfile(fullname):
        raise FileNotFoundError("해당하는 파일이 없습니다. '{fullname}'")
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image
