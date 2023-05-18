import pygame

from classes.auth.user import User
from classes.game.networking import Networking
from scene.lobby_scene import LobbyScene
from scene.main_screen import MainScreen
from scene.multi_access_scene import MultiAccessScene
from scene.multi_game_scene import MultiGameScene
from scene.multi_robby_scene import MultiRobbyScene
from scene.multi_role_scene import MultiRoleScene
from scene.result_scene import ResultScene
from utils import scene_name, overlay_name
from scene import MenuScene,LandingScene,PlayingScene,ConfigurationOverlayScene, StoryMapScene
from utils.resource_path import resource_path


class SceneManager:
    _instance = None

    def __init__(self, screen, gui_manager, overlay_manager):
        # if SceneManager._instance is not None:
        #     raise Exception("SceneManager should be a singleton class.")
        # SceneManager._instance = self

        self.screen = screen
        self.gui_manager = gui_manager
        self.overlay_manager = overlay_manager
        self.overlay_activate = False
        from config import configuration
        self.current_sound_volume = configuration.get_sound_volume()
        self.current_sound_on = configuration.is_sound_on()

        self.sounds = {
            "LOBBY":  pygame.mixer.Sound(resource_path("assets/sound/lobby.mp3")),
            "PLAYING": pygame.mixer.Sound(resource_path("assets/sound/game.mp3"))
        }

        self.scenes = {
            scene_name.LANDING: LandingScene,
            scene_name.MAIN_MENU: MenuScene,
            scene_name.PLAYING_GAME: PlayingScene,
            scene_name.LOBBY_SCENE: LobbyScene,
            scene_name.STORY_MAP_SCENE: StoryMapScene,
            scene_name.PLAYING_SCENE: MainScreen,
            scene_name.RESULT_SCENE: ResultScene,
            scene_name.MULTI_ROLE_SCENE : MultiRoleScene,
            scene_name.MULTI_ACCESS_SCENE: MultiAccessScene,
            scene_name.MULTI_GAME_SCENE: MultiGameScene,
            scene_name.MULTI_ROBBY_SCENE: MultiRobbyScene
        }
        self.overlay_scenes = {
            overlay_name.CONFIGURATION: ConfigurationOverlayScene
        }
        self.current_sound = self.sounds["LOBBY"]
        self.current_sound.play()
        params = {"winner":User(0,'haemin')}
        self.current_scene = self.scenes[scene_name.PLAYING_GAME](screen, gui_manager)
        self.current_overlay = self.overlay_scenes[overlay_name.CONFIGURATION](screen, overlay_manager)

    def update(self):
        from config import configuration
        if self.current_sound_on != configuration.is_sound_on():
            self.current_sound_on = configuration.is_sound_on()
            if self.current_sound_on:
                self.current_sound.play()
            else:
                self.current_sound.stop()
        if self.current_sound_volume != configuration.get_sound_volume():
            self.current_sound.set_volume(configuration.get_sound_volume())
            self.current_sound_volume = configuration.get_sound_volume()

        if self.current_scene.state.scene_changed:
            self.current_scene.state.scene_changed = False
            self.current_scene = self.scenes[self.current_scene.state.next_scene_name](self.screen, self.gui_manager, self.current_scene.state.next_params)
            print("Scene moved(Current Scene) : ", self.current_scene)

        if self.current_scene.state.overlay_active_changed:

            self.current_overlay = self.overlay_scenes[self.current_scene.state.overlay_scene_name](self.screen,
                                                                                                    self.overlay_manager)
            self.current_overlay.overlay_active_changed = False
            self.current_scene.state.overlay_active_changed = False
            self.overlay_activate = self.current_scene.state.overlay_active
            if self.overlay_activate:
                self.current_overlay.set_active()
            else:
                self.current_overlay.set_inactive()

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

