from dataclasses import dataclass

from classes.cards.card import Card
from classes.enums.directions import Directions
from utils.player_utility import next_player_index


@dataclass
class SpecialCard(Card):
    def __post_init__(self):
        self.nominal = 20

    def possible_move(self, card: Card) -> bool:
        if super().possible_move(card) or card.__class__ == self.__class__:
            return True
        else:
            return False


@dataclass
class GetTwoCard(SpecialCard):
    @staticmethod
    def move(game):
        game.users[game.next_player_index(game.cur_user_index, game.direction)].deck.random_cards(2)

@dataclass
class GetOneCard(SpecialCard):
    @staticmethod
    def move(game):
        game.users[game.next_player_index(game.cur_user_index, game.direction)].deck.random_cards(1)

@dataclass
class GetThreeCard(SpecialCard):
    @staticmethod
    def move(game):
        game.users[game.next_player_index(game.cur_user_index, game.direction)].deck.random_cards(3)


@dataclass
class ReverseCard(SpecialCard):
    @staticmethod
    def move(game):
        if game.direction == Directions.CLOCKWISE:
            game.direction = Directions.COUNTER_CLOCKWISE
        else:
            game.direction = Directions.CLOCKWISE


@dataclass
class SkipCard(SpecialCard):
    @staticmethod
    def move(game):
        print("Skip Card!")
        game.next_player()
