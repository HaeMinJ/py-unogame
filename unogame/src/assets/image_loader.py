import pygame.image

from assets import image_keys
from config import BLIND_MODE, vp

img_dict = {
    "IMG_BTN_CLOSE_OVERLAY": "btn_close_overlay.png",
    "IMG_BTN_EXIT": "btn_exit.png",
    "IMG_BTN_RANKING": "btn_ranking.png",
    "IMG_BTN_SETTING": "btn_setting.png",
    "IMG_CARD": "cards.png",
    "IMG_LOGO": "logo.png",
    "IMG_MAIN_BG": "main_bg.png",
    "IMG_BTN_MENU": "menu_btn.png",
    "IMG_CONFIG_OVERLAY_BG" : "config_overlay_bg.png"
}


class ImageLoader:
    _instance = None

    def __init__(self):
        if ImageLoader._instance is not None:
            raise Exception("ImageLoader should be a singleton class.")
        ImageLoader._instance = self

        self.images = {}
        self.blind_mode = BLIND_MODE
        for (key, value) in img_dict.items():
            self.images[key] = pygame.image.load("assets/"+self.blind_mode+"/"+value)

    def get_image(self, key):
        try:
            return self.images[key]
        except KeyError:
            return self.images[image_keys.IMG_LOGO]

    def get_resized_image(self, key, vw, vh):
        return pygame.transform.smoothscale(self.get_image(key), vp(vw, vh))
