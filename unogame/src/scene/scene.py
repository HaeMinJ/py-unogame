from abc import abstractmethod


class Scene:
    focusable_buttons = []

    def __init__(self, screen, gui_manager):
        self.screen = screen
        self.gui_manager = gui_manager
        self.state = None
        self.gui_manager.clear_and_reset()
        pass

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def process_events(self, event):
        pass

    @abstractmethod
    def resize_images(self):
        pass

    @abstractmethod
    def initialize_elements(self):
        pass


