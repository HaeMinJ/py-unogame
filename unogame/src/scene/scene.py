from abc import abstractmethod


class Scene:


    def __init__(self, screen, gui_manager, params=None, server=None):
        self.screen = screen
        self.gui_manager = gui_manager
        self.params = params
        self.state = None
        self.gui_manager.clear_and_reset()
        self.focusable_buttons = []
        self.server = server
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


