import pygame

from classes.game.networking import Networking
from scene.lobby_scene import LobbyScene
from scene.main_screen import MainScreen
from utils import scene_name, overlay_name
from scene import MenuScene, LandingScene, PlayingScene, ConfigurationOverlayScene, StoryMapScene


class SceneManager:
    _instance = None

    def __init__(self, screen, gui_manager, overlay_manager):
        if SceneManager._instance is not None:
            raise Exception("SceneManager should be a singleton class.")
        SceneManager._instance = self

        # self.image_loader = image_loader
        self.screen = screen
        self.gui_manager = gui_manager
        self.overlay_manager = overlay_manager
        self.overlay_activate = False

        self.scenes = {
            scene_name.LANDING: LandingScene,
            scene_name.MAIN_MENU: MenuScene,
            scene_name.PLAYING_GAME: PlayingScene,
            scene_name.LOBBY_SCENE: LobbyScene,
            scene_name.STORY_MAP_SCENE: StoryMapScene,
            scene_name.PLAYING_SCENE: MainScreen,
        }
        self.overlay_scenes = {
            overlay_name.CONFIGURATION: ConfigurationOverlayScene
        }
        self.current_scene = self.scenes[scene_name.STORY_MAP_SCENE](screen, gui_manager)
        self.current_overlay = self.overlay_scenes[overlay_name.CONFIGURATION](screen, overlay_manager)

    def update(self):
        if self.current_scene.state.scene_changed:
            self.current_scene.state.scene_changed = False
            self.current_scene = self.scenes[self.current_scene.state.next_scene_name](self.screen, self.gui_manager, self.current_scene.state.next_params)
            print("Scene moved(Current Scene) : ", self.current_scene)

        if self.current_scene.state.overlay_active_changed:
            self.current_scene.state.overlay_active_changed = False
            self.current_overlay = self.overlay_scenes[self.current_scene.state.overlay_scene_name](self.screen,
                                                                                                    self.overlay_manager)

            self.current_overlay.set_active()
            self.overlay_activate = True
            print("Overlay status changed")

    def process_events(self, event):
        if not self.current_overlay.active:
            self.current_scene.process_events(event)
            self.gui_manager.process_events(event)
        else:
            self.current_overlay.process_events(event)
            self.overlay_manager.process_events(event)

    def draw(self):
        self.current_scene.draw()
        self.current_overlay.draw()
