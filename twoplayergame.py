from __future__ import annotations
import numpy as np


class GameState:
    BoardSize = 3

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
    def make_move(self, move_index: int) -> GameState:  # Returns a game state.
        assert (0 <= move_index <= 8)
        assert (move_index in self.get_valid_moves())

        game_board = self.game_board.copy()
        move = self.move_map[move_index]
        game_board[move[0], move[1]] = self.turn

        if self.turn == 1:
            next_turn = -1
        else:
            next_turn = 1

        return GameState(self.players, next_turn, game_board)

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

        if GameState.check_board(winning_possibilities, GameState.BoardSize):
            self.winner = self.players[0]
            return self.winner

        if GameState.check_board(winning_possibilities, - GameState.BoardSize):
            self.winner = self.players[1]
            return self.winner

        # Fix this hack!
        flat = self.game_board.flatten()
        zeros_indices, = np.where(flat == 0)
        if len(zeros_indices) == 0:
            self.winner = 'Draw'
            return self.winner

        return None

    @staticmethod
    def check_board(winning_possibilities, winning_number):
        return any(winning_possibilities == winning_number)
