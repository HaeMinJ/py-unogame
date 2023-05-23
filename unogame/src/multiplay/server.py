import logging
import pickle
import socket
import threading
from typing import Callable, NoReturn

from classes.auth.user import User
from classes.cards.card import Card
from classes.cards.wild_cards import WildCard, WildChangeColorCard, WildGetFourCard
from classes.decks.game_deck import GameDeck
from classes.game.game import Game

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG)


class Server:
    """
    Сервер игры построенный с помощью Singleton паттерна
    """

    # Конечно, это ничего более чем просто демонстрация
    # учитывая, мою базу по сетям, я бы мог и написать эту историю поверх UDP,
    # сконструировать красивый протокол, сделать сервер не блокирующим (т.е. асинхронным)
    # но времени мало + мне лень, а также в лицее нам про асинхронность почему-то не рассказывают)
    def __init__(self, password, address: str = socket.gethostname(), port: int = 5499):
        self.current_game = Game([], GameDeck())
        self.current_game.deck.init_random()
        self.user_list_changed = False
        self.password = password
        self.threads = []
        # порт в моём случае выбран абсолютно случайно
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._bind(address, port)
        self._listen()

    def _bind(self, address: str, port: int):
        self.sock.bind((address, port))

    def _listen(self, max_clients: int = 3):
        self.sock.listen(max_clients)

    def __fetch(self):
        return self.current_game

    def __update(self, data: dict):
        pass
        # match data["update_type"]:

    def __throw(self, user, card: int | Card, ignore: bool) -> bool:
        if type(card) == int:
            card_object = user.deck.cards[card]
        else:
            card_object = card
        result = self.current_game.deck.append_card(card_object, ignore=ignore)
        if result:
            if len(user.deck.cards) == 2 and not user.deck.uno_said:
                user.deck.random_cards(2)
            card_object.move(self.current_game)
            if type(card) == int:
                user.deck.cards.pop(card)
            print(self.current_game.cur_user_index)
            if type(card_object) not in [WildChangeColorCard, WildGetFourCard]:
                # because it will change player after choosing a color
                self.current_game.next_player()
        return result

    @staticmethod
    def __get_card(user) -> bool:
        user.deck.random_cards()
        return True

    # this method shouldn't be a static, because then it will be executed in another thread
    # def __add_points(self, auth: Authorization, user, amount=0) -> bool:
    #     auth.add_points(user.id, amount)
    #     return True

    @staticmethod
    def __say_uno(user):
        user.deck.uno_said = True
        return True

    def _client_thread(self, sock: socket.socket, address: tuple[str, int]):
        while True:
            data = sock.recv(2048)
            if not data:
                logging.info(f"Client {address} closed connection, so we are closing it too")
                try:
                    pass
                    # self.current_game.users.remove(
                    #     [user for user in self.current_game.users if user.address == address][0])
                except IndexError:
                    logging.warning(f"User with address {address} didnt logon, so we cant remove it")
                sock.close()
                break
            loaded_data: dict = pickle.loads(data)

            answer = None
            # python 3.10 goes brrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr
            match loaded_data['type']:
                case "access":
                    password = loaded_data['password']
                    if password == self.password:
                        answer = "allow"
                        user = User(len(self.current_game.users), "Player"+str(len(self.current_game.users)))
                        user.deck.init_random()
                        user.address = address
                        self.current_game.append_user(user)
                        self.user_list_changed = True
                    else:
                        answer = "deny"
                case "fetch":
                    answer = self.__fetch()
                case "update":
                    self.__update(loaded_data)
                    answer = self.__fetch()
                case "throw":
                    answer = self.__throw(self._user_by_address(address), loaded_data['card'],
                                          loaded_data['ignore'])
                case "get_card":
                    answer = self.__get_card(self._user_by_address(address))
                # case "add_points":
                #     answer = self.__add_points(authorization, self._user_by_address(address),
                #                                loaded_data['amount'])
                case "say_uno":
                    answer = self.__say_uno(self._user_by_address(address))
            sock.sendall(pickle.dumps(answer))

    def _user_by_address(self, address: tuple[str, int]):
        return [user for user in self.current_game.users if user.address == address][0]

    def mainloop(self, client_thread: Callable = None) -> NoReturn:
        if not client_thread:
            client_thread = self._client_thread
        while True:
            client_socket, client_address = self.sock.accept()
            #logging.info(f"New client {client_address}, starting client thread")
            thread = threading.Thread(target=client_thread, args=(client_socket, client_address))
            self.threads.append(thread)
            thread.start()
            #if self.current_game.is_started:
            #    self.current_game.deck.cards[0].move(self.current_game)

    def __del__(self):
        self.sock.close()


if __name__ == '__main__':
    server = Server(address='127.0.0.1')
    server.mainloop()
