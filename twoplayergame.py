from __future__ import annotations
import numpy as np


class GameState:
    board_size = 3

    def __init__(self, players: np.array, turn: int, game_board=np.zeros((board_size, board_size))):
        assert (turn == -1 or turn == 1)
        self.game_board = game_board
        self.players = players
        self.turn = turn
        self.winner = None
        self.move_map = {0: (0, 0), 1: (0, 1), 2: (0, 2), 3: (1, 0),
                         4: (1, 1), 5: (1, 2), 6: (2, 0), 7: (2, 1), 8: (2, 2)}
        self.reverse_move_map = {(0, 0): 0, (0, 1): 1, (0, 2): 2, (1, 0): 3,
                                 (1, 1): 4, (1, 2): 5, (2, 0): 6, (2, 1): 7, (2, 2): 8}

    # Assigns a -1 to player 1, and 1 to player 2.
    def make_move(self, move_index: int) -> GameState:  # Returns a game state.
        assert (0 <= move_index <= 8)
        assert (move_index in self.get_legal_actions())

        game_board = self.game_board
        move = self.move_map[move_index]
        game_board[move[0], move[1]] = self.turn

        next_turn = -1 if self.turn == 1 else 1
        return GameState(self.players, next_turn, game_board)

    def get_legal_actions(self) -> list:
        actions = []
        for move in self.reverse_move_map.keys():
            if self.game_board[move[0]][move[1]] == 0:
                actions.append(self.reverse_move_map[move])

        return actions

    def __repr__(self):
        return self.game_board.__repr__()

    @property
    def current_player(self):
        if self.turn == -1:
            self.turn = 1
        else:
            self.turn = 0
        return self.players[self.turn]

    @property
    def is_game_over(self):  # Returns the player that won and None if the game is still in progress.
        row_sum = self.game_board.sum(0)
        col_sum = self.game_board.sum(1)
        diagonal = self.game_board.trace()
        inv_diagonal = self.game_board[::-1].trace()

        winning_possibilities = np.append(row_sum, col_sum)
        winning_possibilities = np.append(winning_possibilities, diagonal)
        winning_possibilities = np.append(winning_possibilities, inv_diagonal)

        if GameState.check_board(winning_possibilities, GameState.board_size):
            self.winner = self.players[0]
            return self.winner

        if GameState.check_board(winning_possibilities, - GameState.board_size):
            self.winner = self.players[1]
            return self.winner

        return None

    @staticmethod
    def check_board(winning_possibilities, winning_number):
        return any(winning_possibilities == winning_number)
