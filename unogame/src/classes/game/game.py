from dataclasses import dataclass

from classes.auth.user import User
from classes.decks.game_deck import GameDeck
from classes.enums.directions import Directions


@dataclass
class Game:
    users: list[User]
    deck: GameDeck
    cur_user_index: int = 0
    direction: Directions = Directions.CLOCKWISE

    def append_user(self, user: User):
        if len(self.users) <= 4:
            print(self.users)
            self.users.append(user)
        else:
            raise ValueError("Value Error")

    @property
    def is_started(self) -> bool:
        return True #if len(self.users) == 4 else False

    def next_player(self):
        print("Next Player function called! From : ", self.cur_user_index)
        if self.direction == Directions.CLOCKWISE:
            self.cur_user_index=(self.cur_user_index+1)%len(self.users)
            # if self.cur_user_index != 3:
            #     self.cur_user_index += 1
            # else:
            #     self.cur_user_index = 0
        elif self.direction == Directions.COUNTER_CLOCKWISE:
            self.cur_user_index = (self.cur_user_index-1) % len(self.users)
            # if self.cur_user_index != 0:
            #     self.cur_user_index -= 1
            # else:
            #     self.cur_user_index = 3
        print("To : ", self.cur_user_index)

    def next_player_index(self,cur_index: int, direction: Directions) -> int:
        if direction == Directions.CLOCKWISE:
            return (cur_index+1)%len(self.users)
        elif direction == Directions.COUNTER_CLOCKWISE:
            return (cur_index - 1) % len(self.users)
