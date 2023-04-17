from classes.auth.user import User
from states import GameState
from utils import scene_name


class StoryMapState(GameState):
    def __init__(self):
        super().__init__()

    def start_single_play(self, STAGE_NAME :int):
        if STAGE_NAME == 1:
            self.move_scene(scene_name.PLAYING_SCENE, [User(0,"Me",is_ai=False), User(1, "Stage1",is_ai=True)])
        elif STAGE_NAME == 2:
            self.move_scene(scene_name.PLAYING_SCENE, [User(0,"Me",is_ai=False), User(1, "Minsu",is_ai=True), User(2, "Amy",is_ai=True)])
        #todo 3,4,5 넣기.
