class GameState:
    def __init__(self):
        self.scene_changed = False
        self.next_scene_name = None
        self.overlay_active_changed = False
        self.overlay_active = False
        self.overlay_scene_name = None
        self.next_params = None

    def handle_events(self, events):
        pass

    def update(self):
        pass

    def move_scene(self, next_scene_name, params=None):
        self.scene_changed = True
        self.next_scene_name = next_scene_name
        self.next_params = params

    def active_overlay(self, overlay_scene_name):
        self.overlay_active_changed = True
        self.overlay_scene_name = overlay_scene_name

    def inactive_overlay(self, overlay_scene_name):
        self.overlay_active_changed = False
        self.overlay_scene_name = overlay_scene_name
