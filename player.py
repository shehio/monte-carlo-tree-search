from typing import Callable
from twoplayergame import GameState


class Player:
    def __init__(self, name: str, strategy: Callable[[GameState], int]):
        self.name = name
        self.strategy = strategy

    def make_move(self, game_state: GameState):
        return self.strategy(game_state)
