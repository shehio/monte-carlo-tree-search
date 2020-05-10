from typing import Callable
from twoplayergame import GameState


class Player:
    def __init__(self, name: str, strategy: Callable[[GameState], int]):
        self.name = name
        self.strategy = strategy

    def get_move(self, game_state: GameState):
        return self.strategy(game_state)

    def __repr__(self):
        return f'player: {self.name}'
