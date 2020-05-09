from __future__ import annotations


class GameState:
    def __init__(self):
        pass

    def make_move(self, player, move) -> GameState:  # Returns a game state.
        pass

    def get_legal_actions(self, player) -> list:
        pass

    @property
    def is_game_over(self):  # Returns the player that won and None if the game is still in progress.
        pass
