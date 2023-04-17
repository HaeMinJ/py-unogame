from __future__ import annotations

import pickle
import time

import pygame.time

from classes.auth.exceptions import WrongCredentials
from classes.auth.user import User
from classes.cards.card import Card
from classes.cards.wild_cards import WildChangeColorCard, WildGetFourCard
from classes.decks.game_deck import GameDeck
from classes.enums.colors import Colors
from classes.game.game import Game
from utils.card_utility import random_cards


class Networking:
    """
    Networking-singleton для авторизации и обмена состояниями игры
    """

    def __init__(self, players=None): #, address: str = socket.gethostname(), port: int = 5499):
        if players is None:
            players = [User(0, "Me"), User(1, "Computer1", is_ai=True), User(2, "Computer2", is_ai=True),
                       User(3, "Computer3", is_ai=True)]
        self.current_game: Game = Game(players, GameDeck())
        self.current_game.deck.init_random()
        #self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.authorized_user = None
        #self._connect(address, port)
        self.user = self.get_user_from_game()

    def _connect(self, address, port):
        pass
#        self.sock.connect((address, port))

    # def login(self, username, password) -> User:
    #     data = {'type': 'login', 'username': username, 'password': password}
    #     self.sock.sendall(pickle.dumps(data))
    #     answer = user, game = pickle.loads(self.sock.recv(2048))
    #     if type(answer) == dict:
    #         raise WrongCredentials(answer['message'])
    #     else:
    #         self.authorized_user = user
    #         self.current_game = game
    #         return answer
    #
    # def register(self, username, password) -> User:
    #     data = {'type': 'register', 'username': username, 'password': password}
    #     self.sock.sendall(pickle.dumps(data))
    #     answer = user, game = pickle.loads(self.sock.recv(2048))
    #     if type(answer) == dict:
    #         raise ValueError(answer['message'])
    #     else:
    #         self.authorized_user = user
    #         self.current_game = game
    #         return answer

    # def fetch(self):
    #     data = {'type': 'fetch'}
    #     #self.sock.sendall(pickle.dumps(data))
    #     self.current_game = pickle.loads(self.sock.recv(4096))

    def throw_card(self, userIdx: int, card: int | Card, ignore: bool = False) -> bool:
        current_user = self.get_user_from_game()
        print("Request UserID", userIdx,"CurrentUserId", current_user.id)
        if current_user.id != userIdx:
            print("Not",userIdx,"Turn! It's", current_user.id, "turn")
            return False
        print(card, " was requested to thrown")
        if type(card) == int:
            card_object = current_user.deck.cards[card]

        else:
            card_object = card
        result = self.current_game.deck.append_card(card_object, ignore=ignore)
        if result:
            if len(current_user.deck.cards) == 2 and not current_user.deck.uno_said:
                current_user.deck.random_cards(2)
            card_object.move(self.current_game)
            if type(card) == int:
                print("POP card in", current_user)
                current_user.deck.cards.pop(card)
            #print(self.current_game.cur_user_index)
            if type(card_object) not in [WildChangeColorCard, WildGetFourCard]:
                # because it will change player after choosing a color
                self.current_game.next_player()
                pass
            elif current_user.is_ai:
                pygame.time.delay(1000)
                import random
                card = random_cards(color=random.choice([Colors.RED,Colors.BLUE,Colors.GREEN,Colors.YELLOW]))[0]
                self.throw_card(current_user.id, card, ignore=True)
                pass

        return result


    def get_card(self) -> bool:
        data = {'type': 'get_card'}
        self.user.deck.random_cards()
        self.current_game.next_player()
        return True
        # self.sock.sendall(pickle.dumps(data))
        # return pickle.loads(self.sock.recv(2048))

    #def add_points(self, amount: int = 0) -> bool:
        #auth.add_points(self.user.id, amount)
        #return True
        #data = {'type': 'add_points', 'amount': amount}
        # self.sock.sendall(pickle.dumps(data))
        # return pickle.loads(self.sock.recv(2048))

    def say_uno(self) -> bool:
        self.user.deck.uno_said = True
        return True
        #data = {'type': 'say_uno'}
        # self.sock.sendall(pickle.dumps(data))
        # return pickle.loads(self.sock.recv(2048))

    def get_user_from_game(self) -> User:
        return [user for user in self.current_game.users][self.current_game.cur_user_index] #if user.id == self.authorized_user.id][0]

    def user_id(self, user) -> int:
        return self.current_game.users.index(user)


    @property
    def is_our_move(self) -> bool:
        return self.current_game.cur_user_index == 0 #self.user_id(self.get_user_from_game())

    # def __del__(self):
    #     self.sock.close()
