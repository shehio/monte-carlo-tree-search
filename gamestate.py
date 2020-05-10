from __future__ import annotations
import numpy as np

from drawplayer import OnlyDrawPlayer


class GameState:
    BoardSize = 4

    def __init__(self, players: np.array, turn: int, game_board=np.zeros((BoardSize, BoardSize))):
        assert (turn == -1 or turn == 1)
        self.game_board = game_board
        self.players = players
        self.turn = turn
        self.winner = None
        self.move_map = dict(map(
            lambda x: (x, (np.int(x / GameState.BoardSize), x % GameState.BoardSize)),
            list(range(0, GameState.BoardSize ** 2))))
        self.reverse_move_map = {value: key for (key, value) in self.move_map.items()}

    # Assigns a -1 to player 1, and 1 to player 2.
    def make_move(self, move_index: int) -> GameState:
        assert (0 <= move_index <= GameState.BoardSize ** 2 - 1)
        assert (move_index in self.get_valid_moves())

        game_board = self.game_board.copy()
        move = self.move_map[move_index]
        game_board[move[0], move[1]] = self.turn

        if self.turn == 1:
            next_turn = -1
        else:
            next_turn = 1

        return GameState(self.players, next_turn, game_board)

    # In other complete information games, like chess or go, these moves would depend on the current player.
    def get_valid_moves(self) -> list:
        moves = []
        for move in self.reverse_move_map.keys():
            if self.game_board[move[0]][move[1]] == 0:
                moves.append(self.reverse_move_map[move])

        return moves

    def __repr__(self):
        return self.game_board.__repr__()

    @property
    def current_player(self):
        if self.turn == -1:
            return self.players[1]
        else:
            return self.players[0]

    @property
    def is_game_over(self):  # Returns the player that won and None if the game is still in progress.
        row_sum = self.game_board.sum(0)
        col_sum = self.game_board.sum(1)
        diagonal = [self.game_board.trace()]
        inv_diagonal = [self.game_board[::-1].trace()]
        winning_possibilities = np.concatenate((row_sum, col_sum, diagonal, inv_diagonal))

        if GameState.check_board(winning_possibilities, GameState.BoardSize):
            self.winner = self.players[0]

        if GameState.check_board(winning_possibilities, - GameState.BoardSize):
            self.winner = self.players[1]

        zeros_indices, = np.where(self.game_board.flatten() == 0)
        if len(zeros_indices) == 0:
            self.winner = OnlyDrawPlayer

        return self.winner is not None

    @staticmethod
    def check_board(winning_possibilities, winning_number):
        return any(winning_possibilities == winning_number)
