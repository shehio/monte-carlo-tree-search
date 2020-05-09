from __future__ import annotations
import numpy as np


class GameState:
    def __init__(self, players: np.array, turn: int, game_board=np.zeros((3, 3))):
        assert (0 <= turn <= 1)
        self.game_board = game_board
        self.players = players
        self.turn = turn
        self.move_map = {0: (0, 0), 1: (0, 1), 2: (0, 2), 3: (1, 0),
                         4: (1, 1), 5: (1, 2), 6: (2, 0), 7: (2, 1), 8: (2, 2)}
        self.reverse_move_map = {(0, 0): 0, (0, 1): 1, (0, 2): 2, (1, 0): 3,
                                 (1, 1): 4, (1, 2): 5, (2, 0): 6, (2, 1): 8, (2, 2): 9}

    # Assigns a -1 to player 1, and 1 to player 2.
    def make_move(self, player, move: int) -> GameState:  # Returns a game state.
        assert (0 <= move <= 8)
        assert (move in self.get_legal_actions(player))
        player_index = np.where(self.players == player)
        if player_index == 0:
            player_index = -1

        game_board = self.game_board
        move_tuple = self.move_map(move)
        game_board[move_tuple[0]][move_tuple[1]] = player_index

        return GameState(self.players, 1 - self.turn, game_board)

    def get_legal_actions(self, player) -> list:
        assert self.players.contain(player)
        actions = np.array([])
        for move in self.reverse_move_map.keys():
            move_tuple = self.move_map(move)
            if self.game_board[move_tuple[0]][move_tuple[1]] == 0:
                actions = np.append(actions, self.reverse_move_map[move])

        return actions

    @property
    def is_game_over(self):  # Returns the player that won and None if the game is still in progress.
        pass
