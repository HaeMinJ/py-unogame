from dataclasses import dataclass

from classes.auth.user import User


@dataclass
class AIUser(User):
    def __post_init__(self):
        super().__post_init__()
        self.throwable = True
        self.is_ai = True

    def do_action(self, networking):
        super().do_action(networking)
        can_throw = False
        cur_user = networking.get_user_from_game()
        for card in range(len(networking.get_user_from_game().deck.cards)):
            if networking.throw_card(cur_user.id, card):  # self.networking.get_user_from_game().deck.cards[0])
                can_throw = True
                break
        if not can_throw:
            networking.get_card()
        self.throwable = True


