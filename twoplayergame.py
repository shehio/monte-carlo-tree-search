from __future__ import annotations


class GameState:
    def __init__(self):
        pass

    def make_move(self, player, move) -> GameState:  # Returns a game state.
        pass

    def is_game_over(self):  # Say returns -1 for p1 win, 1 for p2 win, 0 for draw, and -inf for game still in progress.
        pass

    def get_legal_actions(self, player):
        pass